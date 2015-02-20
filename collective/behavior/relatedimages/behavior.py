from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.interface.declarations import provider


@provider(IFormFieldProvider)
class IRelatedImages(form.Schema):

    relates_images = RelationList(
        title=u'Related Images',
        default=[],
        value_type=RelationChoice(
            title=u"Pictures",
            source=CatalogSource(portal_type='Image'),
        ),
        required=False,
    )
