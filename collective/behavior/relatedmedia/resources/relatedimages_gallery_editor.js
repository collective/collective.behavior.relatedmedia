window.tinymce.PluginManager.add('relatedimagesgallery', (editor, url) => {

    async function galleryeditor() {
        // das window.__geheimprojekt__tinymce__helplink ... steht zur verfügung, da in main.js das help.js importiert wurde, das dann wieder dieses globale window objekt registriert.
        // zum zeitpunkt dieses aufrufs (ein button wird gedrückt, siehe unten) ist schon alles fertig geladen und die ladereihenfolge probleme meiner vorherigen versuche ein tinymce plugin zu registrieren sind keine mehr.
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
