#!/usr/bin/env node
'use strict';
// Dependency-free Node >=18 regression tests of the actual offline HTML analyzer.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {webcrypto} = require('node:crypto');
const root = path.resolve(__dirname, '..');
const filename = 'DIKWP_VERITYWEAVE_SEMANTIC_RESILIENCE_GRID_OS_v2.0.0.html';
const html = fs.readFileSync(path.join(root, filename), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const code = script.slice(0, script.indexOf("\ndocument.querySelectorAll('.tab')"));
const sandbox = {window: {crypto: webcrypto}, crypto: webcrypto, TextEncoder, console,
  semanticResult: {innerHTML: ''}, commonsResult: {innerHTML: ''}, interopPreview: {textContent: ''},
  alert: () => {}, document: {querySelector: () => ({focus: () => {}})}};
vm.createContext(sandbox);
vm.runInContext(code, sandbox, {filename});
const runtime = vm.runInContext('VerityWeaveRuntime', sandbox);
const clone = value => JSON.parse(JSON.stringify(value));
const baseInput = {
  case_id: 'browser-invariant-regression', text: 'Context and evidence should remain open to correction.',
  language: 'en', domain: 'general', content_role: 'advice', channel: 'post', dikwp_source_position: 'I', dikwp_target_position: 'P',
  audience_context: [], source_links: [], counterevidence: [], known_outcomes: [], monetized: false, paid_amplification: false,
  affiliate_or_sales_funnel: false, commercial_conflict_disclosed: true, price_transparency: 0.8, refund_transparency: 0.8,
  evidence_quality: 0.8, source_traceability: 0.8, counterevidence_visibility: 0.8, uncertainty_disclosure: 0.8,
  provenance_manifest_present: true, reach: 0.2, repetition: 0.2, recommendation_intensity: 0.2, creator_power: 0.2,
  platform_power: 0.2, audience_dependence: 0.2, decision_stakes: 0.2, ai_origin: 'unknown', addictive_features: [],
  verified_fabrication: false, verified_harm: false, imminent_harm_or_illegal: false, authorized_human_review: false,
  creator_notified: false, appeal_available: true, correction_channel_available: true, notes: ''
};
let collected = 0, passed = 0, failed = 0;
async function test(name, run) {
  collected += 1;
  try { await run(); passed += 1; console.log(`PASS ${name}`); }
  catch (error) { failed += 1; console.error(`FAIL ${name}: ${error.stack || error}`); }
}
function rejects(output, mutate, checkId) {
  const value = clone(output); mutate(value);
  value.invariants = {all_checks_passed: true}; value.validation = {passed: true, checks: []};
  const report = sandbox.validateAnalysisOutput(value);
  assert.equal(report.passed, false);
  if (checkId) assert.equal(report.checks.find(item => item.id === checkId)?.status, 'FAIL');
  assert.throws(() => runtime.validateOrThrow(value, sandbox.deriveValidationReference), /Runtime validation failed/);
}
(async () => {
  const baseline = await sandbox.analyzeCase(clone(baseInput));
  const adverse = await sandbox.analyzeCase({...clone(baseInput), verified_harm: true});
  await test('all four offline HTML copies are byte-identical', () => {
    for (const relative of [`web/${filename}`, `src/dikwp_verityweave/data/${filename}`, 'src/dikwp_verityweave/data/standalone.html'])
      assert.equal(fs.readFileSync(path.join(root, relative), 'utf8'), html, relative);
  });
  await test('embedded validator matches reviewable JavaScript source', () => {
    assert.ok(script.includes(fs.readFileSync(path.join(root, 'web/runtime_validation.js'), 'utf8').trim()));
    assert.doesNotMatch(html, /<script\b[^>]*\bsrc\s*=/i);
  });
  await test('generated report uses structured local checks and explicit unverified boundaries', () => {
    assert.equal(baseline.validation.schema_version, '1.0');
    assert.equal(baseline.validation.scope, 'local_generated_output_only');
    assert.equal(baseline.validation.passed, true);
    assert.ok(baseline.validation.checks.some(item => item.status === 'NOT_VERIFIED' && item.id === 'external_enforcement'));
    assert.ok(baseline.validation.checks.every(item => item.evidence.length > 0));
    assert.ok(Object.values(baseline.invariants).every(value => typeof value === 'boolean'));
    assert.equal(baseline.invariants.external_enforcement, undefined);
  });
  await test('cached invariant success cannot hide a modified signal', () => rejects(baseline, value => {value.signals.evidence_deficit.score = 0.99;}, 'generated_analysis_matches_input'));
  await test('in-range confidence tampering is rejected', () => rejects(baseline, value => {value.confidence = 0.1234;}, 'generated_analysis_matches_input'));
  await test('self-assessment counts are explicitly not test results', () => {
    assert.match(html, /source-level author claims, not test PASS counts/);
    assert.match(html, /4<\/b><span>proposal-only controls/);
    assert.doesNotMatch(html, /50<\/b><span>implemented/);
  });
  await test('unknown automatic action is rejected', () => rejects(baseline, value => {value.interventions[0].action = 'Delete the account.'; value.interventions[0].automatic = true;}, 'automatic_actions_are_known_reversible_local_recommendations'));
  await test('valid human gate cannot cover another ungated adverse action', () => rejects(adverse, value => {value.interventions[1].human_gate = false;}, 'every_nonlocal_proposal_is_human_gated'));
  await test('automatic external proposal is rejected', () => rejects(adverse, value => {value.interventions[0].automatic = true;}, 'every_nonlocal_proposal_is_human_gated'));
  await test('execution enablement is rejected', () => rejects(baseline, value => {value.interventions[0].execution_enabled = true;}, 'all_generated_actions_are_nonexecuting'));
  await test('irreversible proposal is rejected', () => rejects(adverse, value => {value.interventions[0].reversible = false;}, 'every_nonlocal_proposal_is_human_gated'));
  await test('missing appeal checklist requirement is rejected', () => rejects(adverse, value => {value.interventions[0].required_before_execution = ['named_human_authority'];}, 'nonlocal_proposals_have_due_process_requirements'));
  await test('nonfinite expiry is rejected', () => rejects(adverse, value => {value.interventions[0].expiry_hours = Infinity;}, 'nonlocal_proposals_have_due_process_requirements'));
  await test('person moral scoring field is rejected', () => rejects(baseline, value => {value.person_score = 0.2;}, 'generated_output_has_no_person_or_viewpoint_score_fields'));
  await test('world weight tampering is rejected', () => rejects(baseline, value => {value.worlds[0].weight = NaN;}, 'finite_signal_and_world_values'));
  await test('malformed action object is rejected', () => rejects(baseline, value => {value.interventions = [null];}, 'analysis_output_shape'));
  await test('truthy string authority input is rejected', () => rejects(baseline, value => {value.input.authorized_human_review = 'false';}, 'input_types_and_ranges'));
  await test('out-of-range input factor is rejected', () => rejects(baseline, value => {value.input.evidence_quality = 2;}, 'input_types_and_ranges'));
  await test('protected distress preserves expression and negative affect remains nonrestrictive', async () => {
    const output = await sandbox.analyzeCase({...clone(baseInput), content_role: 'distress_expression', text: 'I am sad and angry. I feel hopeless and exhausted.'});
    assert.equal(output.decision, 'PRESERVE_ADVERSE_TRUTH_OR_DISTRESS');
    assert.equal(output.signals.negative_affect.restrictive_feature, false);
    assert.equal(output.validation.checks.find(item => item.id === 'negative_affect_is_nonrestrictive_in_this_plan').status, 'PASS');
  });
  await test('no appeal channel suppresses adverse proposals', async () => {
    const output = await sandbox.analyzeCase({...clone(baseInput), verified_harm: true, appeal_available: false});
    assert.ok(output.interventions.some(item => item.reason_codes.includes('DUE_PROCESS_INCOMPLETE')));
    assert.ok(!output.interventions.some(item => ['correction', 'remedy'].includes(item.layer)));
    assert.equal(output.validation.passed, true);
  });
  await test('no correction channel suppresses adverse proposals', async () => {
    const output = await sandbox.analyzeCase({...clone(baseInput), verified_harm: true, correction_channel_available: false});
    assert.ok(output.interventions.some(item => item.reason_codes.includes('DUE_PROCESS_INCOMPLETE')));
    assert.equal(output.validation.passed, true);
  });
  await test('unsafe actions from a faulty generator fail closed too', async () => {
    sandbox.savedPlan = sandbox.plan;
    vm.runInContext("plan=(...args)=>{const result=savedPlan(...args);result.interventions[0].action='Delete the account.';result.interventions[0].automatic=true;return result}", sandbox);
    try { await assert.rejects(sandbox.analyzeCase(clone(baseInput)), /Runtime validation failed/); }
    finally {sandbox.plan = sandbox.savedPlan;}
  });
  await test('rendering displays local scope and NOT_VERIFIED evidence', () => {
    sandbox.renderAnalysis(baseline);
    assert.match(sandbox.semanticResult.innerHTML, /NOT_VERIFIED/);
    assert.match(sandbox.semanticResult.innerHTML, /external enforcement remain unverified/);
    assert.doesNotMatch(sandbox.semanticResult.innerHTML, />Runtime invariants</);
  });
  await test('rendering rejects a tampered stored result', () => {
    const result = clone(adverse); result.interventions[0].automatic = true;
    assert.throws(() => sandbox.renderAnalysis(result), /Runtime validation failed/);
  });
  await test('analysis export revalidates and blocks tampered state', () => {
    sandbox.exportCount = 0;
    vm.runInContext('download=()=>{exportCount+=1}', sandbox);
    sandbox.badResult = clone(adverse); sandbox.badResult.interventions[0].automatic = true;
    vm.runInContext('currentAnalysis=badResult;exportAnalysis("json");exportInterop("dsa")', sandbox);
    assert.equal(sandbox.exportCount, 0);
  });
  await test('workspace export revalidates and blocks tampered state', () => {
    vm.runInContext('exportWorkspace()', sandbox);
    assert.equal(sandbox.exportCount, 0);
  });
  await test('Markdown exports preserve validation boundaries', () => {
    const text = sandbox.analysisMarkdown(baseline);
    assert.match(text, /Recomputed local validation/);
    assert.match(text, /external_enforcement: NOT_VERIFIED/);
  });
  await test('empty or unknown appeal receipts cannot establish closure', () => {
    const expected = ['RESTORE', 'CORRECT'];
    assert.equal(runtime.validateAppeal({correction_receipts: [{type: 'RESTORE', evidence: ''}, {type: 'CORRECT', evidence: 'done'}]}, expected).complete, false);
    assert.equal(runtime.validateAppeal({correction_receipts: [{type: 'RESTORE', evidence: 'done'}, {type: 'OTHER', evidence: 'done'}]}, expected).complete, false);
  });
  await test('receipt checklist completeness is not external restoration proof', () => {
    const result = runtime.validateAppeal({status: 'CORRECTION_CLOSED', correction_receipts: [{type: 'RESTORE', evidence: 'User-declared supporting receipt'}]}, ['RESTORE']);
    assert.equal(result.complete, true);
    assert.equal(result.validation.checks.find(item => item.id === 'real_world_restoration_and_reuse_control').status, 'NOT_VERIFIED');
  });
  const presets = vm.runInContext('presets', sandbox);
  const fields = {evidence:'evidence_quality',traceability:'source_traceability',counter:'counterevidence_visibility',uncertainty:'uncertainty_disclosure',price:'price_transparency',refund:'refund_transparency',reach:'reach',repetition:'repetition',recommendation:'recommendation_intensity',creatorPower:'creator_power',platformPower:'platform_power',audienceDependence:'audience_dependence',stakes:'decision_stakes'};
  for (const [name, preset] of Object.entries(presets)) await test(`offline preset ${name} satisfies local checks`, async () => {
    const input = {...clone(baseInput),text:preset.text,domain:preset.domain,content_role:preset.role,channel:preset.channel,
      audience_context:preset.audience.split(',').map(value=>value.trim()).filter(Boolean),monetized:preset.monetized,paid_amplification:preset.paid,
      affiliate_or_sales_funnel:preset.funnel,commercial_conflict_disclosed:preset.conflict,provenance_manifest_present:preset.provenance,
      appeal_available:preset.appeal,correction_channel_available:preset.correction,addictive_features:preset.addictive};
    for (const [key,value] of Object.entries(preset.values)) input[fields[key]] = value;
    assert.equal((await sandbox.analyzeCase(input)).validation.passed, true);
  });
  console.log('DIKWP_SUITE_RESULT='+JSON.stringify({collected,passed,failed,skipped:0}));
  process.exitCode = failed ? 1 : 0;
})().catch(error => {console.error(error);console.log('DIKWP_SUITE_RESULT='+JSON.stringify({collected,passed,failed:failed+1,skipped:0}));process.exitCode=1;});
