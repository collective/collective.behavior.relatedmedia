# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.behavior.relatedmedia.testing import (  # noqa
    COLLECTIVE_BEHAVIOR_RELATEDMEDIA_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

import unittest


no_get_installer = False

try:
    from Products.CMFPlone.utils import get_installer
except Exception:
    # Quick shim for 5.1 api change

    class get_installer(object):
        def __init__(self, portal, request):
            self.installer = getToolByName(portal, "portal_quickinstaller")

        def is_product_installed(self, name):
            return self.installer.isProductInstalled(name)

        def uninstall_product(self, name):
            return self.installer.uninstallProducts([name])


class TestSetup(unittest.TestCase):
    """Test that collective.behavior.relatedmedia is properly installed."""

    layer = COLLECTIVE_BEHAVIOR_RELATEDMEDIA_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.behavior.relatedmedia is installed."""
        self.assertTrue(
            self.installer.is_product_installed("collective.behavior.relatedmedia")
        )


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_BEHAVIOR_RELATEDMEDIA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.behavior.relatedmedia")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.behavior.relatedmedia is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed("collective.behavior.relatedmedia")
        )
