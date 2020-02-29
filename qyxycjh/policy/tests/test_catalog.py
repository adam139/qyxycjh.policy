# -*- coding: UTF-8 -*-
"""refer  the plone.app.discussion catalog indexes
"""
from datetime import datetime
from dexterity.membrane import indexers as catalog
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.indexer.delegate import DelegatingIndexerFactory
from Products.CMFCore.utils import getToolByName
from qyxycjh.policy.testing import POLICY_INTEGRATION_TESTING
from zope import event
from zope.annotation.interfaces import IAnnotations
from zope.component import createObject
from qyxycjh.policy.tests.base import Base

import transaction
import unittest


class CatalogSetupTest(Base):

    layer = POLICY_INTEGRATION_TESTING


    def test_catalog_installed(self):
        self.assertTrue('email' in
                        self.portal.portal_catalog.indexes())
        self.assertTrue('Title' in
                        self.portal.portal_catalog.indexes())

    def test_conversation_total_comments(self):
        self.assertTrue(isinstance(catalog.Title,
                                   DelegatingIndexerFactory))
        self.assertTrue(isinstance(catalog.member_email,
                                   DelegatingIndexerFactory))
        p0 = self.portal['memberfolder']['member1']
        p1 = self.portal['memberfolder']['member2']
        p2 = self.portal['memberfolder']['sponsor1']
        self.assertEqual(catalog.Title(p0)(), u"tangyuejun")
        self.assertEqual(catalog.Title(p1)(), u"tangyuejun")
        self.assertEqual(catalog.Title(p2)(), u"tangyuejun")
        self.assertEqual(catalog.member_email(p0)(), "12@qq.com")
        self.assertEqual(catalog.member_email(p1)(), "13@qq.com")
        self.assertEqual(catalog.member_email(p2)(), "100@qq.com")

    def test_catalogsearch(self):
        catalog2 = getToolByName(self.portal, 'portal_catalog')
        results2 = list(catalog2({'email': "12@qq.com"}))
        self.assertEqual(len(results2), 1)

        results2 = list(catalog2({'email': "100@qq.com"}))
        self.assertEqual(len(results2), 1)
        results2 = list(catalog2({'Title': u"tangyuejun"}))

        self.assertEqual(len(results2), 6)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
