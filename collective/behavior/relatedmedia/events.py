from collective.behavior.relatedmedia.utils import get_media_root
from collective.behavior.relatedmedia.utils import get_related_media
from logging import getLogger
from plone import api
from plone.dexterity.utils import createContentInContainer
from Products.CMFPlone.utils import safe_unicode
from z3c.relationfield import create_relation
from z3c.relationfield.event import _setRelation
from zope.globalrequest import getRequest


try:
    from plone.app.contenttypes.behaviors.leadimage import ILeadImageBehavior
except ImportError:
    from plone.app.contenttypes.behaviors.leadimage import (
        ILeadImage as ILeadImageBehavior,
    )

logger = getLogger(__name__)


def create_media_base_path(obj, event):
    """automatically create related base path"""

    create = api.portal.get_registry_record(
        "collective.behavior.relatedmedia.create_media_container_base_paths",
        default=False,
    )

    if (
        not create
        or obj.related_media_base_path
        or getattr(getRequest(), "translation_info", {})
    ):
        # do not create or we already have a value or we create a translation just return
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
            "Folder",
            id=media_base_id,
            title=obj.Title(),
        )
    else:
        # XXX: this should never happen?
        media_base = media_root[media_base_id]

    _rel = create_relation("/".join(media_base.getPhysicalPath()))
    # fix RelationValue properties
    _setRelation(obj, "related_media_base_path", _rel)
    obj.related_media_base_path = _rel


def sync_workflow_state(obj, event):
    """keep workflow of base path in sync"""

    if not obj.related_media_base_path:
        return

    try:
        api.content.transition(
            obj=obj.related_media_base_path.to_object,
            transition=event.status["action"],
        )
    except (api.exc.InvalidParameterError, api.exc.MissingParameterError) as msg:
        # possibly unsynced state ...
        logger.info(
            "Could not sync workflow state of %s: %s (%s)",
            obj.absolute_url(1),
            event.status,
            msg,
        )


def modified(obj, event):
    update_leadimage(obj, event)
    update_titles(obj, event)


def update_leadimage(obj, event):
    if not api.portal.get_registry_record(
        "collective.behavior.relatedmedia.update_leadimage", default=False
    ):
        return

    imgs = get_related_media(obj, portal_type="Image")

    if not imgs:
        return

    lead_image_adapter = ILeadImageBehavior(obj, None)
    if lead_image_adapter is None:
        # The lead image adapter could not be retrieved.
        # This usually occurs if the FTI does not list the `plone.leadimage` behavior.
        return

    if not lead_image_adapter.image:
        # set first related image as lead image (incl. caption)
        lead_image_adapter.image = imgs[0].image
        lead_image_adapter.image_caption = safe_unicode(imgs[0].Title())
        obj.reindexObject()


def get_obj_from_relateditem_path(value, prefix=19):
    item_path = value[prefix:].replace("--", "/")
    rel_obj = None

    try:
        rel_obj = api.content.get(path=item_path)
    except Exception:
        logger.warn(f"Could not find related item {item_path}")

    return rel_obj


def update_titles(obj, event):
    req_form = getRequest().form

    for k in req_form:
        if k.startswith("relatedmedia-title-"):
            rel_obj = get_obj_from_relateditem_path(k)
            if rel_obj and rel_obj.title != req_form[k]:
                rel_obj.title = req_form[k]
                rel_obj.reindexObject()
        if k.startswith("relatedmedia-description-"):
            rel_obj = get_obj_from_relateditem_path(k, 25)
            if rel_obj and rel_obj.description != req_form[k]:
                rel_obj.description = req_form[k]
                rel_obj.reindexObject()
