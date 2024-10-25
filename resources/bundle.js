import registry from "@patternslib/patternslib/src/core/registry";

import "./pat-related-images/related-images";

// Register Fancybox gloablly
async function register_global_libraries() {
    // Register Fancybox globally
    const Fancybox = (await import("@fancyapps/ui")).Fancybox;
    window.Fancybox = Fancybox;
}
register_global_libraries();


registry.init();
