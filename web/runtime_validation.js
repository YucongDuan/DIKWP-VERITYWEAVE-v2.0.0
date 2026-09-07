/* Local-output checks only. This validator cannot attest to external enforcement. */
const VerityWeaveRuntime = (() => {
  'use strict';
  const LOCAL_ACTIONS = new Set([
    'Do not restrict solely for negative tone, criticism, whistleblowing, satire, or distress.',
    'Offer optional source lineage, context, and support without obscuring the item.',
    'Display a high-visibility uncertainty and scope card.',
    'Add a source and context card plus a reversible sharing pause.',
    'Add a source check, context card, and read-before-forwarding pause.',
    'Add scope, source, counterexample, and incentive context.',
    'No restriction is indicated. Preserve the item and keep correction available.'
  ]);
  const LOCAL_LAYERS = new Set(['reader', 'speech', 'none']);
  const EXTERNAL_LAYERS = new Set(['authority', 'correction', 'remedy', 'discovery', 'creator', 'distribution', 'commerce']);
  const PROPOSAL_ACTIONS = new Map([
    ['Prepare a time-bounded lawful safety action with evidence preservation.', 'authority'],
    ['Urgently preserve evidence and route to an authorized human reviewer.', 'authority'],
    ['Propagate a correction to prior recipients and dependent decisions.', 'correction'],
    ['Prepare restoration, verified-loss compensation, and model-revision receipts.', 'remedy'],
    ['Propose a transparent discovery boost for high-integrity public-value content.', 'discovery'],
    ['Offer verification, translation, accessibility, or context-production support.', 'creator'],
    ['Propose a temporary recommendation limit pending independent review.', 'distribution'],
    ['Propose a pause on paid amplification or affiliate conversion until disclosures are complete.', 'commerce'],
    ['Request evidence, conflicts, pricing, refund, failure cases, and scope.', 'creator'],
    ['Propose a time-bounded recommendation limit with notice and appeal.', 'distribution'],
    ['Keep proposed restrictions inactive until an authorized reviewer establishes appeal and correction channels.', 'authority']
  ]);
  const ADVERSE_ACTIONS = new Set([
    'Prepare a time-bounded lawful safety action with evidence preservation.',
    'Propagate a correction to prior recipients and dependent decisions.',
    'Prepare restoration, verified-loss compensation, and model-revision receipts.',
    'Propose a temporary recommendation limit pending independent review.',
    'Propose a pause on paid amplification or affiliate conversion until disclosures are complete.',
    'Propose a time-bounded recommendation limit with notice and appeal.'
  ]);
  const REQUIREMENTS = ['named_human_authority', 'notice', 'reasons', 'evidence_scope', 'expiry', 'appeal', 'correction', 'restoration'];
  const INPUT_NUMBERS = ['price_transparency', 'refund_transparency', 'evidence_quality', 'source_traceability', 'counterevidence_visibility', 'uncertainty_disclosure', 'reach', 'repetition', 'recommendation_intensity', 'creator_power', 'platform_power', 'audience_dependence', 'decision_stakes'];
  const INPUT_BOOLEANS = ['monetized', 'paid_amplification', 'affiliate_or_sales_funnel', 'commercial_conflict_disclosed', 'provenance_manifest_present', 'verified_fabrication', 'verified_harm', 'imminent_harm_or_illegal', 'authorized_human_review', 'creator_notified', 'appeal_available', 'correction_channel_available'];
  const PROTECTED_ROLES = new Set(['criticism', 'whistleblowing', 'distress_expression', 'satire']);
  const FORBIDDEN_FIELDS = new Set(['person_score', 'moral_score', 'moral_worth', 'political_reliability', 'person_intelligence_score', 'viewpoint_penalty', 'sentiment_penalty']);
  const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
  const all = (values, test) => Array.isArray(values) && values.every(test);
  const words = values => all(values, value => typeof value === 'string' && value.trim().length > 0);
  const finiteUnit = value => typeof value === 'number' && Number.isFinite(value) && value >= 0 && value <= 1;
  const equal = (left, right) => JSON.stringify(left) === JSON.stringify(right);
  function report(checks) {
    return {schema_version: '1.0', scope: 'local_generated_output_only', passed: checks.length > 0 && !checks.some(check => check.status === 'FAIL'), checks};
  }
  function check(id, pass, evidence) { return {id, status: pass ? 'PASS' : 'FAIL', evidence: [evidence]}; }
  function boundary(id, evidence) { return {id, status: 'NOT_VERIFIED', evidence: [evidence]}; }
  function noForbiddenFields(value, seen = new Set()) {
    if (!value || typeof value !== 'object') return true;
    if (seen.has(value)) return false;
    seen.add(value);
    const result = Object.entries(value).every(([key, item]) => !FORBIDDEN_FIELDS.has(key) && noForbiddenFields(item, seen));
    seen.delete(value);
    return result;
  }
  function prepareInterventions(interventions, input) {
    let selected = interventions;
    if (input && (input.appeal_available !== true || input.correction_channel_available !== true) && interventions.some(item => ADVERSE_ACTIONS.has(item.action))) {
      selected = interventions.filter(item => !ADVERSE_ACTIONS.has(item.action));
      selected.push({layer: 'authority', action: 'Keep proposed restrictions inactive until an authorized reviewer establishes appeal and correction channels.', automatic: false, reversible: true, expiry_hours: 168, human_gate: true, reason_codes: ['DUE_PROCESS_INCOMPLETE']});
    }
    return selected.map(item => {
      const local = LOCAL_LAYERS.has(item.layer);
      return {...item, scope: local ? 'user_local_recommendation' : 'human_gated_proposal', execution_enabled: false,
        expiry_hours: local ? item.expiry_hours : (item.expiry_hours ?? 168),
        required_before_execution: local ? [] : [...REQUIREMENTS]};
    });
  }
  function validateAnalysisOutput(output, derive) {
    const checks = [];
    const shape = object(output) && object(output.input) && object(output.signals) && Array.isArray(output.worlds) &&
      Array.isArray(output.interventions) && output.interventions.length > 0 && output.interventions.every(object) &&
      words(output.reason_codes) && output.reason_codes.length > 0;
    checks.push(check('analysis_output_shape', shape, 'Analysis input, signals, worlds, reason codes, and every intervention must have the expected shape.'));
    if (!shape) return report(checks);
    const inputShape = typeof output.input.text === 'string' && output.input.text.trim().length > 0 &&
      typeof output.input.content_role === 'string' && typeof output.input.domain === 'string' &&
      INPUT_NUMBERS.every(key => finiteUnit(output.input[key])) && INPUT_BOOLEANS.every(key => typeof output.input[key] === 'boolean') &&
      words(output.input.audience_context) && words(output.input.addictive_features);
    checks.push(check('input_types_and_ranges', inputShape, 'Input flags must be booleans, scalar factors must be finite [0,1] numbers, and declared collections must contain strings. No truthy-string authority flags.'));
    if (!inputShape) return report(checks);
    let expected = null;
    try { expected = derive(output.input); } catch (_) { /* Malformed or unsupported input fails closed below. */ }
    const derived = object(expected) && object(expected.plan) && object(expected.signals);
    checks.push(check('input_recomputable', derived, 'Input is recomputed through the local reference analyzer; supplied validation and invariant flags are ignored.'));
    if (!derived) return report(checks);
    const c = output.input, actions = output.interventions;
    checks.push(check('generated_analysis_matches_input',
      equal(output.signals, expected.signals) && equal(output.worlds, expected.worlds) && equal(output.commons_support, expected.commons) &&
      output.decision === expected.plan.decision && equal(output.reason_codes, expected.plan.reasons) &&
      output.protected_expression === expected.plan.protected && output.high_impact === expected.plan.high &&
      output.semantic_control_potential === Number(expected.plan.scp.toFixed(4)) && output.confidence === expected.confidence,
      'Signals, competing worlds, support result, decision, reasons, control potential, and confidence are recomputed from the saved input.'));
    checks.push(check('interventions_match_generated_plan', equal(actions, prepareInterventions(expected.plan.interventions, c)),
      'The complete action list must match the reference plan, including action wording, gating, scope, expiry, and required safeguards.'));
    checks.push(check('finite_signal_and_world_values',
      Object.values(output.signals).every(signal => object(signal) && finiteUnit(signal.score)) &&
      output.worlds.length > 1 && output.worlds.every(world => object(world) && finiteUnit(world.weight)) &&
      Math.abs(output.worlds.reduce((sum, world) => sum + world.weight, 0) - 1) < 1e-8 && finiteUnit(output.confidence),
      'Scores are finite values in [0,1]; competing-world weights sum to one.'));
    checks.push(check('all_generated_actions_are_nonexecuting', actions.every(action => action.execution_enabled === false),
      'Every generated item is a nonexecuting recommendation or proposal; this page has no external-action executor.'));
    checks.push(check('automatic_actions_are_known_reversible_local_recommendations', actions.every(action =>
      action.automatic !== true || (LOCAL_LAYERS.has(action.layer) && LOCAL_ACTIONS.has(action.action) &&
      action.scope === 'user_local_recommendation' && action.reversible === true && action.human_gate === false)),
      'Each automatic-planning item is individually checked against the local action allowlist and reversibility requirements.'));
    checks.push(check('every_nonlocal_proposal_is_human_gated', actions.every(action => LOCAL_LAYERS.has(action.layer) ||
      (EXTERNAL_LAYERS.has(action.layer) && PROPOSAL_ACTIONS.get(action.action) === action.layer && action.human_gate === true && action.automatic === false && action.reversible === true && action.scope === 'human_gated_proposal')),
      'Every nonlocal proposal must be nonautomatic, reversible, and human-gated; one valid gate cannot cover another unsafe action.'));
    checks.push(check('nonlocal_proposals_have_due_process_requirements', actions.every(action => LOCAL_LAYERS.has(action.layer) ||
      (Number.isFinite(action.expiry_hours) && action.expiry_hours > 0 && all(action.required_before_execution, value => typeof value === 'string') &&
      REQUIREMENTS.every(required => action.required_before_execution.includes(required)) && words(action.reason_codes) && action.reason_codes.length > 0)),
      'Each nonlocal proposal carries finite expiry, reasons, and an explicit pre-execution notice/appeal/correction/restoration checklist. Checklist presence does not prove satisfaction.'));
    const independentBasis = c.verified_harm === true || c.imminent_harm_or_illegal === true || c.verified_fabrication === true;
    const adverse = actions.some(action => ADVERSE_ACTIONS.has(action.action));
    checks.push(check('adverse_proposals_require_declared_appeal_and_correction', !adverse || (c.appeal_available === true && c.correction_channel_available === true),
      'If an appeal or correction channel is absent, adverse proposals are replaced with an inactive due-process hold.'));
    checks.push(check('protected_expression_requires_declared_independent_basis',
      !(PROTECTED_ROLES.has(c.content_role) && adverse && !independentBasis),
      'Protected expression cannot acquire an adverse proposal without a separately declared harm/fabrication basis; the declaration itself is not externally verified.'));
    checks.push(check('negative_affect_is_nonrestrictive_in_this_plan',
      output.signals.negative_affect?.restrictive_feature === false && expected.negativeAffectDecision === expected.plan.decision &&
      expected.negativeAffectControlPotential === expected.plan.scp,
      'A local counterfactual sets the negative-affect score to zero; decision and control potential must remain unchanged.'));
    const deception = output.worlds.find(world => world.key === 'coordinated_deception');
    checks.push(check('no_unverified_deliberate_deception_finding', c.verified_fabrication === true ||
      (!!deception && deception.weight < 0.15 && !/DELIBERATE_DECEPTION|COORDINATED_DECEPTION/.test(output.decision)),
      'Without separately declared fabrication, the local result must not present deliberate deception as a finding. World weights are heuristic decision weights, not probabilities.'));
    checks.push(check('generated_output_has_no_person_or_viewpoint_score_fields', noForbiddenFields({signals: output.signals, worlds: output.worlds, interventions: actions, result: Object.fromEntries(Object.entries(output).filter(([key]) => !['input', 'validation', 'invariants'].includes(key)))}),
      'Generated result fields are traversed for explicit person-worth and viewpoint/sentiment penalty scores; input quotations are excluded. This is not a universal fairness proof.'));
    checks.push(boundary('policy_wide_fairness_and_moral_scoring_prohibitions', 'Policy intentions cannot be proven across all inputs or future implementations by this finite local validator.'));
    checks.push(boundary('independent_evidence_and_named_authority', 'The page cannot verify input declarations, reviewer identity, lawful authority, notice delivery, appeal availability, or real restoration.'));
    checks.push(boundary('external_enforcement', 'No platform, operating-system, account, payment, deletion, or lineage control is enforced by this standalone page.'));
    return report(checks);
  }
  function validateOrThrow(output, derive) {
    const validation = validateAnalysisOutput(output, derive);
    output.validation = validation;
    output.invariants = Object.fromEntries(validation.checks.filter(item => item.status !== 'NOT_VERIFIED').map(item => [item.id, item.status === 'PASS']));
    if (!validation.passed) {
      const error = new Error('Runtime validation failed. Result rendering and exports are blocked; no action has been executed.');
      error.validation = validation;
      throw error;
    }
    return output;
  }
  function validateAppeal(appeal, receiptTypes) {
    const valid = object(appeal) && Array.isArray(appeal.correction_receipts) && appeal.correction_receipts.every(item =>
      object(item) && receiptTypes.includes(item.type) && typeof item.evidence === 'string' && item.evidence.trim().length > 0);
    const present = new Set(valid ? appeal.correction_receipts.map(item => item.type) : []);
    const missing = receiptTypes.filter(type => !present.has(type));
    return {valid, missing, complete: valid && missing.length === 0, validation: report([
      check('local_receipt_structure', valid, 'Every recorded receipt must have a known type and nonempty evidence text.'),
      check('local_receipt_checklist_complete', valid && missing.length === 0, `Missing receipt categories: ${missing.join(', ') || 'none'}.`),
      boundary('real_world_restoration_and_reuse_control', 'Receipt text is user-declared. Real correction, compensation, delivery, and external reuse blocking are not verified or enforced here.')
    ])};
  }
  return {prepareInterventions, validateAnalysisOutput, validateOrThrow, validateAppeal};
})();
if (typeof module !== 'undefined' && module.exports) module.exports = VerityWeaveRuntime;
