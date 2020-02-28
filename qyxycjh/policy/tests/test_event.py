# -*- coding: UTF-8 -*-
from dexterity.membrane.membrane_helpers import get_user_id_for_email
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.namedfile.file import NamedImage
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from qyxycjh.policy.testing import FunctionalTesting
from qyxycjh.policy.testing import POLICY_INTEGRATION_TESTING
from zope import event
from zope.lifecycleevent import IObjectAddedEvent
from zope.lifecycleevent import ObjectAddedEvent
from qyxycjh.policy.tests.base import Base
import os
import unittest


class TestView(Base):
    layer = FunctionalTesting

    def test_update_operator(self):
        sorg = self.portal['orgnizationfolder1']['sponsororgnization1']
        self.assertEqual(sorg.operator, "100@qq.com")


    def test_org_adapter(self):
        from qyxycjh.policy.behaviors.org import IOrg
        app = self.layer['app']
        portal = self.layer['portal']
        member = portal['memberfolder1']['member1']
        org = portal['orgnizationfolder1']['orgnization1']
        path = IOrg(member).getOrgPath()
        lp = IOrg(member).getOrgBn().orgnization_legalPerson
        sr = IOrg(member).getOrgBn().orgnization_supervisor
        self.assertEqual(lp, u"张三")
        self.assertEqual(sr, u"企业信用促进会")
        self.assertEqual(path, org.absolute_url())
