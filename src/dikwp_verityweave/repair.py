from __future__ import annotations

from .models import RepairCard, SemanticFlowCase, Signal


def build_repair_card(case: SemanticFlowCase, signals: dict[str, Signal]) -> RepairCard:
    text = case.text.casefold()
    family_case = case.domain == "family_parenting" or any(term in text for term in ("mother", "child", "parent", "caregiver", "husband", "wife"))

    if family_case:
        return RepairCard(
            useful_core=(
                "A caregiver's sustained exhaustion can reduce the quality and safety of care. "
                "Rest, health support, dignity, and protected personal time can therefore be legitimate needs."
            ),
            missing_conditions=[
                "The child's age, health, dependency, and non-negotiable safety needs.",
                "The responsibilities of the other parent, family members, institutions, and public services.",
                "The difference between restorative self-care and unilateral withdrawal from agreed responsibilities.",
                "Available time, money, sleep, substitute care, transport, and emergency support.",
                "Whether violence, coercive control, mental-health crisis, or child-safety concerns are present.",
            ],
            affected_parties=[
                "The primary caregiver",
                "The child or dependent person",
                "The other caregiver or partner",
                "Extended family or substitute carers",
                "Relevant health, education, or social-support services",
            ],
            likely_misreadings=[
                "My needs must always come before the child's basic needs.",
                "Caregiver exhaustion is solely a failure to love oneself.",
                "The partner is necessarily the enemy of self-realization.",
                "A purchased course can replace a concrete redistribution of time, money, and care.",
                "One family member must lose for another to recover.",
            ],
            balanced_rewrite=(
                "Caregivers need rest, health, and support, while children and dependent people need stable and safe care. "
                "Treat both as joint constraints: specify each person's minimum needs, who carries which responsibility, "
                "what substitute care exists, and how the arrangement will be reviewed after a short trial."
            ),
            verification_questions=[
                "For which ages, health conditions, and family structures is the claim intended?",
                "What needs are non-negotiable for the child or dependent person?",
                "Which responsibilities are explicitly assigned to each caregiver?",
                "What does 'care for yourself' mean operationally: sleep, medical care, protected time, spending, or exit?",
                "Who benefits financially if the claim is accepted?",
                "What seven-day observations would show that the change helped rather than transferred the burden?",
            ],
            reversible_next_steps=[
                "Create a seven-day shared-care schedule with minimum needs and named responsibilities.",
                "Provide each primary caregiver with a protected recovery block and a substitute-care plan.",
                "Record sleep, conflict, child safety, and caregiver function without person-level moral labels.",
                "Review the schedule after seven days and redistribute any newly concentrated burden.",
            ],
            stop_conditions=[
                "Stop the experiment and seek qualified help if child safety, violence, severe neglect, or acute crisis appears.",
                "Do not purchase a high-pressure programme before pricing, evidence, refund terms, and conflicts are visible.",
            ],
        )

    missing = ["The claim's source, scope, counterexamples, and observable falsifiers."]
    if signals["context_compression"].score > 0.28:
        missing.append("The population, time horizon, resource assumptions, affected parties, and exceptions.")
    if signals["incentive_opacity"].score > 0.20:
        missing.append("Pricing, affiliation, refund rights, failure cases, and conflicts of interest.")
    if signals["actionability_hazard"].score > 0.20:
        missing.append("The cost of acting, the safer reversible alternative, and the conditions for stopping.")
    if signals["provenance_weakness"].score > 0.30:
        missing.append("A reconstructable record of origin, edits, source lineage, and AI involvement.")

    return RepairCard(
        useful_core=(
            "The item may contain a useful question, local observation, or partial experience. "
            "That useful core should be preserved while its scope and evidence are tested."
        ),
        missing_conditions=missing,
        affected_parties=[
            "The intended audience",
            "People excluded by the stated assumptions",
            "People who bear downstream cost or risk",
            "The creator, sponsor, distributor, and platform",
        ],
        likely_misreadings=[
            "A conditional observation applies to everyone.",
            "A personal experience establishes general causation.",
            "High confidence or popularity substitutes for evidence.",
            "Disagreement demonstrates ignorance or bad faith.",
        ],
        balanced_rewrite=(
            "Treat this as a conditional claim rather than a universal rule. State who it applies to, the evidence and uncertainty, "
            "credible counterexamples, affected parties, incentives, likely costs, and a small reversible way to test it."
        ),
        verification_questions=[
            "Is this a fact claim, interpretation, value judgment, personal experience, prediction, or sales promise?",
            "Which independent source supports it, and which observation would weaken it?",
            "Who is included and excluded by the claim?",
            "Who gains money, status, attention, or control if the audience believes or shares it?",
            "What is the lowest-risk reversible next step?",
            "How can an affected person appeal, correct, refund, or exit?",
        ],
        reversible_next_steps=[
            "Find one independent source and one serious counterexample.",
            "Add scope, uncertainty, affected parties, and incentive disclosure before sharing.",
            "Run a small time-bounded test rather than a high-cost or irreversible action.",
            "Use a qualified human reviewer for high-stakes health, finance, legal, education, or child-safety claims.",
        ],
        stop_conditions=[
            "Stop if the proposed action creates irreversible risk, suppresses dissent, or lacks a correction path.",
            "Escalate imminent or unlawful harm to an authorized human process rather than relying on this tool.",
        ],
    )
