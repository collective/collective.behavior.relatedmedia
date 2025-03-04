import registry from "@patternslib/patternslib/src/core/registry";
import plone_registry from "@plone/registry";

// Register Fancybox globally
async function register_global_libraries() {
    if(!window.Fancybox) {
        // Register Bootstrap globally
        const Fancybox = (await import("@fancyapps/ui")).Fancybox;
        window.Fancybox = Fancybox;
    }
}
register_global_libraries();

// register custon `pat-contentbrowser` components
async function register_selecteditem_component() {
    // we register our component to a custom keyname, which is used
    // in the "RelatedImagesWidget" pattern_options.
    // see collective/behavior/relatedmedia/behavior.py
    const SelectedImages = (await import("./pat-related-images/components/SelectedImages.svelte")).default;
    plone_registry.registerComponent({
        name: "pat-contentbrowser.relatedimages.SelectedItem",
        component: SelectedImages,
    });
    const SelectedAttachments = (await import("./pat-related-images/components/SelectedAttachments.svelte")).default;
    plone_registry.registerComponent({
        name: "pat-contentbrowser.relatedattachments.SelectedItem",
        component: SelectedAttachments,
    });
}
register_selecteditem_component();

import "./pat-related-images/related-images";

registry.init();
