import { BasePattern } from "@patternslib/patternslib/src/core/basepattern";
import Parser from "@patternslib/patternslib/src/core/parser";
import registry from "@patternslib/patternslib/src/core/registry";

export const parser = new Parser("related-images");
parser.addArgument("uuids", "");

class Pattern extends BasePattern {
    static name = "related-images";
    static trigger = ".pat-related-images";
    static parser = parser;

    async init() {
        import("./related-images.scss");

        await this.uploader_event();

        // The options are automatically created, if parser is defined.
        this.el.innerHTML = `
            <pre class="text-muted">will replace ${this.options.uuids} with image gallery soon !</pre>
        `;
    }

    async uploader_event() {
        const $ = (await import("jquery")).default;

        $(".pat-upload").on("uploadAllCompleted", function (response, path) {
            // reload viewlets on upload
            var base_url = $(this).data("relmedia-baseurl");
            var $relimages = $("#related-images");
            if ($relimages.length) {
                $.ajax({
                    url: base_url + "/@@relatedImages",
                    success: function (response) {
                        $relimages.replaceWith($(response).siblings("#related-images"));
                    }
                });
            }
            var $relatts = $("#related-attachments");
            if ($relatts.length) {
                $.ajax({
                    url: base_url + "/@@relatedAttachments",
                    success: function (response) {
                        $relatts.replaceWith($(response).find("#related-attachments"));
                    }
                });
            }
        });
    }
}


// Register Pattern class in the global pattern registry and make it usable there.
registry.register(Pattern);

// Export Pattern as default export.
// You can import it as ``import AnyName from "./related-images";``
export default Pattern;
// Export BasePattern as named export.
// You can import it as ``import { Pattern } from "./related-images";``
export { Pattern };
