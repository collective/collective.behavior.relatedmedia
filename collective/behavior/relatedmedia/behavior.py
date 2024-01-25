from collective.behavior.relatedmedia import messageFactory as _
from collective.behavior.relatedmedia.utils import media_root_path
from collective.behavior.relatedmedia.widget import RelatedAttachmentsFieldWidget
from collective.behavior.relatedmedia.widget import RelatedImagesFieldWidget
from plone import api
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import HIDDEN_MODE
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.deferredimport import deprecated
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

import os


try:
    from plone.app.multilingual.dx.interfaces import ILanguageIndependentField

    HAS_PAM = True
except ImportError:
    HAS_PAM = False


def read_js_template(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as tpl:
        return tpl.read().replace('"', '"').replace("\n", "")


@implementer(IVocabularyFactory)
class GalleryCSSClassesVocabulary:
    def __call__(self, context):
        return SimpleVocabulary.fromValues(
            api.portal.get_registry_record(
                "collective.behavior.relatedmedia.image_gallery_cssclass"
            )
        )


def default_css_class():
    return api.portal.get_registry_record(
        "collective.behavior.relatedmedia.image_gallery_default_class"
    )


def default_gallery_first_image_scale():
    return api.portal.get_registry_record(
        "collective.behavior.relatedmedia.image_gallery_default_gallery_first_image_scale",
        default="large",
    )


def default_gallery_scale():
    return api.portal.get_registry_record(
        "collective.behavior.relatedmedia.image_gallery_default_gallery_scale",
        default="preview",
    )


def default_preview_scale_direction():
    return api.portal.get_registry_record(
        "collective.behavior.relatedmedia.image_gallery_default_preview_scale_direction"
    )


def default_titles_as_caption():
    return api.portal.get_registry_record(
        "collective.behavior.relatedmedia.show_titles_as_caption_default", default=False
    )


def default_show_images_viewlet():
    return api.portal.get_registry_record(
        "collective.behavior.relatedmedia.show_images_viewlet", default=True
    )


def default_include_leadimage():
    return api.portal.get_registry_record(
        "collective.behavior.relatedmedia.include_leadimage_default", default=True
    )


@provider(IFormFieldProvider)
class IRelatedMediaBehavior(model.Schema):
    related_images = RelationList(
        title=_("label_images", default="Related Images"),
        value_type=RelationChoice(
            title=_("Pictures"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        default=[],
    )
    form.widget(
        "related_images",
        RelatedImagesFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "recentlyUsed": True,  # Just turn on. Config in plone.app.widgets.
            "selectableTypes": ["Image"],
            "basePath": media_root_path,
            "selectionTemplate": read_js_template(
                "resources/relateditems_selection.xml"
            ),
            # add Description to the returned attributes
            "attributes": [
                "UID",
                "Title",
                "Description",
                "portal_type",
                "path",
                "getURL",
                "getIcon",
                "is_folderish",
                "review_state",
            ],
            "upload": True,
        },
    )

    related_attachments = RelationList(
        title=_("label_attachments", default="Related Attachments"),
        value_type=RelationChoice(
            title=_("Files"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        default=[],
    )

    form.widget(
        "related_attachments",
        RelatedAttachmentsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "recentlyUsed": True,  # Just turn on. Config in plone.app.widgets.
            "selectableTypes": ["File"],
            "basePath": media_root_path,
            "selectionTemplate": read_js_template(
                "resources/relateditems_selection.xml"
            ),
            "attributes": [
                "UID",
                "Title",
                "Description",
                "portal_type",
                "path",
                "getURL",
                "getIcon",
                "is_folderish",
                "review_state",
            ],
            "upload": True,
        },
    )

    show_titles_as_caption = schema.Bool(
        title=_("Show image titles as caption"),
        defaultFactory=default_titles_as_caption,
        required=False,
    )

    show_images_viewlet = schema.Bool(
        title=_("Show images in viewlet"),
        description=_(
            "Turn this of if you place an image gallery inside TinyMCE via "
            "gallery template to avoid duplicated content."
        ),
        defaultFactory=default_show_images_viewlet,
        required=False,
    )

    include_leadimage = schema.Bool(
        title=_("Include leadimage in image gallery?"),
        defaultFactory=default_include_leadimage,
        required=False,
    )

    first_image_scale = schema.Choice(
        title=_("Gallery default scale for first image"),
        vocabulary="plone.app.vocabularies.ImagesScales",
        defaultFactory=default_gallery_first_image_scale,
    )

    first_image_scale_direction = schema.Bool(
        title=_("Crop first image"),
        defaultFactory=default_preview_scale_direction,
        required=False,
    )

    preview_scale = schema.Choice(
        title=_("Image scale"),
        description=_("Gallery image preview scale"),
        vocabulary="plone.app.vocabularies.ImagesScales",
        defaultFactory=default_gallery_scale,
    )

    preview_scale_direction = schema.Bool(
        title=_("Crop image"),
        description=_("Crop the image to the selected boundaries above"),
        default=False,
        required=False,
    )

    gallery_css_class = schema.Choice(
        title=_("Gallery layout"),
        description=_("Feel free to add/remove classes in your registry.xml"),
        vocabulary="collective.relatedmedia.gallerycssclasses",
        defaultFactory=default_css_class,
        required=False,
    )

    related_media_base_path = RelationChoice(
        title=_("label_base_path", default="Base Path"),
        description=_(
            "label_base_path_desc",
            default="Base path for uploaded content. If not given "
            "the base path is automatically generated as "
            "[configured media root path]/[this id].",
        ),
        vocabulary="plone.app.vocabularies.Catalog",
        required=False,
    )

    # outdated
    form.omitted("related_media_base_path")

    model.fieldset(
        "relatedmedia",
        label=_("Related Media"),
        fields=[
            "related_images",
            "related_attachments",
            "show_images_viewlet",
            "show_titles_as_caption",
            "include_leadimage",
            "first_image_scale",
            "first_image_scale_direction",
            "preview_scale",
            "preview_scale_direction",
            "gallery_css_class",
            "related_media_base_path",
        ],
    )


class IGalleryEditSchema(IRelatedMediaBehavior):
    form.mode(
        related_attachments=HIDDEN_MODE,
        show_images_viewlet=HIDDEN_MODE,
        gallery_css_class=HIDDEN_MODE,
        related_media_base_path=HIDDEN_MODE,
    )


# define languageindependent fields if p.a.multilingual is installed
if HAS_PAM:
    alsoProvides(
        IRelatedMediaBehavior["related_media_base_path"], ILanguageIndependentField
    )
    alsoProvides(
        IRelatedMediaBehavior["show_titles_as_caption"], ILanguageIndependentField
    )
    alsoProvides(IRelatedMediaBehavior["include_leadimage"], ILanguageIndependentField)
    alsoProvides(IRelatedMediaBehavior["first_image_scale"], ILanguageIndependentField)
    alsoProvides(
        IRelatedMediaBehavior["first_image_scale_direction"], ILanguageIndependentField
    )
    alsoProvides(IRelatedMediaBehavior["preview_scale"], ILanguageIndependentField)
    alsoProvides(
        IRelatedMediaBehavior["preview_scale_direction"], ILanguageIndependentField
    )
    alsoProvides(IRelatedMediaBehavior["gallery_css_class"], ILanguageIndependentField)


# mark old name as deprecated
deprecated(
    "Renamed to 'IRelatedMediaBehavior'. Will be removed in Version 4.",
    IRelatedMedia="collective.behavior.relatedmedia.behavior:IRelatedMediaBehavior",
)
