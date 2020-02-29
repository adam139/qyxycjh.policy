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

        portal = self.portal
        wf = getToolByName(portal, 'portal_workflow')
        wt = wf.credit_survey_workflow
        org = portal['orgnizationfolder1']['orgnization1']
        dummy = org['orgnizationsurvey1']
        wf.notifyCreated(dummy)
        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] == 'credit_survey_workflow')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state, 'private')
        wf.doActionFor(dummy, 'submit', comment='submit to sponsor')
# available variants is actor,action,comments,time, and review_history
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state, 'pending')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment, 'submit to sponsor')

# sponsor agree
        wf.doActionFor(dummy, 'publish', comment='sponsor has been agree')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state, 'published')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment, 'sponsor has been agree')
        app = self.layer['app']
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        import transaction
        transaction.commit()        
        logout()
        obj = org.absolute_url() + '/@@view'   
        browser.open(obj)
        outstr = '283832nb'
        self.assertTrue(outstr in browser.contents)
        outstr = 'orgnizationsurvey1'
        self.assertTrue(outstr in browser.contents)        
        
 