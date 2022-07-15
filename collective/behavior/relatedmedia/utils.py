# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone import api
from plone.dexterity.utils import createContentInContainer
from plone.protect.interfaces import IDisableCSRFProtection
from zope.globalrequest import getRequest
from zope.interface import alsoProvides

import logging


logger = logging.getLogger(__name__)


def get_media_root(context, as_path=False):
    container_base = api.portal.get_navigation_root(context)
    media_path = api.portal.get_registry_record(
        "collective.behavior.relatedmedia.media_container_path", default="/media"
    )
    media_container_in_assets_folder = api.portal.get_registry_record(
        "collective.behavior.relatedmedia.media_container_in_assets_folder",
        default=False,
    )

    if media_container_in_assets_folder:
        # Assets folder
        pc = api.portal.get_tool("portal_catalog")
        results = pc.unrestrictedSearchResults(
            portal_type="LIF", Language=api.portal.get_current_language(context)
        )
        if results:
            container_base = results[0].getObject()
        else:
            logger.warn("Could not find Assets folder! Fallback to Navigation Root")

    media_container = container_base

    for f_id in media_path.split("/"):
        if not f_id:
            continue

        if not hasattr(media_container.aq_base, f_id):
            # try to create media container path
            # XXX: this is a write on read when accessing the behavior the first time
            alsoProvides(getRequest(), IDisableCSRFProtection)
            media_container = createContentInContainer(
                media_container,
                "Folder",
                id=f_id,
                title=f_id,
                exclude_from_nav=True,
                checkConstraints=False,
            )
            continue

        media_container = media_container.get(f_id)

    if as_path:
        return "/".join(media_container.getPhysicalPath())

    return media_container


def media_root_path(context):
    return get_media_root(context, as_path=True)


def get_related_media(context, portal_type=None):
    from collective.behavior.relatedmedia.behavior import IRelatedMedia

    context = aq_inner(context)
    rm_behavior = IRelatedMedia(context, None)

    if not rm_behavior:
        return []

    rel_media = []
    if rm_behavior.related_media_base_path:
        try:
            rm_base = rm_behavior.related_media_base_path.to_object
            rel_media = [
                i.getObject()
                for i in rm_base.restrictedTraverse("@@contentlisting")(
                    portal_type=portal_type
                )
            ]
        except Exception:
            rel_media = []
    if portal_type in ("Image", None):
        rel_media += [i.to_object for i in rm_behavior.related_images]
    elif portal_type in ("File", None):
        rel_media += [i.to_object for i in rm_behavior.related_attachments]
    return rel_media
