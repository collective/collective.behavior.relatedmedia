import { BasePattern } from "@patternslib/patternslib/src/core/basepattern";
import Parser from "@patternslib/patternslib/src/core/parser";
import registry from "@patternslib/patternslib/src/core/registry";
import { Fancybox } from "@fancyapps/ui";
import $ from "jquery";
import "slick-carousel";

// import tinymce plugin code
// the plugin is called in another script registered in "custom_plugins"
// see profiles/default/registry.xml
import "../relatedimages-gallery/related-images-gallery";

export const parser = new Parser("related-images");
parser.addArgument("uuids", "");
parser.addArgument("slickSliderOptions");

class Pattern extends BasePattern {
    static name = "related-images";
    static trigger = ".pat-related-images";
    static parser = parser;

    async init() {
        import("./related-images.scss");

        await this.uploader_event();
        await this.load_gallery();
        await this.init_fancybox();
    }

    async init_fancybox() {
        Fancybox.bind("[data-fancybox]", {
            // prevent window reload on close
            Hash: false,
        });
    }

    async
    async uploader_event() {
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

    async load_gallery() {
        const uuids = this.options?.uuids;
        const base_url = document.querySelector("body").dataset.baseUrl;
        const req = new Request(`${base_url}/@@relatedImages?uuids=${uuids}&showGallery=1&ajax_load=${new Date().getTime()}`);
        fetch(req)
            .then((response) => response.text())
            .then(async (text) => {
                this.el.innerHTML = text;
                await this.init_slick(this.el);
                registry.scan(this.el);
                // trigger fancybox
                await this.init_fancybox();
            });
    }

    async init_slick(el) {
        let slickOptions = {
            infinite: false,
            slidesToShow: 1,
            centerMode: false,
            variableWidth: true,
            prevArrow: el.querySelector(".related-images-slider .slider-prev"),
            nextArrow: el.querySelector(".related-images-slider .slider-next"),
            ...(this.options.slickSliderOptions || {})
        }
        $(".related-images-slider .slick-slider", $(this.el)).slick(slickOptions);
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
