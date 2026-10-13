// Webpack entry point for module federation.
// The import needs to be kept dynamic (async boundary for shared modules)
// and is exported as default: the Patternslib Module Federation helper
// (@patternslib/dev >= 4.1) awaits it, so the host's initial DOM scan runs
// only after the patterns and components of this bundle are registered.
export default import("./bundle");
