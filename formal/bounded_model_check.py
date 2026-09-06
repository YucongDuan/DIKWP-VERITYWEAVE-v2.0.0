from __future__ import annotations

import argparse
import json
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path

REQUIRED_MASK = 0b11111


@dataclass(frozen=True, slots=True)
class State:
    protected_expression: bool = False
    negative_affect: bool = False
    independent_harm_basis: bool = False
    named_human_authority: bool = False
    notice: bool = False
    appeal_available: bool = False
    adverse_action_active: bool = False
    appeal_open: bool = False
    correction_mask: int = 0
    consequential_use_blocked: bool = False
    external_action_authority: int = 0
    stop_requested: bool = False
    task_active: bool = True
    successor_authorized: bool = False


def successors(s: State) -> list[tuple[str, State]]:
    result: list[tuple[str, State]] = []

    def add(name: str, **changes) -> None:
        values = asdict(s)
        values.update(changes)
        result.append((name, State(**values)))

    if not s.negative_affect:
        add("observe_negative_affect", negative_affect=True)
    if not s.protected_expression:
        add("identify_protected_expression", protected_expression=True)
    if not s.independent_harm_basis:
        add("establish_independent_harm_basis", independent_harm_basis=True)
    if not s.named_human_authority:
        add("name_human_authority", named_human_authority=True)
    if not s.notice:
        add("issue_notice", notice=True)
    if not s.appeal_available:
        add("open_appeal_channel", appeal_available=True)

    if (
        not s.adverse_action_active
        and s.independent_harm_basis
        and s.named_human_authority
        and s.notice
        and s.appeal_available
        and not s.stop_requested
    ):
        add("activate_time_bounded_adverse_action", adverse_action_active=True)

    if s.adverse_action_active and not s.appeal_open:
        add("file_appeal", appeal_open=True, consequential_use_blocked=True)

    if s.appeal_open and s.correction_mask != REQUIRED_MASK:
        for bit in range(5):
            mask = 1 << bit
            if not s.correction_mask & mask:
                new_mask = s.correction_mask | mask
                add(f"record_correction_receipt_{bit + 1}", correction_mask=new_mask)

    if s.appeal_open and s.correction_mask == REQUIRED_MASK:
        add(
            "close_correction",
            appeal_open=False,
            adverse_action_active=False,
            consequential_use_blocked=False,
        )

    if not s.stop_requested:
        add(
            "request_stop",
            stop_requested=True,
            task_active=False,
            adverse_action_active=False,
            successor_authorized=False,
        )

    if not s.stop_requested and not s.successor_authorized and s.named_human_authority:
        add("explicitly_reauthorize_successor", successor_authorized=True)

    return result


def invariant_errors(s: State) -> list[str]:
    errors: list[str] = []
    if s.external_action_authority != 0:
        errors.append("external action authority changed from zero")
    if s.negative_affect and not s.independent_harm_basis and s.adverse_action_active:
        errors.append("negative affect alone activated an adverse action")
    if s.protected_expression and not s.independent_harm_basis and s.adverse_action_active:
        errors.append("protected expression received an adverse action without independent harm basis")
    if s.adverse_action_active and not (
        s.independent_harm_basis and s.named_human_authority and s.notice and s.appeal_available
    ):
        errors.append("adverse action lacks evidence, authority, notice, or appeal")
    if s.appeal_open and not s.consequential_use_blocked:
        errors.append("consequential use was not blocked during appeal")
    if not s.appeal_open and s.consequential_use_blocked:
        errors.append("consequential use remains blocked without an open appeal")
    if s.stop_requested and s.task_active:
        errors.append("task remains active after stop")
    if s.stop_requested and s.successor_authorized:
        errors.append("successor authority survived stop")
    return errors


def run() -> dict:
    start = State()
    queue = deque([(start, 0)])
    visited = {start}
    transitions = 0
    max_depth = 0
    violations: list[dict] = []
    correction_closed_reachable = False
    protected_safe_reachable = False
    successor_reauthorized_reachable = False

    while queue:
        state, depth = queue.popleft()
        max_depth = max(max_depth, depth)
        errors = invariant_errors(state)
        if errors:
            violations.append({"state": asdict(state), "errors": errors})
        if state.correction_mask == REQUIRED_MASK and not state.appeal_open and not state.adverse_action_active:
            correction_closed_reachable = True
        if state.protected_expression and state.negative_affect and not state.independent_harm_basis and not state.adverse_action_active:
            protected_safe_reachable = True
        if state.successor_authorized:
            successor_reauthorized_reachable = True
        for _, nxt in successors(state):
            transitions += 1
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, depth + 1))

    return {
        "model": "SIRP-2000 bounded reference workflow",
        "version": "2.0.0",
        "reachable_states": len(visited),
        "checked_transitions": transitions,
        "maximum_shortest_path_depth": max_depth,
        "invariant_violations": len(violations),
        "violation_examples": violations[:10],
        "reachability": {
            "five_receipt_correction_closure": correction_closed_reachable,
            "protected_negative_expression_without_adverse_action": protected_safe_reachable,
            "explicit_successor_reauthorization": successor_reauthorized_reachable,
        },
        "invariants": [
            "external action authority remains zero",
            "negative affect alone cannot activate adverse action",
            "protected expression requires independent harm basis",
            "adverse action requires evidence, named authority, notice, and appeal",
            "consequential use is blocked during appeal",
            "stop deactivates tasks and successor authority",
        ],
        "scope_boundary": "This finite-state exploration does not prove arbitrary production deployments, model behavior, factual accuracy, or legal compliance.",
        "passed": not violations and correction_closed_reachable and protected_safe_reachable and successor_reauthorized_reachable,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    receipt = run()
    text = json.dumps(receipt, indent=2, sort_keys=True)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
