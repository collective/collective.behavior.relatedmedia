
# Upload and Manage Related Images and Attachments


This packages adds a dexterity behavior to upload and manage related images and attachments for rich media pages.


## Install

Add to buildout configuration or ``pip install collective.behavior.relatedmedia``.

Enable it in Plone Add-on controlpanel.


## Configure

There is a ``Related Media Settings`` controlpanel in the Add-on configuration section.

Make sure you set a valid ``Media Container`` path where all the media is stored.


## Edit

When you edit a Page go to the tab ``Related Media``.

In the relateditems widgets you can select existing content from your page, or you upload
new content via the uploader. Relation type is selected via the mimetype of the media.
You can change the titles of the relations in an input field and rearrange the order
within the widget via drag/drop.


## View

The related media viewlets (image, attachment) are defined by:

- ``collective.behavior.related_images`` -> plone.belowcontenttitle
- ``collective.behavior.related_attachments`` -> plone.belowcontentbody


Feel free to override the placement in your package zcml for example::

    <include package="collective.behavior.relatedmedia" />
    <configure package="collective.behavior.relatedmedia">
        <browser:viewlet
            name="collective.behavior.related_images"
            for="*"
            manager="plone.app.layout.viewlets.interfaces.IAboveContentTitle"
            template="widget_images_display.pt"
            permission="zope2.View" />
    </configure>

## TinyMCE Template

We provide a TinyMCE toolbar icon to enable gallery placement inside the richtext editor::

- create a new paragraph in your text where you want to place the gallery.
- Click on the Gallery Icon in the toolbar
- Choose the images you want inside your gallery. You can drag/drop reorder the images too.
- Edit an existing gallery by clicking inside the preview block and click the toolbar icon again.

NOTES:

- make sure you disable the checkbox "Show images in viewlet" to prevent double rendered gallery.
- When you add related images after you've inserted a gallery in TinyMCE you need to edit it again
  and add the new images manually.


## Author

- Peter Mathis [petschki]


## Contributors

- Peter Holzer [agitator]
