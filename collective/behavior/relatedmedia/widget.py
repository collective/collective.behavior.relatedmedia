from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from zope.interface import implementer
from zope.interface import implementer_only


try:
    # Plone 6.1
    from plone.app.z3cform.interfaces import (
        IContentBrowserWidget as IRelatedMediaWidget,
    )
    from plone.app.z3cform.widgets.contentbrowser import (
        ContentBrowserWidget as RelatedMediaWidget,
    )
except ImportError:
    # Plone 6.0
    from plone.app.z3cform.interfaces import IRelatedItemsWidget as IRelatedMediaWidget
    from plone.app.z3cform.widgets.relateditems import (
        RelatedItemsWidget as RelatedMediaWidget,
    )


class IRelatedImagesWidget(IRelatedMediaWidget):
    """marker for widget"""


@implementer_only(IRelatedImagesWidget)
class RelatedImagesWidget(RelatedMediaWidget):
    """overrides widget template"""


@implementer(IFieldWidget)
def RelatedImagesFieldWidget(field, request, extra=None):
    if extra is not None:
        request = extra
    return FieldWidget(field, RelatedImagesWidget(request))


class IRelatedAttachmentsWidget(IRelatedMediaWidget):
    """marker for widget"""


@implementer_only(IRelatedAttachmentsWidget)
class RelatedAttachmentsWidget(RelatedMediaWidget):
    """overrides widget template"""


@implementer(IFieldWidget)
def RelatedAttachmentsFieldWidget(field, request, extra=None):
    if extra is not None:
        request = extra
    return FieldWidget(field, RelatedAttachmentsWidget(request))
