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
