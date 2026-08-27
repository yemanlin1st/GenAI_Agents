import { classifyTaskRisk, approvalRequirements } from './policy.mjs';

const SPATIAL = new Set(['3d', 'digital_twin', 'topology', 'spatial_graph', 'simulation']);
const HARNESS = new Set(['long_running_agent', 'session_persistence', 'mcp_tools', 'sandbox', 'subagents', 'streaming', 'agentic_coding', 'trajectory_analysis']);

export function routeTask(task = {}, options = {}) {
  const features = new Set(task.features ?? []);
  const risk = classifyTaskRisk(task);
  const approvals = approvalRequirements(task, risk);
  const route = {
    supervisor: 'METAPEFYON_OMEGA',
    primary: 'direct_reasoning',
    augmentations: [],
    risk,
    approvals,
    execution_mode: 'direct',
    reasons: []
  };

  if ([...features].some((f) => SPATIAL.has(f))) {
    route.augmentations.push('threejs');
    route.reasons.push('spatial capability requested');
  }

  const needsHarness = [...features].some((f) => HARNESS.has(f));
  if (needsHarness) {
    const preferred = options.preferredHarness ?? 'trueforge';
    route.primary = preferred;
    route.execution_mode = risk.risk === 'critical' ? 'approval_gated_sandbox' : 'supervised_harness';
    route.reasons.push(`harness features requested; selected ${preferred}`);
  }

  if (risk.risk === 'critical') {
    route.execution_mode = 'approval_gated_sandbox';
    route.reasons.push('critical-risk execution cannot run directly');
  } else if (risk.risk === 'high' && route.execution_mode === 'direct') {
    route.execution_mode = 'supervised_tools';
    route.reasons.push('high-risk task requires supervised execution');
  }

  if (features.has('low_resource')) {
    route.augmentations = route.augmentations.filter((x) => x !== 'threejs');
    route.reasons.push('low-resource mode suppresses optional 3D runtime');
  }

  return route;
}
