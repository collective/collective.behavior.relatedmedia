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
