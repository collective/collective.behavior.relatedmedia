import registry from "@patternslib/patternslib/src/core/registry";

import "./pat-related-images/related-images";

registry.init();

// Register Fancybox globally
async function register_global_libraries() {
    if(!window.Fancybox) {
        // Register Bootstrap globally
        const Fancybox = (await import("@fancyapps/ui")).Fancybox;
        window.Fancybox = Fancybox;
    }
}
register_global_libraries();
