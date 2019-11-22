# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.utils import createContentInContainer
from plone.protect.interfaces import IDisableCSRFProtection
from zope.globalrequest import getRequest
from zope.interface import alsoProvides


def get_media_root(context, as_path=False):
    portal = api.portal.get()
    nav_root = api.portal.get_navigation_root(context)
    media_container_path = api.portal.get_registry_record(
        'collective.behavior.relatedmedia.media_container_path', default='/')
    media_container_in_assets_folder = api.portal.get_registry_record(
        'collective.behavior.relatedmedia.media_container_in_assets_folder', default=False)  # noqa
    assets_folder_id = ''

    if media_container_in_assets_folder:
        # Assets folder
        pc = api.portal.get_tool('portal_catalog')
        results = pc.unrestrictedSearchResults(
            portal_type='LIF',
            Language=api.portal.get_current_language(context))
        if results:
            assets_folder_id = '/' + results[0].id

    media_container = portal.restrictedTraverse("{}{}{}".format('/'.join(
        nav_root.getPhysicalPath()), assets_folder_id, media_container_path), None)  # noqa

    if media_container is None and media_container_path:
        # try to create media container path
        # XXX: this is a write on read when accessing the behavior
        #      the first time
        alsoProvides(getRequest(), IDisableCSRFProtection)
        media_container = nav_root
        for f_id in media_container_path.split('/'):
            if not f_id:
                continue
            if not hasattr(media_container, f_id):
                media_container = createContentInContainer(
                    media_container, 'Folder', id=f_id, title=f_id,
                    exclude_from_nav=True, checkConstraints=False)
            else:
                media_container = media_container[f_id]

    if as_path:
        return '/'.join(media_container.getPhysicalPath())

    return media_container


def media_root_path(context):
    return get_media_root(context, as_path=True)
