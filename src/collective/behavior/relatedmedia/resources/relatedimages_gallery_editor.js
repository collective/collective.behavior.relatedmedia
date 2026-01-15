window.tinymce.PluginManager.add('relatedimagesgallery', (editor, url) => {

    async function galleryeditor() {
        const galleryeditor = new window.__collectivebehaviorrelatedmedia_galleryeditor(editor);
        galleryeditor.show();
    }

    // add plugin code here
    editor.ui.registry.addButton("relatedimagesgallery", {
        icon: "gallery",
        tooltip: "Insert/edit related image gallery",
        onAction: () => {
            galleryeditor();
        },
    });
    editor.ui.registry.addMenuItem("relatedimagesgallery", {
        icon: "gallery",
        text: "Insert/edit related image gallery",
        onAction: () => {
            galleryeditor();
        },
    });
});
