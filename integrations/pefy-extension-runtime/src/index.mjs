export { classifyTaskRisk, riskAtMost, approvalRequirements } from './policy.mjs';
export { routeTask } from './router.mjs';
export { selectInstructionModules, assembleExecutionEnvelope } from './prompt-assembler.mjs';
export { createTrueForgeClient, streamTrueForgeTurn, trueForgeRuntimePolicy } from './trueforge-adapter.mjs';
export { loadThree, spatialBudget } from './threejs-adapter.mjs';

import { routeTask } from './router.mjs';
import { assembleExecutionEnvelope } from './prompt-assembler.mjs';

export function planOmegaExecution(task = {}, options = {}) {
  const route = routeTask(task, options);
  const envelope = assembleExecutionEnvelope(task, route);
  return { route, envelope };
}
