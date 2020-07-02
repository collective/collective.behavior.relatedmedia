# -*- coding: utf-8 -*-
from collective.behavior.relatedmedia import messageFactory as _
from collective.behavior.relatedmedia.utils import media_root_path
from collective.behavior.relatedmedia.widget import RelatedMediaFieldWidget
from plone import api
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import IEditForm
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

try:
    from plone.app.multilingual.dx.interfaces import ILanguageIndependentField
    HAS_PAM = True
except ImportError:
    HAS_PAM = False


@implementer(IVocabularyFactory)
class GalleryCSSClassesVocabulary(object):

    def __call__(self, context):
        return SimpleVocabulary.fromValues(api.portal.get_registry_record(
            'collective.behavior.relatedmedia.image_gallery_cssclass'))


def default_css_class():
    return api.portal.get_registry_record(
        'collective.behavior.relatedmedia.image_gallery_default_class')


def default_preview_scale_direction():
    return api.portal.get_registry_record(
        'collective.behavior.relatedmedia.'
        'image_gallery_default_preview_scale_direction')


def default_include_leadimage():
    return api.portal.get_registry_record(
        'collective.behavior.relatedmedia.'
        'include_leadimage_default', default=True)


@provider(IFormFieldProvider)
class IRelatedMedia(model.Schema):

    related_media_base_path = RelationChoice(
        title=_(u'label_base_path', default=u'Base Path'),
        description=_(
            'label_base_path_desc',
            default='Base path for uploaded content. If not given '
                    'the base path is automatically generated as '
                    '[configured media root path]/[this id].'),
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    form.widget(
        'related_media_base_path',
        RelatedMediaFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'recentlyUsed': True,  # Just turn on. Config in plone.app.widgets.
            'selectableTypes': ['Folder'],
            'basePath': media_root_path,
        },
    )

    show_titles_as_caption = schema.Bool(
        title=_(u"Show image titles as caption"),
        default=False,
        required=False,
    )

    include_leadimage = schema.Bool(
        title=_(u"Include Leadimage"),
        description=_(
            "Whether or not include the Leadimage in the gallery viewlet"),
        defaultFactory=default_include_leadimage,
        required=False,
    )

    first_image_scale = schema.Choice(
        title=_(u"First image scale"),
        description=_("Size for the first image in the gallery"),
        vocabulary="plone.app.vocabularies.ImagesScales",
        default=u'large',
    )

    first_image_scale_direction = schema.Bool(
        title=_(u"Crop first image"),
        description=_("Crop the image to the selected boundaries above"),
        defaultFactory=default_preview_scale_direction,
        required=False,
    )

    preview_scale = schema.Choice(
        title=_(u"Image scale"),
        description=_("Gallery image preview scale"),
        vocabulary="plone.app.vocabularies.ImagesScales",
        default='preview',
    )

    preview_scale_direction = schema.Bool(
        title=_(u"Crop image"),
        description=_("Crop the image to the selected boundaries above"),
        default=False,
        required=False,
    )

    gallery_css_class = schema.Choice(
        title=_(u"Gallery layout"),
        description=_("Feel free to add/remove classes in your registry.xml"),
        vocabulary="collective.relatedmedia.gallerycssclasses",
        defaultFactory=default_css_class,
    )

    related_images = RelationList(
        title=_(u'label_images', default=u'Additional Related Images'),
        value_type=RelationChoice(
            title=_(u"Pictures"),
            vocabulary='plone.app.vocabularies.Catalog',
        ),
        required=False,
        default=[],
    )
    form.widget(
        'related_images',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'recentlyUsed': True,  # Just turn on. Config in plone.app.widgets.
            'selectableTypes': ['Image'],
        },
    )

    related_attachments = RelationList(
        title=_(u"label_attachments", default=u"Additional Related Attachments"),  # noqa
        value_type=RelationChoice(
            title=_(u"Files"),
            vocabulary='plone.app.vocabularies.Catalog',
        ),
        required=False,
        default=[],
    )
    form.widget(
        'related_attachments',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'recentlyUsed': True,  # Just turn on. Config in plone.app.widgets.
            'selectableTypes': ['File'],
        },
    )

    # AddForm shows media_base_path field ... the rest is only on EditForm
    form.omitted(
        'related_images',
        'show_titles_as_caption',
        'include_leadimage',
        'first_image_scale',
        'first_image_scale_direction',
        'preview_scale',
        'preview_scale_direction',
        'gallery_css_class',
        'related_attachments',
    )
    form.no_omit(
        IEditForm,
        'related_images',
        'show_titles_as_caption',
        'include_leadimage',
        'first_image_scale',
        'first_image_scale_direction',
        'preview_scale',
        'preview_scale_direction',
        'gallery_css_class',
        'related_attachments',
    )

    model.fieldset('relatedmedia', label=_("Related Media"), fields=[
        'related_media_base_path',
        'show_titles_as_caption',
        'include_leadimage',
        'first_image_scale',
        'first_image_scale_direction',
        'preview_scale',
        'preview_scale_direction',
        'gallery_css_class',
        'related_images',
        'related_attachments',
    ])


# define languageindependent fields if p.a.multilingual is installed
if HAS_PAM:
    alsoProvides(IRelatedMedia['related_media_base_path'], ILanguageIndependentField)  # noqa
    alsoProvides(IRelatedMedia['show_titles_as_caption'], ILanguageIndependentField)  # noqa
    alsoProvides(IRelatedMedia['include_leadimage'], ILanguageIndependentField)  # noqa
    alsoProvides(IRelatedMedia['first_image_scale'], ILanguageIndependentField)  # noqa
    alsoProvides(IRelatedMedia['first_image_scale_direction'], ILanguageIndependentField)  # noqa
    alsoProvides(IRelatedMedia['preview_scale'], ILanguageIndependentField)  # noqa
    alsoProvides(IRelatedMedia['preview_scale_direction'], ILanguageIndependentField)  # noqa
    alsoProvides(IRelatedMedia['gallery_css_class'], ILanguageIndependentField)  # noqa
