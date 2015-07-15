from operator import attrgetter
from plone import api
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.supermodel import model
from z3c.form import widget
from z3c.relationfield.schema import RelationChoice, RelationList
from zope import schema
from zope.interface import provider, implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from . import messageFactory as _

RELATED_MEDIA_CONFIG_STORAGE_KEY = "__collective.related.media.local_config__"


@implementer(IVocabularyFactory)
class ImageScalesVocabulary(object):

    def __call__(self, context):
        props = api.portal.get_tool('portal_properties')
        terms = set()
        for s in props.imaging_properties.allowed_sizes:
            k, v = s.split(' ')
            if k not in map(attrgetter('value'), terms):
                terms.add(SimpleTerm(k, title="{0} ({1})".format(k, v)))
        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class GalleryCSSClassesVocabulary(object):

    def __call__(self, context):
        return SimpleVocabulary.fromValues(api.portal.get_registry_record(
            'collective.behavior.relatedmedia.image_gallery_cssclass'))


@provider(IFormFieldProvider)
class IRelatedMedia(form.Schema):

    related_images = RelationList(
        title=_('label_images', default=u'Related Images'),
        default=[],
        value_type=RelationChoice(
            title=_(u"Pictures"),
            source=CatalogSource(portal_type=['Image', 'Folder']),
        ),
        required=False,
    )

    show_titles_as_caption = schema.Bool(
        title=_("Show image titles as caption"),
        default=False,
        required=False,
    )

    include_leadimage = schema.Bool(
        title=_("Include Leadimage"),
        description=_("Wether or not include the Leadimage in the " \
            "gallery viewlet"),
        default=True,
        required=False,
    )

    first_image_scale = schema.Choice(
        title=_("First image scale"),
        description=_("Size for the first image in the gallery"),
        vocabulary="collective.relatedmedia.imagescales",
        default='large',
    )

    first_image_scale_direction = schema.Bool(
        title=_("Crop first image"),
        description=_("Downsize or crop the image to the given boundaries"),
        default=False,
        required=False,
    )

    preview_scale = schema.Choice(
        title=_("Image scale"),
        description=_("Gallery image preview scale"),
        vocabulary="collective.relatedmedia.imagescales",
        default='preview',
    )

    preview_scale_direction = schema.Bool(
        title=_("Crop image"),
        description=_("Downsize or crop the image to the given boundaries"),
        default=False,
        required=False,
    )

    gallery_css_class = schema.Choice(
        title=_("Gallery layout"),
        description=_("Feel free to add/remove classes in your registry.xml"),
        vocabulary="collective.relatedmedia.gallerycssclasses",
    )

    related_attachments = RelationList(
        title=_(u"label_attachments", default=u"Related Attachments"),
        default=[],
        value_type=RelationChoice(
            title=_(u"Files"),
            source=CatalogSource(portal_type=['File', 'Folder']),
        ),
        required=False,
    )

    model.fieldset('relatedmedia', label=_("Related Media"), fields=[
        'related_images', 'show_titles_as_caption', 'include_leadimage',
        'first_image_scale', 'first_image_scale_direction', 'preview_scale',
        'preview_scale_direction', 'gallery_css_class', 'related_attachments'])


def default_css_class_factory(widget):
    return api.portal.get_registry_record('collective.behavior.relatedmedia' \
        '.image_gallery_default_class')

default_css_class_value = widget.ComputedWidgetAttribute(
    default_css_class_factory, field=IRelatedMedia['gallery_css_class'])
