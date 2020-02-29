#-*- coding: UTF-8 -*-
import unittest
from qyxycjh.policy.testing import POLICY_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
from plone.namedfile.file import NamedImage
from qyxycjh.policy.tests.base import Base
from plone.namedfile.testing import NamedFileTestLayer

class Allcontents(Base,NamedFileTestLayer):
    layer = POLICY_INTEGRATION_TESTING   

                
    def test_folder_types(self):
        self.assertEqual(self.portal['organizations'].id,'organizations')        
        self.assertEqual(self.portal['organizations']['sponsororgnization1'].id,'sponsororgnization1')
        self.assertEqual(self.portal['organizations']['orgnization1'].id,'orgnization1')
        self.assertEqual(self.portal['memberfolder'].id,'memberfolder') 
    
    def test_item_types(self):
        self.assertEqual(self.portal['organizations']['orgnization1']['orgnizationsurvey1'].id,'orgnizationsurvey1')
        self.assertEqual(self.portal['organizations']['orgnization1']['orgnizationsurvey2'].id,'orgnizationsurvey2')

    def test_item_types(self):
        self.assertEqual(self.member1.email,'12@qq.com')
        self.assertEqual(self.sponsor1.email,'100@qq.com')
           
        