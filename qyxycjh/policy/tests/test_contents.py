#-*- coding: UTF-8 -*-
import unittest
from qyxycjh.policy.testing import POLICY_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
from plone.namedfile.file import NamedImage
from qyxycjh.policy.tests.base import Base

class Allcontents(Base):
    layer = POLICY_INTEGRATION_TESTING   

                
    def test_folder_types(self):
        self.assertEqual(self.portal['orgnizationfolder1'].id,'orgnizationfolder1')        
        self.assertEqual(self.portal['orgnizationfolder1']['sponsororgnization1'].id,'sponsororgnization1')
        self.assertEqual(self.portal['orgnizationfolder1']['orgnization1'].id,'orgnization1')
        self.assertEqual(self.portal['memberfolder1'].id,'memberfolder1') 
    
    def test_item_types(self):
        self.assertEqual(self.portal['orgnizationfolder1']['orgnization1']['orgnizationsurvey1'].id,'orgnizationsurvey1')
        self.assertEqual(self.portal['orgnizationfolder1']['orgnization1']['orgnizationsurvey2'].id,'orgnizationsurvey2')

    def test_item_types(self):
        self.assertEqual(self.member1.email,'12@qq.com')
        self.assertEqual(self.sponsor1.email,'17@qq.com')
           
        