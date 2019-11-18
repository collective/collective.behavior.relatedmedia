# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.utils import createContentInContainer


def get_media_root(context):
    portal = api.portal.get()
    nav_root = api.portal.get_navigation_root(context)
    media_container_path = api.portal.get_registry_record(
        'collective.behavior.relatedmedia.media_container_path')
    media_container = portal.restrictedTraverse("{}{}".format('/'.join(
        nav_root.getPhysicalPath()), media_container_path), None)

    if media_container is None and media_container_path:
        # try to create media container path
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

    return media_container
