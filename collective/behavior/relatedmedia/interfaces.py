# -*- coding: utf-8 -*-
from collective.behavior.relatedmedia import messageFactory as _
from zope import schema
from zope.interface import Interface


class ICollectiveBehaviorRelatedmediaLayer(Interface):
    """browserlayer"""


class IRelatedMediaSettings(Interface):
    """various settings"""

    media_container_path = schema.TextLine(
        title=_("Media Container"),
        description=_(
            "Traversable path to media container. "
            "We respect IPloneSiteRoot, INavigationRoot "
            'and IChildSite (lineage) as "/"'
        ),
        required=True,
    )

    media_container_in_assets_folder = schema.Bool(
        title=_("Create Media Container in Assets Folder " "(language independent)?"),
        description=_(
            "If True, the Media Container path defined above is "
            "generated in the language independend Assets folder. "
            "This requires plone.app.multilingual."
        ),
        default=False,
        required=False,
    )

    create_media_container_base_paths = schema.Bool(
        title=_("Create containers for each linked object?"),
        default=False,
        required=False,
    )

    image_gallery_cssclass = schema.List(
        title=_("Gallery CSS classes"),
        value_type=schema.TextLine(title="CSS Class"),
        required=False,
    )

    image_gallery_default_class = schema.TextLine(
        title=_("Default gallery class for new articles"),
        required=True,
    )

    image_gallery_default_gallery_first_image_scale = schema.Choice(
        title=_("Gallery default scale for first image"),
        vocabulary="plone.app.vocabularies.ImagesScales",
        default="large",
        required=False,
    )

    image_gallery_default_scale = schema.Choice(
        title=_("Gallery default scale"),
        vocabulary="plone.app.vocabularies.ImagesScales",
        default="preview",
        required=False,
    )

    image_gallery_default_preview_scale_direction = schema.Bool(
        title=_("Default setting for cropping gallery images"),
        default=False,
        required=False,
    )

    include_leadimage_default = schema.Bool(
        title=_("Include leadimage in image gallery?"),
        default=True,
        required=False,
    )

    update_leadimage = schema.Bool(
        title=_("Set first related image as leadimage?"),
        description=_("This is applied on any change."),
        default=False,
        required=False,
    )

    open_attachment_in_new_window = schema.Bool(
        title=_("Open Attachment links in new window"),
        default=True,
        required=False,
    )
