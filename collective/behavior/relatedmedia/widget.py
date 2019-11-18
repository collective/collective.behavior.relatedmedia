# -*- coding: utf-8 -*-
from Products.CMFPlone import PloneMessageFactory as _
from collective.behavior.relatedmedia.interfaces import IRelatedMediaWidget
from plone.app.content.browser.contents import get_top_site_from_url
from plone.app.content.browser.file import TUS_ENABLED
from plone.app.content.interfaces import IStructureAction
from plone.app.content.utils import json_dumps
from plone.app.widgets.utils import get_widget_form
from plone.app.z3cform.views import RenderWidget
from plone.app.z3cform.widget import RelatedItemsWidget
from plone.uuid.interfaces import IUUID
from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import getUtilitiesFor
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import implementer_only


@implementer_only(IRelatedMediaWidget)
class RelatedMediaWidget(RelatedItemsWidget):
    """ overrides widget template """


@implementer(IFieldWidget)
def RelatedMediaFieldWidget(field, request, extra=None):
    if extra is not None:
        request = extra
    return FieldWidget(field, RelatedMediaWidget(request))


class RelatedMediaRenderWidget(RenderWidget):

    index = ViewPageTemplateFile('widget_relatedmedia.pt')
    ignored_action_ids = [
        'cut',
        'copy',
        'paste',
        'tags',
        'properties',
        'workflow',
    ]

    @property
    def widget_context(self):
        form = get_widget_form(self.context)
        return form.context

    @property
    def upload_context(self):
        view_context = self.widget_context
        if not getattr(view_context, 'related_media_base_path', False):
            return
        return view_context.related_media_base_path[0].to_object

    def get_actions(self):
        actions = []
        context = self.upload_context
        for name, Utility in getUtilitiesFor(IStructureAction):
            utility = Utility(context, self.request)
            actions.append(utility)
        actions.sort(key=lambda a: a.order)
        for a in actions:
            opts = a.get_options()
            if opts['id'] in self.ignored_action_ids:
                continue
            yield opts

    def get_indexes(self):
        return {
            'created': translate(_('Created on'), context=self.request),
            'sortable_title': translate(_('Title'), context=self.request),
        }

    def get_structure_options(self):
        view_context = self.widget_context
        site = get_top_site_from_url(view_context, self.request)
        base_url = site.absolute_url()
        base_vocabulary = '%s/@@getVocabulary?name=' % base_url
        site_path = site.getPhysicalPath()
        upload_context = self.upload_context
        options = {
            'vocabularyUrl': '%splone.app.vocabularies.Catalog' % (
                base_vocabulary),
            'urlStructure': {
                'base': base_url,
                'appended': '/folder_contents'
            },
            'moveUrl': '%s{path}/fc-itemOrder' % base_url,
            'indexOptionsUrl': '%s/@@qsOptions' % base_url,
            'contextInfoUrl': '%s{path}/@@fc-contextInfo' % base_url,
            'setDefaultPageUrl': '%s{path}/@@fc-setDefaultPage' % base_url,
            'availableColumns': {},
            'attributes': ['Title', 'path', 'getURL', 'getIcon', 'getMimeIcon', 'portal_type'],  # noqa
            'buttons': list(self.get_actions()),
            'rearrange': {
                'properties': self.get_indexes(),
                'url': '%s{path}/@@fc-rearrange' % base_url
            },
            'basePath': '/' + '/'.join(upload_context.getPhysicalPath()[len(site_path):]),  # noqa
            'upload': {
                'relativePath': 'fileUpload',
                'baseUrl': upload_context.absolute_url(),
                'initialFolder': IUUID(upload_context, None),
                'useTus': TUS_ENABLED
            },
            'thumb_scale': 'thumb',
        }
        return json_dumps(options)
