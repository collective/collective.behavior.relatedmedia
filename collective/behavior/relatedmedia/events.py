# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.utils import createContentInContainer
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds


def create_media_base_path(obj, event):
    """ automatically create related base path
    """

    if obj.related_media_base_path:
        return

    portal = api.portal.get()
    nav_root = api.portal.get_navigation_root(obj)
    media_root = portal.restrictedTraverse("{}{}".format('/'.join(
        nav_root.getPhysicalPath()),
        api.portal.get_registry_record(
        'collective.behavior.relatedmedia.media_container_path')), None)

    if media_root is None:
        # do nothing ... no media root path is defined
        return

    # we user UID for media container id to avoid duplicate ids in media root
    media_base_id = obj.UID()

    if media_base_id not in media_root:
        # create base path
        createContentInContainer(
            media_root,
            'Folder',
            id=media_base_id,
            title=obj.Title(),
        )

    to_id = getUtility(IIntIds).getId(media_root[media_base_id])
    obj.related_media_base_path = RelationValue(to_id)


def sync_workflow_state(obj, event):
    """ keep workflow of base path in sync
    """

    if not obj.related_media_base_path:
        return

    try:
        api.content.transition(
            obj=obj.related_media_base_path.to_object,
            transition=event.status['action'],
        )
    except api.exc.InvalidParameterError:
        # possibly unsynced state ...
        pass
