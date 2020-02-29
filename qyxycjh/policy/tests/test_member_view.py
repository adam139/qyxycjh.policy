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
from plone.namedfile.file import NamedImage
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from qyxycjh.policy.testing import FunctionalTesting
from qyxycjh.policy.testing import POLICY_INTEGRATION_TESTING
from zope.component import getUtility
from qyxycjh.policy.tests.base import Base
import hmac
import json
import os
import unittest


class TestView(Base):

    layer = FunctionalTesting

    def test_member_page(self):

        app = self.layer['app']
        portal = self.portal
        login(self.layer['portal'], TEST_USER_NAME)
        setRoles(self.layer['portal'], TEST_USER_ID, ['Manager'])              
        wf = getToolByName(portal, 'portal_workflow')
        wt = wf.dexterity_membrane_workflow
        dummy = portal['memberfolder']['member1']
        wf.notifyCreated(dummy)
        wf.doActionFor(dummy, 'approve', comment='foo')
        import transaction
        transaction.commit()
        logout()
        browser = Browser(app)
        browser.handleErrors = False        
        browser.open(portal.absolute_url() + '/login_form')
        browser.getControl(name='__ac_name').value = "12@qq.com"
        browser.getControl(name='__ac_password').value = "391124"
        browser.getControl(name='submit').click()        
        obj = '%s/@@view' % dummy.absolute_url()
        browser.open(obj)
        outstr = "I am member1"
        self.assertTrue(outstr in browser.contents)
        outstr = "12@qq.com"
        self.assertTrue(outstr in browser.contents)
        outstr = "++add++qyxycjh.policy.orgnizationsurvey"
        self.assertTrue(outstr in browser.contents)

    def test_ajax_member_state(self):
        request = self.layer['request']
        portal = self.portal
        wf = getToolByName(portal, 'portal_workflow')
        dummy = portal['memberfolder']['member2']
        review_state = wf.getInfoFor(dummy, 'review_state')
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
            '_authenticator': auth,
            'state': review_state,  # new created member initial status
            'id': 'member2',
        }

        view = self.portal['memberfolder'].restrictedTraverse(
            '@@ajaxmemberstate')
        result = view()

        self.assertEqual(json.loads(result), True)

    def test_member_workflow(self):
        app = self.layer['app']
        wf = getToolByName(self.portal, 'portal_workflow')
        wt = wf.dexterity_membrane_workflow
        dummy = self.portal['memberfolder']['member1']
        wf.notifyCreated(dummy)
        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] == 'dexterity_membrane_workflow')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state, 'pending')
        wf.doActionFor(dummy, 'approve', comment='foo')

# available variants is actor,action,comments,time, and review_history
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state, 'enabled')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment, 'foo')
