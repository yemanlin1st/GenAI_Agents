const CORE_MODULES = Object.freeze([
  'sovereign_constitution',
  'runtime_identity_truth',
  'epistemic_freshness',
  'task_risk_classifier',
  'output_contract',
  'safety_compliance_trust',
  'observability_evidence',
  'resilience_recovery'
]);

const FEATURE_MODULES = Object.freeze({
  long_running_agent: ['trueforge_harness_adapter'],
  session_persistence: ['trueforge_harness_adapter'],
  mcp_tools: ['trueforge_harness_adapter'],
  sandbox: ['trueforge_harness_adapter'],
  subagents: ['trueforge_harness_adapter'],
  agentic_coding: ['trueforge_harness_adapter'],
  trajectory_analysis: ['deepseek_harness'],
  '3d': ['threejs_spatial_visualization'],
  digital_twin: ['threejs_spatial_visualization'],
  topology: ['threejs_spatial_visualization'],
  spatial_graph: ['threejs_spatial_visualization'],
  simulation: ['threejs_spatial_visualization'],
  fable_structure: ['fable5_structure_adapter']
});

export function selectInstructionModules(task = {}, route = {}) {
  const selected = new Set(CORE_MODULES);
  for (const feature of task.features ?? []) {
    for (const moduleName of FEATURE_MODULES[feature] ?? []) selected.add(moduleName);
  }
  if (route.primary === 'trueforge') selected.add('trueforge_harness_adapter');
  if ((route.augmentations ?? []).includes('threejs')) selected.add('threejs_spatial_visualization');
  return [...selected];
}

export function assembleExecutionEnvelope(task = {}, route = {}) {
  const modules = selectInstructionModules(task, route);
  return {
    schema: 'pefy.omega.execution-envelope/v1',
    supervisor: route.supervisor ?? 'METAPEFYON_OMEGA',
    task: {
      id: task.id ?? null,
      objective: task.objective ?? '',
      domain: task.domain ?? 'general',
      features: [...(task.features ?? [])],
      signals: [...(task.signals ?? [])]
    },
    policy: {
      instruction_modules: modules,
      precedence: [
        'sovereign_constitution',
        'runtime_identity_truth',
        'task_risk_classifier',
        'safety_compliance_trust',
        'epistemic_freshness',
        'tool_and_approval_policy',
        'context_memory_policy',
        'orchestration_harness_routing',
        'domain_specific_skills',
        'output_contract',
        'observability_evidence',
        'resilience_recovery'
      ],
      no_runtime_impersonation: true,
      no_default_permission_bypass: true,
      least_privilege: true,
      evidence_required_for_completion_claims: true
    },
    execution: {
      primary: route.primary ?? 'direct_reasoning',
      augmentations: [...(route.augmentations ?? [])],
      mode: route.execution_mode ?? 'direct',
      approvals: [...(route.approvals ?? [])],
      risk: route.risk ?? null
    }
  };
}
