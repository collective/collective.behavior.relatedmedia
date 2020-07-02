# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from collective.behavior.relatedmedia.utils import get_media_root
from collective.behavior.relatedmedia.utils import get_related_media
from logging import getLogger
from plone import api
from plone.dexterity.utils import createContentInContainer
from z3c.relationfield import create_relation
from z3c.relationfield.event import _setRelation

try:
    from plone.app.contenttypes.behaviors.leadimage import ILeadImageBehavior
except ImportError:
    from plone.app.contenttypes.behaviors.leadimage import ILeadImage as ILeadImageBehavior  # noqa: E501

logger = getLogger(__name__)


def create_media_base_path(obj, event):
    """ automatically create related base path
    """

    if obj.related_media_base_path or getattr(obj.REQUEST, 'translation_info', {}):  # noqa
        # if we already have a value or we create a translation just return
        return

    media_root = get_media_root(obj)

    if media_root is None:
        # do nothing ... no media root path is defined
        return

    # we use UID for media container id to avoid duplicate ids in media root
    media_base_id = obj.UID()

    if media_base_id not in media_root:
        # create base path
        media_base = createContentInContainer(
            media_root,
            'Folder',
            id=media_base_id,
            title=obj.Title(),
        )
    else:
        # XXX: this should never happen?
        media_base = media_root[media_base_id]

    _rel = create_relation('/'.join(media_base.getPhysicalPath()))
    # fix RelationValue properties
    _setRelation(obj, 'related_media_base_path', _rel)
    obj.related_media_base_path = _rel


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
    except Exception as msg:
        # possibly unsynced state ...
        logger.info(
            "Could not sync workflow state of %s: %s (%s)",
            obj.absolute_url(1), event.status, msg)


def update_leadimage(obj, event):
    if not api.portal.get_registry_record('collective.behavior.relatedmedia.update_leadimage', default=False):  # noqa
        return

    imgs = get_related_media(obj, portal_type='Image')

    if not imgs:
        return

    # set first related image as lead image (incl. caption)
    ILeadImageBehavior(obj).image = imgs[0].image
    ILeadImageBehavior(obj).image_caption = safe_unicode(imgs[0].Title())
