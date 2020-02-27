#-*- coding: UTF-8 -*-
import unittest
from qyxycjh.policy.testing import POLICY_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
from plone.namedfile.file import NamedImage

class Base(unittest.TestCase):
    layer = POLICY_INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']

        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('qyxycjh.policy.orgnizationfolder', 'orgnizationfolder1')
        portal['orgnizationfolder1'].invokeFactory('qyxycjh.policy.orgnization',
                                                    'orgnization1',
                                                   title="orgnization1")                                                     
        portal['orgnizationfolder1'].invokeFactory('qyxycjh.policy.governmentorgnization',
                                                    'sponsororgnization1',
                                                   title="sponsororgnization1") 
        
        portal['orgnizationfolder1']['orgnization1'].invokeFactory('qyxycjh.policy.orgnizationsurvey',
                                                    'orgnizationsurvey1',
                                                   title="orgnizationsurvey1")
        portal['orgnizationfolder1']['orgnization1'].invokeFactory('qyxycjh.policy.orgnizationsurvey',
                                                    'orgnizationsurvey2',
                                                   title="orgnizationsurvey2")              
        portal.invokeFactory('qyxycjh.policy.memberfolder','memberfolder1')
        portal['memberfolder1'].invokeFactory('qyxycjh.policy.organizationmember', 'member1',
                                              email="12@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',
                                              orgname='orgnization1',
                                              description="I am member1")
        portal['memberfolder1'].invokeFactory('qyxycjh.policy.organizationmember', 'member2',
                                              email="13@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',
                                              orgname='orgnization1',
                                              description="I am member1")

        portal['memberfolder1'].invokeFactory('qyxycjh.policy.organizationmember', 'member3',
                                              email="14@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',
                                              orgname='orgnization1',
                                              description="I am member1")

        portal['memberfolder1'].invokeFactory('qyxycjh.policy.organizationmember', 'member4',
                                              email="15@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',
                                              orgname='orgnization1',
                                              description="I am member1")

        portal['memberfolder1'].invokeFactory('qyxycjh.policy.organizationmember', 'member5',
                                              email="16@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',
                                              orgname='orgnization1',                                              
                                              description="I am member1")
        portal['memberfolder1'].invokeFactory('qyxycjh.policy.sponsormember', 'sponsor1',
                                              email="17@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',
                                              orgname='sponsororgnization1',                                              
                                              description="I am sponsor1") 
       
        self.portal = portal
        self.member1 = portal['memberfolder1']['member1']
        self.sponsor1 = portal['memberfolder1']['sponsor1']
                
 