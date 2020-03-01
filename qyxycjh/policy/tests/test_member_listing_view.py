# -*- coding: UTF-8 -*-
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.namedfile.file import NamedImage
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from qyxycjh.policy.testing import FunctionalTesting
from qyxycjh.policy.tests.base import Base
from Products.Five.utilities.marker import mark



class TestView(Base):

    layer = FunctionalTesting

    def test_member_listing_view(self):
        "adminb3_view"

        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader(
            'Authorization', 'Basic %s:%s' %
            (TEST_USER_NAME, TEST_USER_PASSWORD,))

        import transaction
        transaction.commit()
        obj = portal['memberfolder'].absolute_url() + '/@@admin_view'

        browser.open(obj)
        outstr = "12@qq.com"
        self.assertTrue(outstr in browser.contents)
        obj = portal['memberfolder'].absolute_url() + '/@@adminb3_view'

        browser.open(obj)
        outstr = u"企业"
        self.assertTrue(outstr in browser.contents)        
