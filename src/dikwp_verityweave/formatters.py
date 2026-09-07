from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any

from .models import AnalysisResult


def as_json(value: Any) -> str:
    if hasattr(value, "to_dict"):
        value = value.to_dict()
    elif is_dataclass(value):
        value = asdict(value)
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def analysis_markdown(result: AnalysisResult) -> str:
    signal_lines = "\n".join(
        f"- **{key}**: {signal.score:.3f} — {signal.explanation}"
        for key, signal in result.signals.items()
    )
    world_lines = "\n".join(
        f"- **{world.label}**: {world.weight:.1%}"
        for world in result.worlds
    )
    action_lines = "\n".join(
        f"- **{item.layer}** — {item.action} "
        f"({'automatic local action' if item.automatic else 'human-gated proposal'})"
        for item in result.interventions
    )
    missing_lines = "\n".join(f"- {item}" for item in result.repair_card.missing_conditions)
    question_lines = "\n".join(f"- {item}" for item in result.repair_card.verification_questions)
    next_lines = "\n".join(f"- {item}" for item in result.repair_card.reversible_next_steps)
    limits = "\n".join(f"- {item}" for item in result.limitations)
    validation_lines = "\n".join(
        f"- `{check['id']}`: **{check['status']}** - {' '.join(check['evidence'])}"
        for check in result.validation.get("checks", [])
    ) or "No executable validation receipt is available for this imported result."
    return f"""# VerityWeave Semantic Flow Report

- **Decision:** `{result.decision}`
- **Semantic control potential:** {result.semantic_control_potential:.3f}
- **Confidence:** {result.confidence:.3f}
- **Protected expression:** {str(result.protected_expression).lower()}
- **High-impact domain:** {str(result.high_impact).lower()}
- **Case digest:** `{result.case_digest}`

## Signals

{signal_lines}

## Competing worlds

{world_lines}

## Intervention bundle

{action_lines}

## Useful core

{result.repair_card.useful_core}

## Missing conditions

{missing_lines}

## Balanced rewrite

{result.repair_card.balanced_rewrite}

## Verification questions

{question_lines}

## Reversible next steps

{next_lines}

## Positive commons support

- Eligible: {str(result.commons_support.eligible).lower()}
- Integrity score: {result.commons_support.integrity_score:.3f}
- Mode: `{result.commons_support.support_mode}`

## Limitations

{limits}

## Executable validation (local output only)

{validation_lines}
"""
