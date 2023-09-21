from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import getAllUtilitiesRegisteredFor

import logging
import transaction

logger = logging.getLogger(__name__)
PACKAGE_NAME = "collective.behavior.relatedmedia"


def package_rename(context):
    profile_id = "profile-{0}:default".format(PACKAGE_NAME)
    oldreg_profile_id = "profile-{0}:package_rename".format(PACKAGE_NAME)
    # remove old registry entries
    context.runAllImportStepsFromProfile(oldreg_profile_id)
    # add new registry
    context.runImportStepFromProfile(profile_id, "plone.app.registry")


def local_gallery_configuration(context):
    update_profile_id = "profile-{0}:local_config".format(PACKAGE_NAME)
    context.runAllImportStepsFromProfile(update_profile_id)


def registry_cleanup(context):
    update_profile_id = "profile-{0}:registry_cleanup".format(PACKAGE_NAME)
    context.runAllImportStepsFromProfile(update_profile_id)


def migrate_base_path_relations(context):
    from collective.behavior.relatedmedia.behavior import IRelatedMediaBehavior

    catalog = api.portal.get_tool("portal_catalog")
    items = catalog(
        object_provides="collective.behavior.relatedmedia.behavior.IRelatedMedia",
    )
    _num_items = len(items)

    for idx, item in enumerate(items, 1):
        obj = item.getObject()

        try:
            base_path = IRelatedMediaBehavior(obj).related_media_base_path
        except TypeError:
            logger.info(f"{idx}/{_num_items} no relatedmedia behavior registered for {item.getPath()}.")
            continue

        if not base_path:
            logger.info(f"{idx}/{_num_items} skip migration of {item.getPath()} -> no base path defined.")
            continue

        logger.info(f"{idx}/{_num_items} migrating {item.getPath()}.")

        for media in catalog(path=base_path.to_path):
            # related images
            if media.portal_type == "Image":
                img_obj = media.getObject()
                api.relation.create(source=obj, target=img_obj, relationship="related_images")
                logger.info(f" - related_image {media.getPath()} created")
                continue
            # related attachments
            if media.portal_type == "File":
                file_obj = media.getObject()
                api.relation.create(source=obj, target=file_obj, relationship="related_attachments")
                logger.info(f" - related_attachment {media.getPath()} created")
                continue
            logger.info(f" - no relation created for unknown type {media.getPath()}...")

        # remove base_path information
        IRelatedMediaBehavior(obj).related_media_base_path = None
        transaction.commit()


def migrate_behavior_name(context):
    ftis = getAllUtilitiesRegisteredFor(IDexterityFTI)

    for fti in ftis:
        updated_fti = []
        for behavior in fti.behaviors:
            if behavior in updated_fti:
                continue
            if behavior == 'collective.behavior.relatedmedia.behavior.IRelatedMedia':
                updated_fti.append('collective.relatedmedia')
            else:
                updated_fti.append(behavior)
        fti.behaviors = tuple(updated_fti)


