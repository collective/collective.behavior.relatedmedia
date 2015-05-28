import pkg_resources

try:
    pkg_resources.get_distribution('plone.app.widgets')
except pkg_resources.DistributionNotFound:
    pass
else:
    # if plone.app.widgets is installed, use its relateditems widget
    from plone.app.widgets.dx import RelatedItemsWidget
    from z3c.form.interfaces import IFieldWidget, IFormLayer
    from z3c.form.util import getSpecification
    from z3c.form.widget import FieldWidget
    from zope.component import adapter
    from zope.interface import implementer

    from .behavior import IRelatedMedia


    @adapter(getSpecification(IRelatedMedia['related_images']), IFormLayer)
    @implementer(IFieldWidget)
    def RelatedImagesFieldWidget(field, request):
        widget = FieldWidget(field, RelatedItemsWidget(request))
        # this needs https://github.com/plone/plone.app.widgets/pull/87
        widget.selectable_types = ["Image", ]
        return widget

    @adapter(getSpecification(IRelatedMedia['related_attachments']),
        IFormLayer)
    @implementer(IFieldWidget)
    def RelatedAttachmentsFieldWidget(field, request):
        widget = FieldWidget(field, RelatedItemsWidget(request))
        # this needs https://github.com/plone/plone.app.widgets/pull/87
        widget.selectable_types = ["File", ]
        return widget
