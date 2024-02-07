from plone.app.z3cform.interfaces import IRelatedItemsWidget
from plone.app.z3cform.widgets.relateditems import RelatedItemsWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from zope.interface import implementer
from zope.interface import implementer_only


class IRelatedImagesWidget(IRelatedItemsWidget):
    """marker for widget"""


@implementer_only(IRelatedImagesWidget)
class RelatedImagesWidget(RelatedItemsWidget):
    """overrides widget template"""


@implementer(IFieldWidget)
def RelatedImagesFieldWidget(field, request, extra=None):
    if extra is not None:
        request = extra
    return FieldWidget(field, RelatedImagesWidget(request))


class IRelatedAttachmentsWidget(IRelatedItemsWidget):
    """marker for widget"""


@implementer_only(IRelatedAttachmentsWidget)
class RelatedAttachmentsWidget(RelatedItemsWidget):
    """overrides widget template"""


@implementer(IFieldWidget)
def RelatedAttachmentsFieldWidget(field, request, extra=None):
    if extra is not None:
        request = extra
    return FieldWidget(field, RelatedAttachmentsWidget(request))
