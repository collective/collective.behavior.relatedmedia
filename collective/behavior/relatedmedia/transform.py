from bs4 import BeautifulSoup
from plone.base.utils import safe_text
from plone.outputfilters.interfaces import IFilter
from zope.interface import implementer

import re


@implementer(IFilter)
class RelatedImagesFilter:
    def __init__(self, context=None, request=None):
        self.context = context
        self.request = request

    # IFilter implementation
    order = 900

    def is_enabled(self):
        # disabled until developed
        return False

    def __call__(self, data):
        data = re.sub(r"<([^<>\s]+?)\s*/>", self._shorttag_replace, data)
        soup = BeautifulSoup(safe_text(data), "html.parser")
        return str(soup)
