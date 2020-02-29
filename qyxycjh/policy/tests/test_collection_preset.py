#-*- coding: UTF-8 -*-
import json
import hmac
from hashlib import sha1 as sha
from plone.keyring.interfaces import IKeyManager
from Products.CMFCore.utils import getToolByName

from qyxycjh.policy.testing import FunctionalTesting
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest


class TestView(unittest.TestCase):
    
    layer = FunctionalTesting
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        
    def test_sort_on(self):
# check collection sort_on,sort_reversed etc.        

        portal = self.layer['portal']
        item = portal['sqls']['xiehuidongtai']  
        self.assertTrue(item.sort_on == "created")
        self.assertTrue(item.sort_reversed == True)      

  