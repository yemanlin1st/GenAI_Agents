import test from 'node:test';
import assert from 'node:assert/strict';
import {
  classifyTaskRisk,
  routeTask,
  planOmegaExecution,
  trueForgeRuntimePolicy,
  loadThree
} from '../src/index.mjs';

test('simple task remains direct', () => {
  const plan = planOmegaExecution({ objective: 'summarize a stable document' });
  assert.equal(plan.route.primary, 'direct_reasoning');
  assert.equal(plan.route.execution_mode, 'direct');
  assert.equal(plan.envelope.supervisor, 'METAPEFYON_OMEGA');
});

test('agentic task routes to subordinate harness', () => {
  const route = routeTask({ features: ['long_running_agent', 'sandbox'] });
  assert.equal(route.primary, 'trueforge');
  assert.equal(route.execution_mode, 'supervised_harness');
});

test('critical production task is approval gated', () => {
  const task = { signals: ['production', 'privileged_execution', 'irreversible'] };
  const risk = classifyTaskRisk(task);
  const route = routeTask(task);
  assert.equal(risk.risk, 'critical');
  assert.equal(route.execution_mode, 'approval_gated_sandbox');
  assert.ok(route.approvals.includes('human_change_authority'));
  assert.ok(route.approvals.includes('two_person_review'));
});

test('spatial task gets Three.js augmentation', () => {
  const route = routeTask({ features: ['digital_twin'] });
  assert.deepEqual(route.augmentations, ['threejs']);
});

test('low-resource mode suppresses optional Three.js route', () => {
  const route = routeTask({ features: ['digital_twin', 'low_resource'] });
  assert.deepEqual(route.augmentations, []);
});

test('TrueForge runtime policy forbids default bypass', () => {
  const policy = trueForgeRuntimePolicy();
  assert.equal(policy.permission_bypass_default, false);
  assert.equal(policy.shared_deployment_requires_explicit_approval, true);
});

test('Three.js can be skipped without importing runtime in low-resource mode', async () => {
  const result = await loadThree({ lowResource: true });
  assert.equal(result.enabled, false);
  assert.equal(result.fallback, '2d');
});

test('execution envelope includes mandatory governance modules', () => {
  const { envelope } = planOmegaExecution({ features: ['fable_structure'] });
  assert.ok(envelope.policy.instruction_modules.includes('sovereign_constitution'));
  assert.ok(envelope.policy.instruction_modules.includes('fable5_structure_adapter'));
  assert.equal(envelope.policy.no_runtime_impersonation, true);
  assert.equal(envelope.policy.no_default_permission_bypass, true);
});
