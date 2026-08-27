function isLoopback(urlString) {
  const url = new URL(urlString);
  return ['127.0.0.1', 'localhost', '::1'].includes(url.hostname);
}

export async function createTrueForgeClient(options = {}) {
  const baseUrl = options.baseUrl ?? process.env.TRUEFORGE_BASE_URL ?? 'http://127.0.0.1:8000';
  const token = options.token ?? process.env.TRUEFORGE_TOKEN;
  const allowSharedDeployment = options.allowSharedDeployment === true;

  if (!isLoopback(baseUrl) && !allowSharedDeployment) {
    throw new Error('Non-loopback TrueForge endpoints require explicit shared-deployment approval.');
  }

  const { TrueForge } = await import('@truefoundry/trueforge-sdk');
  return new TrueForge({
    baseUrl,
    ...(token ? { token } : {})
  });
}

export async function streamTrueForgeTurn({ sessionId, request = {}, clientOptions = {} }) {
  if (!sessionId) throw new Error('sessionId is required');
  const client = await createTrueForgeClient(clientOptions);
  return client.sessions.createTurnStream(sessionId, request);
}

export function trueForgeRuntimePolicy() {
  return Object.freeze({
    authority: 'subordinate_to_METAPEFYON_OMEGA',
    local_default: true,
    shared_deployment_requires_explicit_approval: true,
    production_write_requires_change_control: true,
    credentials_from_environment_only: true,
    permission_bypass_default: false
  });
}
