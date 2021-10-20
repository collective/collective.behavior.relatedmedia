# -*- coding: utf-8 -*-
from collective.behavior.relatedmedia import messageFactory as _
from zope import schema
from zope.interface import Interface


class IRelatedMediaSettings(Interface):
    """ various settings """

    media_container_path = schema.TextLine(
        title=_(u"Media Container"),
        description=_(
            u"Traversable path to media container. "
            u"We respect IPloneSiteRoot, INavigationRoot "
            u'and IChildSite (lineage) as "/"'
        ),
        required=True,
    )

    media_container_in_assets_folder = schema.Bool(
        title=_(u"Create Media Container in Assets Folder " u"(language independent)?"),
        description=_(
            u"If True, the Media Container path defined above is "
            u"generated in the language independend Assets folder. "
            u"This requires plone.app.multilingual."
        ),
        default=False,
        required=False,
    )

    create_media_container_base_paths = schema.Bool(
        title=_(u"Create containers for each linked object?"),
        default=False,
        required=False,
    )

    image_gallery_cssclass = schema.List(
        title=_(u"Gallery CSS classes"),
        value_type=schema.TextLine(title=u"CSS Class"),
        required=False,
    )

    image_gallery_default_class = schema.TextLine(
        title=_(u"Default gallery class for new articles"),
        required=True,
    )

    image_gallery_default_gallery_first_image_scale = schema.Choice(
        title=_(u"Gallery default scale for first image"),
        vocabulary="plone.app.vocabularies.ImagesScales",
        default="large",
        required=False,
    )

    image_gallery_default_scale = schema.Choice(
        title=_(u"Gallery default scale"),
        vocabulary="plone.app.vocabularies.ImagesScales",
        default="preview",
        required=False,
    )

    image_gallery_default_preview_scale_direction = schema.Bool(
        title=_(u"Default setting for cropping gallery images"),
        default=False,
        required=False,
    )

    include_leadimage_default = schema.Bool(
        title=_(u"Include leadimage in image gallery?"),
        default=True,
        required=False,
    )

    update_leadimage = schema.Bool(
        title=_(u"Set first related image as leadimage?"),
        description=_(u"This is applied on any change."),
        default=False,
        required=False,
    )

    open_attachment_in_new_window = schema.Bool(
        title=_(u"Open Attachment links in new window"),
        default=True,
        required=False,
    )
