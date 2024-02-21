/* global tinymce:true */

let PloneModal = null;

tinymce.PluginManager.add('relatedimagesgallery', (editor, url) => {
    let gallery_modal = null;

    debugger;

    const openGalleryEditor = () => {
        if(!this.gallery_modal) {
            const PloneModal = window.__patternslib_registry["plone-modal"];
            var $el = $("<div/>").appendTo("body");
            this.gallery_modal = new PloneModal($el, {
                ajaxUrl: "./@@gallery-editor?ajax_load=1",
                modalSizeClass: "modal-xl",
                position:"center top",
                automaticallyAddButtonActions: false,
                actions: {
                    "submit": (e) => {
                        alert("submitted");
                    }
                }
            });
            this.gallery_modal.show();
        } else {
            this.gallery_modal.show();
        }
    };

    // add plugin code here
    editor.ui.registry.addButton("relatedimagesgallery", {
        icon: "gallery",
        tooltip: "Insert/edit related image gallery",
        onAction: () => {
            openGalleryEditor();
        },
        // stateSelector: "img:not([data-mce-object])",
    });
    editor.ui.registry.addMenuItem("relatedimagesgallery", {
        icon: "gallery",
        text: "Insert/edit related image gallery",
        onAction: () => {
            openGalleryEditor();
        },
        // stateSelector: "img:not([data-mce-object])",
    });
});
