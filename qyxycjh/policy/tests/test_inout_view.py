#-*- coding: UTF-8 -*-
import json
import hmac
from hashlib import sha1 as sha
from plone.keyring.interfaces import IKeyManager
from Products.CMFCore.utils import getToolByName
from qyxycjh.policy.testing import FunctionalTesting
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.app.testing import logout
from plone.testing.z2 import Browser
import unittest
from zope.component import getUtility
from qyxycjh.policy.tests.base import Base

class TestView(Base):
    
    layer = FunctionalTesting

  
    def test_data(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/@@datainout-controlpanel'
        logout()   
        browser.open(obj)
        outstr = '<input type="file" name="csv_upload" />'
        self.assertTrue(outstr in browser.contents)
        
 