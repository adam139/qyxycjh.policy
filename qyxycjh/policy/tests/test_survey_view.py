# -*- coding: UTF-8 -*-
from hashlib import sha1 as sha
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.keyring.interfaces import IKeyManager

from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from qyxycjh.policy.testing import FunctionalTesting
from qyxycjh.policy.testing import POLICY_INTEGRATION_TESTING
from zope.component import getUtility
from qyxycjh.policy.tests.base import Base
import datetime
import hmac
import json
import unittest

class TestProductlView(Base):
    layer = FunctionalTesting

    def test_ajax_submit_sponsor(self):
        request = self.layer['request']
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
            '_authenticator': auth,
            'subject': u"请审批",

        }
# Look up and invoke the view via traversal
        context = self.portal['organizations']['orgnization1']['orgnizationsurvey1']
        view = context.restrictedTraverse('@@ajax_submit_sponsor')
        result = view()
        self.assertEqual(json.loads(result)['result'], True) 

    def test_ajax_sponsor_reject(self):
        request = self.layer['request']
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
            '_authenticator': auth,
            'subject': u"某处有问题",
        }
# Look up and invoke the view via traversal
        context = self.portal['organizations']['orgnization1']['orgnizationsurvey1']
        self.wf.doActionFor(
            context,
            'submit',
            comment=request.form['subject'])
        view = context.restrictedTraverse('@@ajax_sponsor_reject')
        result = view()
        self.assertEqual(json.loads(result)['result'], True)

    def test_ajax_sponsor_agree(self):
        request = self.layer['request']
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
            '_authenticator': auth,
            'subject': u"基本可以",
            'quality':"hege"
        }
# Look up and invoke the view via traversal
        context = self.portal['organizations']['orgnization1']['orgnizationsurvey1']
        self.wf.doActionFor(
            context,
            'submit',
            comment=request.form['subject'])
        view = context.restrictedTraverse('@@ajax_sponsor_agree')
        result = view()
        self.assertEqual(json.loads(result)['result'], True)


# agent retract
    def test_ajax_agent_retract(self):
        request = self.layer['request']
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
            '_authenticator': auth,
            'subject': u"基本可以",
        }
# Look up and invoke the view via traversal
        context = self.portal['organizations']['orgnization1']['orgnizationsurvey1']
        self.wf.doActionFor(
            context,
            'submit',
            comment=request.form['subject'])
        self.wf.doActionFor(
            context,
            'publish',
            comment=request.form['subject'])
        view = context.restrictedTraverse('@@ajax_agent_retract')
        result = view()
        self.assertEqual(json.loads(result)['result'], True)


    def test_draft_view(self):

# 启用member1
        app = self.layer['app']
        portal = self.portal
        wf = getToolByName(portal, 'portal_workflow')
        wt = self.wf.dexterity_membrane_workflow
        dummy = portal['memberfolder']['member1']
        self.wf.notifyCreated(dummy)
        chain = self.wf.getChainFor(dummy)
        self.failUnless(chain[0] == 'dexterity_membrane_workflow')
        review_state = self.wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state, 'pending')
        self.wf.doActionFor(dummy, 'approve', comment='foo')

# 启用监管账号

        dummy = portal['memberfolder']['sponsor1']
        obj = portal['organizations']['orgnization1']['orgnizationsurvey1']
        self.wf.notifyCreated(dummy)
        self.wf.notifyCreated(obj)
        chain = self.wf.getChainFor(dummy)
        self.failUnless(chain[0] == 'dexterity_membrane_workflow')
        review_state = self.wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state, 'pending')
        self.wf.doActionFor(dummy, 'approve', comment='foo')
        import transaction
        transaction.commit()
        logout()
        browser = Browser(app)
        browser.handleErrors = False
        browser.open(portal.absolute_url() + '/login_form')
        browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
        browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
        browser.getControl(name='submit').click()

        page = obj.absolute_url() + '/@@draftview'
        browser.open(page)
#        监管单位经手
        outstr = 'orgnizationsurvey1'
        self.assertTrue(outstr in browser.contents)

    def test_pending_view(self):

# 启用member1
        app = self.layer['app']
        portal = self.portal
        wf = getToolByName(portal, 'portal_workflow')
        wt = self.wf.dexterity_membrane_workflow
        dummy = portal['memberfolder']['member1']
        self.wf.notifyCreated(dummy)
        chain = self.wf.getChainFor(dummy)
        self.failUnless(chain[0] == 'dexterity_membrane_workflow')
        review_state = self.wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state, 'pending')
        self.wf.doActionFor(dummy, 'approve', comment='foo')
        
# 启用监管账号
        dummy = portal['memberfolder']['sponsor1']
        obj = portal['organizations']['orgnization1']['orgnizationsurvey1']
        self.wf.notifyCreated(dummy)
        self.wf.notifyCreated(obj)
        chain = self.wf.getChainFor(dummy)
        self.failUnless(chain[0] == 'dexterity_membrane_workflow')
        review_state = self.wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state, 'pending')
        self.wf.doActionFor(dummy, 'approve', comment='foo')
        import transaction
        transaction.commit()
        logout()
        browser = Browser(app)
        browser.handleErrors = False           

        browser.open(portal.absolute_url() + '/login_form')
        browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
        browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
        browser.getControl(name='submit').click()

# sponsor view
        page = obj.absolute_url() + '/@@sponsorview'
        browser.open(page)
#        监管单位经手
        outstr = 'orgnizationsurvey1'
        self.assertTrue(outstr in browser.contents)


    def test_published_view(self):

# 启用member1
        app = self.layer['app']
        portal = self.portal
        wf = getToolByName(portal, 'portal_workflow')
        wt = self.wf.dexterity_membrane_workflow
        dummy = portal['memberfolder']['member1']
        self.wf.notifyCreated(dummy)
        chain = self.wf.getChainFor(dummy)
        self.failUnless(chain[0] == 'dexterity_membrane_workflow')
        review_state = self.wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state, 'pending')
        self.wf.doActionFor(dummy, 'approve', comment='foo')
        
# 启用监管账号
        dummy = portal['memberfolder']['sponsor1']
        obj = portal['organizations']['orgnization1']['orgnizationsurvey1']
        self.wf.notifyCreated(dummy)
        self.wf.notifyCreated(obj)
        chain = self.wf.getChainFor(dummy)
        self.failUnless(chain[0] == 'dexterity_membrane_workflow')
        review_state = self.wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state, 'pending')
        self.wf.doActionFor(dummy, 'approve', comment='foo')
        import transaction
        transaction.commit()
        logout()
        browser = Browser(app)
        browser.handleErrors = False           

        browser.open(portal.absolute_url() + '/login_form')
        browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
        browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
        browser.getControl(name='submit').click()
# # published view
        page = obj.absolute_url() + '/@@publishedview'
        browser.open(page)
#        监管单位经手
        outstr = 'id="review-history"'
        self.assertTrue(outstr in browser.contents)
        outstr = 'orgnizationsurvey1'
        self.assertTrue(outstr in browser.contents)

