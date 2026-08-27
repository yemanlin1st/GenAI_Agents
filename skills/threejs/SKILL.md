# Three.js Spatial Visualization Capability

## Status
Approved optional visualization engine for PEFY/MƐTAPEFYON Ω interfaces and project applications when 3D/spatial interaction adds measurable value.

## Initial version
Pin `three` to `0.185.1` for the initial integration baseline. Re-verify the latest supported release before upgrading.

## Intended uses
- infrastructure and network topology
- cyber attack-path and relationship maps
- digital twins
- knowledge graphs
- process and supply-chain visualization
- geospatial/spatial operational views where appropriate
- product configurators and immersive demonstrations
- simulation playback
- training and educational visualizations

## Architecture
Domain data → typed visualization model → worker/streaming adapter → Three.js scene graph → WebGPU when supported / WebGL fallback → interaction and accessibility layer.

Three.js is a presentation/interaction layer, not the source of truth. Business rules, security controls and authoritative state remain outside the scene graph.

## Smart loading policy
Do not load Three.js for ordinary text, forms, tables or low-resource views. Use route-level lazy loading or dynamic imports. Prefer progressive loading and 2D/static fallback when 3D is not available or is not useful.

## Performance rules
- set explicit frame-time and memory budgets per application
- use instancing for repeated objects
- use level of detail for complex scenes
- compress and stream glTF assets where applicable
- avoid unnecessary real-time shadows/post-processing
- pause rendering when the view is hidden or static
- move expensive transforms/data preparation to workers where practical
- dispose geometries, materials, textures and render targets deterministically
- benchmark representative low-end/mobile devices

## Accessibility
Every operational 3D view must expose an equivalent semantic representation for critical information: table, list, tree, textual summary or 2D diagram. Keyboard navigation and reduced-motion preferences must be respected where interaction requires them.

## Security
- never render unsanitized HTML from scene metadata
- validate external asset origins and MIME/content expectations
- apply CSP and trusted asset-hosting policy
- avoid embedding credentials/tokens in asset URLs
- treat imported 3D assets as untrusted supply-chain inputs
- limit resource size and complexity to mitigate denial-of-service through pathological assets

## Data protection
Do not expose confidential topology, customer data, credentials, internal hostnames or security relationships to public/client-side views unless explicitly authorized and appropriately filtered.

## Verification
A Three.js integration is accepted only when it passes functional, accessibility, bundle/performance, memory-leak, browser/device compatibility and security checks, and has a non-3D fallback for critical workflows.
