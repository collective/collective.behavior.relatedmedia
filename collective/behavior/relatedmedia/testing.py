# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2

try:
    # Python 2: "unicode" is built-in
    unicode
except NameError:
    unicode = str


class CollectiveBehaviorRelatedMediaLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import collective.behavior.relatedmedia
        self.loadZCML(package=collective.behavior.relatedmedia)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.behavior.relatedmedia:default')


COLLECTIVE_BEHAVIOR_RELATEDMEDIA_FIXTURE = CollectiveBehaviorRelatedMediaLayer()


COLLECTIVE_BEHAVIOR_RELATEDMEDIA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_BEHAVIOR_RELATEDMEDIA_FIXTURE,),
    name='CollectiveBehaviorRelatedMediaLayer:IntegrationTesting',
)

COLLECTIVE_BEHAVIOR_RELATEDMEDIA_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_BEHAVIOR_RELATEDMEDIA_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveBehaviorRelatedMediaLayer:AcceptanceTesting',
)
