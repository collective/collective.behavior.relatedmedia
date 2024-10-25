import registry from "@patternslib/patternslib/src/core/registry";

import "./pat-related-images/related-images";

// Register Fancybox globally
async function register_global_libraries() {
    const Fancybox = (await import("@fancyapps/ui")).Fancybox;
    window.Fancybox = Fancybox;
}
register_global_libraries();


registry.init();
