/* global tinymce:true */

let PloneModal = null;

window.tinymce.PluginManager.add('relatedimagesgallery', (editor, url) => {

    const openGalleryEditor = (editor) => {
        const tiny_instance = document.getElementById(editor.id)["pattern-tinymce"].instance.tiny;
        // create new or reuse existing gallery wrapper
        let curr_node = tiny_instance.selection.getNode(), gal_wrapper;
        if(!curr_node.classList.contains("pat-related-images")) {
            gal_wrapper = tiny_instance.dom.create(
                "div",
                {"class": "pat-related-images"},
            );
            if(curr_node.innerText.trim() === "") {
                tiny_instance.dom.replace(gal_wrapper, curr_node);
            } else {
                tiny_instance.dom.insertAfter(gal_wrapper, curr_node.previousElementSibling);
            }
            curr_node = gal_wrapper;
        } else {
            gal_wrapper = curr_node;
        }
        // determine uuid filtering
        const data = gal_wrapper.dataset.patRelatedImages || "";
        let uuids = "";
        if(data.indexOf("uuids:") !== -1) {
            uuids = data.split(":")[1].trim();
        }
        const PloneModal = window.__patternslib_registry["plone-modal"];
        const $el = $("<div />").appendTo("body");
        const gallery_modal = new PloneModal($el, {
            ajaxUrl: `./@@gallery-editor?${uuids ? "uuids=" + uuids + "&": ""}ajax_load=${new Date().getTime()}`,
            modalSizeClass: "modal-xl",
            position:"center top",
            backdropOptions: {
                zIndex: "2000",
            },
            actionOptions: {
                modalFunction: "insertOrUpdateGallery",
            }
        });
        gallery_modal.insertOrUpdateGallery = () => {
            // collect active images
            let checked = [];
            const checkboxes = gallery_modal.$modalContent[0].querySelectorAll("input[type=checkbox]");
            checkboxes.forEach((e) => {
                if(e.checked) {
                    checked.push(e.value);
                }
            });
            if(0 < checked.length < checkboxes.length) {
                gal_wrapper.dataset.patRelatedImages = `uuids:${checked.join(",")}`;
                let gal_preview = "";
                for(const uuid of checked) {
                    gal_preview += `<img src="./resolveuid/${uuid}/@@images/image/thumb" class="related-gallery-editor-preview" style="display:inline-block;margin:1rem" />`;
                }
                gal_wrapper.innerHTML = gal_preview;
            } else {
                gal_wrapper.dataset.patRelatedImages = null;
                gal_wrapper.innerHTML = `<img src="++plone++static/icons-bootstrap/images.svg" width="50" height="50">`;
            }
            gallery_modal.hide();
        };
        gallery_modal.show();
    };

    // add plugin code here
    editor.ui.registry.addButton("relatedimagesgallery", {
        icon: "gallery",
        tooltip: "Insert/edit related image gallery",
        onAction: () => {
            openGalleryEditor(editor);
        },
    });
    editor.ui.registry.addMenuItem("relatedimagesgallery", {
        icon: "gallery",
        text: "Insert/edit related image gallery",
        onAction: () => {
            openGalleryEditor(editor);
        },
    });
});
