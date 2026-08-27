const RISK_ORDER = Object.freeze({ low: 0, medium: 1, high: 2, critical: 3 });

export function classifyTaskRisk(task = {}) {
  const signals = new Set(task.signals ?? []);
  let score = 0;

  if (signals.has('external_write')) score += 2;
  if (signals.has('production')) score += 3;
  if (signals.has('credentials')) score += 2;
  if (signals.has('personal_data')) score += 2;
  if (signals.has('regulated')) score += 2;
  if (signals.has('privileged_execution')) score += 3;
  if (signals.has('irreversible')) score += 3;
  if (signals.has('financial_commitment')) score += 2;
  if (signals.has('security_control_change')) score += 3;

  const risk = score >= 7 ? 'critical' : score >= 4 ? 'high' : score >= 2 ? 'medium' : 'low';
  return { risk, score, signals: [...signals].sort() };
}

export function riskAtMost(actual, ceiling) {
  if (!(actual in RISK_ORDER) || !(ceiling in RISK_ORDER)) {
    throw new Error(`Unknown risk level: actual=${actual}, ceiling=${ceiling}`);
  }
  return RISK_ORDER[actual] <= RISK_ORDER[ceiling];
}

export function approvalRequirements(task = {}, riskResult = classifyTaskRisk(task)) {
  const approvals = new Set();
  const signals = new Set(task.signals ?? []);

  if (riskResult.risk === 'critical') approvals.add('human_change_authority');
  if (signals.has('production')) approvals.add('production_owner');
  if (signals.has('credentials')) approvals.add('credential_owner');
  if (signals.has('privileged_execution')) approvals.add('security_authority');
  if (signals.has('irreversible')) approvals.add('two_person_review');
  if (signals.has('financial_commitment')) approvals.add('financial_authority');

  return [...approvals].sort();
}
