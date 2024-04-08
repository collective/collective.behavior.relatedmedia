from plone import api
from plone.base.interfaces.controlpanel import dump_json_to_text
from plone.dexterity.interfaces import IDexterityFTI
from plone.registry.interfaces import IRegistry
from zope.component import getAllUtilitiesRegisteredFor
from zope.component import getUtility
from zope.lifecycleevent import modified

import json
import logging
import transaction


logger = logging.getLogger(__name__)
PACKAGE_NAME = "collective.behavior.relatedmedia"


def package_rename(context):
    profile_id = f"profile-{PACKAGE_NAME}:default"
    oldreg_profile_id = f"profile-{PACKAGE_NAME}:package_rename"
    # remove old registry entries
    context.runAllImportStepsFromProfile(oldreg_profile_id)
    # add new registry
    context.runImportStepFromProfile(profile_id, "plone.app.registry")


def local_gallery_configuration(context):
    update_profile_id = f"profile-{PACKAGE_NAME}:local_config"
    context.runAllImportStepsFromProfile(update_profile_id)


def registry_cleanup(context):
    update_profile_id = f"profile-{PACKAGE_NAME}:registry_cleanup"
    context.runAllImportStepsFromProfile(update_profile_id)


def migrate_base_path_relations(context):
    from collective.behavior.relatedmedia.behavior import IRelatedMediaBehavior

    catalog = api.portal.get_tool("portal_catalog")
    items = catalog(
        object_provides=[
            "collective.behavior.relatedmedia.interfaces.IRelatedMedia",  # old name
            IRelatedMediaBehavior.__identifier__,
        ]
    )
    _num_items = len(items)

    for idx, item in enumerate(items, 1):
        try:
            obj = item.getObject()
        except KeyError as msg:
            # there might be broken objects
            logger.warning(f"Could not migrate {item.getPath()}: {msg}")
            continue

        try:
            base_path = IRelatedMediaBehavior(obj).related_media_base_path
        except TypeError:
            logger.info(
                f"{idx}/{_num_items} no relatedmedia behavior registered for {item.getPath()}."
            )
            continue

        if not base_path:
            logger.info(
                f"{idx}/{_num_items} skip migration of {item.getPath()} -> no base path defined."
            )
            continue

        logger.info(f"{idx}/{_num_items} migrating {item.getPath()}.")

        # get existing relations and append them at the end.
        existing_rel_img = api.relation.get(source=obj, relationship="related_images")
        existing_rel_att = api.relation.get(
            source=obj, relationship="related_attachments"
        )
        obj.related_images = []
        obj.related_attachments = []

        for media in catalog(
            path={
                "query": base_path.to_path,
                "depth": 1,
            },
            sort_on="getObjPositionInParent",
        ):
            # related images
            if media.portal_type == "Image":
                img_obj = media.getObject()
                api.relation.create(
                    source=obj, target=img_obj, relationship="related_images"
                )
                logger.info(f" - related_image {media.getPath()} created")
                continue
            # related attachments
            if media.portal_type == "File":
                file_obj = media.getObject()
                api.relation.create(
                    source=obj, target=file_obj, relationship="related_attachments"
                )
                logger.info(f" - related_attachment {media.getPath()} created")
                continue
            logger.info(f" - no relation created for unknown type {media.getPath()}...")

        # append previously saved existing relations
        rel_img = obj.related_images
        for img in existing_rel_img:
            rel_img.append(img)
        obj.related_images = rel_img

        rel_att = obj.related_attachments
        for att in existing_rel_att:
            rel_att.append(att)
        obj.related_attachments = rel_att

        # remove base_path information
        IRelatedMediaBehavior(obj).related_media_base_path = None

        # necessary event for relation machinery
        modified(obj)

        transaction.commit()


def migrate_behavior_name(context):
    ftis = getAllUtilitiesRegisteredFor(IDexterityFTI)

    for fti in ftis:
        updated_fti = []
        for behavior in fti.behaviors:
            if behavior in updated_fti:
                continue
            if behavior == "collective.behavior.relatedmedia.behavior.IRelatedMedia":
                updated_fti.append("collective.relatedmedia")
            else:
                updated_fti.append(behavior)
        fti.behaviors = tuple(updated_fti)


def update_tinymce_settings(context):
    # first run registry updates
    context.runImportStepFromProfile(
        "profile-collective.behavior.relatedmedia:default",
        "plone.app.registry",
    )

    registry = getUtility(IRegistry)

    try:
        # cleanup old template if there
        templates = json.loads(registry["plone.templates"])
        clean_templates = []

        for tpl in templates:
            if tpl["title"] == "Gallery":
                continue
            clean_templates.append(tpl)

        registry["plone.templates"] = dump_json_to_text(clean_templates)

        if not len(clean_templates) and "template" in registry["plone.plugins"]:
            # remove plugin too
            plugins = registry["plone.plugins"]
            plugins.pop("template")
            registry["plone.plugins"] = plugins

    except Exception:
        logger.info("Could not read TinyMCE templates")
        return

    # add relatedimagesgallery tool
    toolbar = registry["plone.toolbar"]

    if "relatedimagesgallery" not in toolbar:
        toolbar = toolbar.replace(" ploneimage ", " ploneimage relatedimagesgallery ")

    registry["plone.toolbar"] = toolbar
