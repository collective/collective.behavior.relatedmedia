import registry from "@patternslib/patternslib/src/core/registry";
import plone_registry from "@plone/registry";

// Register Fancybox globally and bind it to the related images.
// The images viewlet renders plain ``<a data-fancybox="relatedImages">``
// links without the pat-related-images wrapper (that one is only used by
// the TinyMCE gallery), so the lightbox has to be bound here.
async function register_global_libraries() {
    if(!window.Fancybox) {
        const Fancybox = (await import("@fancyapps/ui")).Fancybox;
        window.Fancybox = Fancybox;
    }
    await import("@fancyapps/ui/dist/fancybox/fancybox.css");
    window.Fancybox.bind("[data-fancybox]", {
        // prevent window reload on close
        Hash: false,
    });
}
register_global_libraries();

// register custom `pat-contentbrowser` components
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
