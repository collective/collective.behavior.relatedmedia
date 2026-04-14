
# collective.behavior.relatedmedia

A Plone Dexterity behavior that lets editors upload, manage, and display related
images and file attachments directly on content items — without leaving the edit
form.

## Features

- **Dexterity behavior** — attach the behavior to any content type via the
  control panel or ZCML; no custom content type required.
- **Dedicated edit tab** — a *Related Media* tab appears on every content item
  that has the behavior enabled.
- **Inline upload & selection** — editors can upload new files or pick existing
  Plone content objects through the relation widget; relation type (image vs.
  attachment) is determined automatically from the file's MIME type.
- **Drag-and-drop ordering** — items inside the widget can be reordered via
  drag-and-drop; titles are editable inline.
- **Configurable media container** — uploaded files are stored in a dedicated
  folder whose path is defined in the *Related Media Settings* control panel.
  Supports `plone.app.multilingual` (language-independent assets folder) and
  per-object sub-containers.
- **Viewlets for display** — two viewlets render the media on the content view:
  - `collective.behavior.related_images` (default: `plone.belowcontenttitle`)
  - `collective.behavior.related_attachments` (default: `plone.belowcontentbody`)
- **Inline gallery via TinyMCE** — a toolbar button lets editors embed an image
  gallery directly inside the rich-text body; placement, image selection, and
  order are fully configurable without leaving the editor.
- **Configurable image scales** — default scales for thumbnails, preview images,
  and overlay images are set globally in the control panel.
- **Gallery CSS classes** — a registry-controlled vocabulary provides the
  available CSS classes for galleries; a default class can be pre-selected.


## Installation

```
pip install collective.behavior.relatedmedia
```

or add the egg to your buildout configuration, then enable the add-on in the
Plone **Add-ons** control panel.


## Configuration

Open **Site Setup → Add-on Configuration → Related Media Settings** and:

1. Set a valid **Media Container** path (relative to the site root or navigation
   root) where uploaded files will be stored.
2. Optionally enable **Create Media Container in Assets Folder** if you use
   `plone.app.multilingual` and want language-independent storage.
3. Adjust the default image scales and gallery CSS classes to match your theme.


## Usage

### Adding media to a content item

1. Open the content item in edit mode.
2. Switch to the **Related Media** tab.
3. Use the *Related Images* widget to upload new images or select existing ones.
   Use the *Related Attachments* widget for non-image files.
4. Reorder items by dragging, edit titles inline, then save.

### Embedding a gallery in the rich-text body

1. Place the cursor in the text where the gallery should appear.
2. Click the **Gallery** icon in the TinyMCE toolbar.
3. Select the images and choose a gallery style; drag-and-drop to reorder.
4. To modify an existing gallery, click inside the preview block and open the
   toolbar icon again.

> **Note:** If you embed a gallery in the text body, disable the
> *Show images in viewlet* checkbox to avoid rendering images twice.
> Images added to the behavior *after* inserting the gallery must be added to
> the TinyMCE gallery manually.


## Overriding viewlet placement

```xml
<include package="collective.behavior.relatedmedia" />
<configure package="collective.behavior.relatedmedia">
    <browser:viewlet
        name="collective.behavior.related_images"
        for="*"
        manager="plone.app.layout.viewlets.interfaces.IAboveContentTitle"
        template="widget_images_display.pt"
        permission="zope2.View" />
</configure>
```


## Authors

- Peter Mathis [petschki]

## Contributors

- Peter Holzer [agitator]
