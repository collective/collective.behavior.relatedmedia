# -*- coding: utf-8 -*-
import transaction

from collective.behavior.relatedmedia.behavior import IRelatedMedia
from collective.behavior.relatedmedia.utils import get_media_root
from plone import api
from plone.app.contenttypes.migration.field_migrators import migrate_datetimefield  # noqa
from plone.app.contenttypes.migration.field_migrators import migrate_richtextfield  # noqa
from plone.app.contenttypes.migration.field_migrators import migrate_simplefield  # noqa
from plone.app.contenttypes.migration.migration import BlobFileMigrator
from plone.app.contenttypes.migration.migration import BlobImageMigrator
from plone.app.contenttypes.migration.migration import DocumentMigrator
from plone.app.contenttypes.migration.migration import migrate
from plone.app.linkintegrity.utils import ensure_intid
from plone.dexterity.utils import createContentInContainer
from z3c.relationfield import RelationValue
from z3c.relationfield.event import _setRelation
from zope.component import getUtility
from zope.intid.interfaces import IIntIds


def migrate_richdocument(context, uninstall=False):
    cat = api.portal.get_tool('portal_catalog')
    portal = api.portal.get()

    # STEP1:
    # Move all SimpleAttachments to a "Media" Folder and migrate them to
    # standard Image/File types
    media_base = get_media_root(context)

    items = cat(portal_type=['FileAttachment', 'ImageAttachment'])
    _all = len(items)

    for no, att in enumerate(items, 1):
        obj = att.getObject()
        richdoc_uid = obj.aq_parent.UID()
        media_path = media_base.get(richdoc_uid)
        if media_path is None:
            media_path = createContentInContainer(
                media_base, 'Folder', id=richdoc_uid,
                title=obj.aq_parent.Title())
        api.content.move(source=obj, target=media_path)
        transaction.commit()
        logger.info("%s/%s moved %s -> %s", no, _all, obj.absolute_url(1), media_path.absolute_url(1))  # noqa

    migrate(portal, FileAttachmentMigrator)
    migrate(portal, ImageAttachmentMigrator)

    # STEP2:
    # Migrate RichDocument to standard Document with
    # collective.behavior.relatedmedia enabled and link migrated
    # SimpleAttachments as relatedmedia
    migrate(portal, RichDocumentMigrator)
    transaction.commit()

    # set related media folder
    intids = getUtility(IIntIds)
    for doc in cat(portal_type='Document'):
        if doc.UID not in media_base:
            continue
        media_path = media_base.get(doc.UID)
        target_id = ensure_intid(media_path, intids)
        rel = RelationValue(target_id)
        doc_obj = doc.getObject()
        # z3c.relations event
        _setRelation(doc_obj, 'related_media_base_path', rel)
        # set relation on behavior
        IRelatedMedia(doc_obj).related_media_base_path = rel
        logger.info("Linked %s -> %s", media_path.absolute_url(1), doc.getPath())  # noqa

    if uninstall:
        try:
            # old style uninstallation
            qi = api.portal.get_tool('portal_quickinstaller')
            qi.uninstallProducts([
                'RichDocument', 'SimpleAttachment',
                'Products.SimpleAttachment'])
        except Exception:
            pass


class FileAttachmentMigrator(BlobFileMigrator):

    src_portal_type = 'FileAttachment'
    src_meta_type = 'FileAttachment'
    dst_portal_type = 'File'
    dst_meta_type = None  # not used


class ImageAttachmentMigrator(BlobImageMigrator):

    src_portal_type = 'ImageAttachment'
    src_meta_type = 'ImageAttachment'
    dst_portal_type = 'Image'
    dst_meta_type = None  # not used


class RichDocumentMigrator(DocumentMigrator):

    src_portal_type = 'RichDocument'
    src_meta_type = 'RichDocument'
    dst_portal_type = 'Document'
    dst_meta_type = None  # not used
