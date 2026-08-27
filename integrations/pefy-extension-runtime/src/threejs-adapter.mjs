export async function loadThree(options = {}) {
  if (options.lowResource === true) {
    return {
      enabled: false,
      reason: 'low_resource_mode',
      fallback: options.fallback ?? '2d'
    };
  }

  const THREE = await import('three');
  return {
    enabled: true,
    revision: THREE.REVISION,
    module: THREE,
    fallback: options.fallback ?? '2d'
  };
}

export function spatialBudget(options = {}) {
  return Object.freeze({
    lazy_load: true,
    fallback_required: true,
    accessibility_alternative_required: true,
    reduced_motion_supported: true,
    max_initial_bundle_kb: options.maxInitialBundleKb ?? 0,
    max_active_objects: options.maxActiveObjects ?? 5000,
    prefer_instancing_above: options.preferInstancingAbove ?? 250,
    prefer_lod_above: options.preferLodAbove ?? 1000,
    dispose_resources: true
  });
}
