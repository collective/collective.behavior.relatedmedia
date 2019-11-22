# -*- coding: utf-8 -*-
from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2
from Products.PluginIndexes.BooleanIndex.BooleanIndex import BooleanIndex

import json

try:
    # Python 2: "unicode" is built-in
    unicode
except NameError:
    unicode = str


def _set_ajax_enabled(should_enable_ajax):
    pattern_options = api.portal.get_registry_record("plone.patternoptions")
    data = {"collectionfilter": unicode(json.dumps({"ajaxLoad": should_enable_ajax}))}
    pattern_options.update(data)
    api.portal.set_registry_record("plone.patternoptions", pattern_options)


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

        catalog = api.portal.get_tool(name='portal_catalog')
        if 'exclude_from_nav' not in catalog.indexes():
            catalog.addIndex(
                'exclude_from_nav',
                BooleanIndex('exclude_from_nav'),
            )

        with api.env.adopt_roles(['Manager']):
            portal.invokeFactory(
                'Document',
                id='testdocument',
                title=u'Test Document for Related Media',
            )


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


class CollectiveBehaviorRelatedMediaAjaxEnabledLayer(CollectiveBehaviorRelatedMediaLayer):
    def setUpPloneSite(self, portal):
        _set_ajax_enabled(True)
        super(CollectiveBehaviorRelatedMediaAjaxEnabledLayer, self).setUpPloneSite(portal)

AJAX_ENABLED_FIXTURE = CollectiveBehaviorRelatedMediaAjaxEnabledLayer()
COLLECTIVE_BEHAVIOR_RELATEDMEDIA_ACCEPTANCE_TESTING_AJAX_ENABLED = FunctionalTesting(
    bases=(
        AJAX_ENABLED_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveBehaviorRelatedMediaLayer:AcceptanceTesting_AjaxEnabled',
)


class CollectiveBehaviorRelatedMediaAjaxDisabledLayer(CollectiveBehaviorRelatedMediaLayer):
    def setUpPloneSite(self, portal):
        _set_ajax_enabled(False)
        super(CollectiveBehaviorRelatedMediaAjaxDisabledLayer, self).setUpPloneSite(portal)


AJAX_DISABLED_FIXTURE = CollectiveBehaviorRelatedMediaAjaxDisabledLayer()
COLLECTIVE_BEHAVIOR_RELATEDMEDIA_ACCEPTANCE_TESTING_AJAX_DISABLED = FunctionalTesting(
    bases=(
        AJAX_DISABLED_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveBehaviorRelatedMediaLayer:AcceptanceTesting_AjaxDisabled',
)
