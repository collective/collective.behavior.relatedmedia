# -*- coding: utf-8 -*-
from collective.behavior.relatedmedia.interfaces import IRelatedMediaWidget
from plone.app.z3cform.widget import RelatedItemsWidget
from zope.interface import implementer_only


@implementer_only(IRelatedMediaWidget)
class RelatedMediaWidget(RelatedItemsWidget):
    """ overrides input template """

    def render(self):
        import pdb; pdb.set_trace()
        return super(RelatedMediaWidget, self).render()
