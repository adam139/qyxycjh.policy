#-*- coding: UTF-8 -*-
import unittest
import os
import datetime
from qyxycjh.policy.testing import POLICY_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
from plone import namedfile
from plone.namedfile.file import NamedImage
from Products.CMFCore.utils import getToolByName

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')


class Base(unittest.TestCase):
    layer = POLICY_INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']

        setRoles(portal, TEST_USER_ID, ('Manager',))

#         portal.invokeFactory('qyxycjh.policy.orgnizationfolder', 'organizations')
        portal['organizations'].invokeFactory('qyxycjh.policy.orgnization',
                                                    'orgnization1',
                                                   title="orgnization1",
                                                   legal_person=u"张三",
                                                   supervisor=u"企业信用促进会",
                                                   register_code="283832nb",
                                                   passDate=datetime.datetime.today())                                                     
        portal['organizations'].invokeFactory('qyxycjh.policy.governmentorgnization',
                                                    'sponsororgnization1',
                                                   title="sponsororgnization1",
                                                   description=u"企业信用促进会",
                                                   operator="17@qq.com") 
        
        portal['organizations']['orgnization1'].invokeFactory('qyxycjh.policy.orgnizationsurvey',
                                                    'orgnizationsurvey1',
                                                   title="orgnizationsurvey1",
                                                   sponsor="sponsororgnization1")
        portal['organizations']['orgnization1'].invokeFactory('qyxycjh.policy.orgnizationsurvey',
                                                    'orgnizationsurvey2',
                                                   title="orgnizationsurvey2")              
#         portal.invokeFactory('qyxycjh.policy.memberfolder','memberfolder')
        portal['memberfolder'].invokeFactory('qyxycjh.policy.organizationmember', 'member1',
                                              email="12@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',
                                              orgname='orgnization1',
                                              description="I am member1")
        portal['memberfolder'].invokeFactory('qyxycjh.policy.organizationmember', 'member2',
                                              email="13@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',
                                              orgname='orgnization1',
                                              description="I am member1")

        portal['memberfolder'].invokeFactory('qyxycjh.policy.organizationmember', 'member3',
                                              email="14@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',
                                              orgname='orgnization1',
                                              description="I am member1")

        portal['memberfolder'].invokeFactory('qyxycjh.policy.organizationmember', 'member4',
                                              email="15@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',
                                              orgname='orgnization1',
                                              description="I am member1")

        portal['memberfolder'].invokeFactory('qyxycjh.policy.organizationmember', 'member5',
                                              email="16@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',
                                              orgname='orgnization1',                                              
                                              description="I am member1")
        portal['memberfolder'].invokeFactory('qyxycjh.policy.sponsormember', 'sponsor1',
                                              email="100@qq.com",
                                              last_name=u"唐",
                                              first_name=u"岳军",
                                              title=u"tangyuejun",
                                              password="391124",
                                              confirm_password="391124",
                                              homepae='http://315ok.org/',
                                              orgname='sponsororgnization1',                                              
                                              description="I am sponsor1") 
        data = getFile('demo.txt').read()
        item = portal['organizations']['orgnization1']['orgnizationsurvey1']
        item.image = NamedImage(data, 'image/gif', u'image.gif')
        item.report = namedfile.NamedBlobFile(data, filename=u"demo.txt")       
        self.portal = portal
        self.member1 = portal['memberfolder']['member1']
        self.sponsor1 = portal['memberfolder']['sponsor1']
        self.wf = getToolByName(portal, 'portal_workflow')
                
 