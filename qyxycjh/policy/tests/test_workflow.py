# -*- coding: UTF-8 -*-
from dexterity.membrane.membrane_helpers import get_user_id_for_email
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.namedfile.file import NamedImage
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from qyxycjh.policy.tests.base import Base
from qyxycjh.policy.testing import FunctionalTesting


import os
import unittest


def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')


class TestView(Base):

    layer = FunctionalTesting

    def test_member_workflow(self):
        app = self.layer['app']
        portal = self.portal
        wf = getToolByName(portal, 'portal_workflow')
        wt = wf.dexterity_membrane_workflow
        dummy = portal['memberfolder1']['member1']
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

    def test_survey_workflow(self):
        app = self.layer['app']
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

# sponsor reject
        wf.doActionFor(dummy, 'reject', comment='object has been reject')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state, 'private')
# owner again submit to sponsor
        wf.doActionFor(dummy, 'submit', comment='submit to sponsor')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state, 'pending')

# owner retract to owner
        wf.doActionFor(dummy, 'retract', comment='owner retract to self')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state, 'private')



    def test_permission_workflow(self):
        app = self.layer['app']
        portal = self.portal
        wf = getToolByName(portal, 'portal_workflow')
        org = portal['orgnizationfolder1']['orgnization1']
        wts = wf.credit_survey_workflow
        survey = org['orgnizationsurvey1']
        wts.notifyCreated(survey)
        wt = wf.dexterity_membrane_workflow
        dummy = portal['memberfolder1']['member1']
        wf.notifyCreated(dummy)
        dummy.email = 'JOE@example.org'
        dummy.password = 'secret'
        dummy.confirm_password = 'secret'
        membrane = getToolByName(portal, 'membrane_tool')
        membrane.reindexObject(dummy)
        # Uppercase:
        user_id = get_user_id_for_email(portal, 'JOE@example.org')
        aclu = getToolByName(portal, 'acl_users')
        auth = aclu.membrane_users.authenticateCredentials
        credentials = {'login': 'JOE@example.org', 'password': 'secret'}
        # First the member needs to be enabled before authentication
        # can succeed.
        self.assertEqual(auth(credentials), None)
        wf_tool = getToolByName(self.layer['portal'], 'portal_workflow')
        login(self.layer['portal'], TEST_USER_NAME)
        setRoles(self.layer['portal'], TEST_USER_ID, ['Reviewer'])
        wf_tool.doActionFor(dummy, 'approve')
        logout()

        self.assertEqual(auth(credentials), (user_id, 'JOE@example.org'))
        memship = getToolByName(portal, 'portal_membership')
        joe_member = memship.getMemberById(user_id)
        self.assertTrue(joe_member)

        # At first, no one gets an extra local role, because the
        # members are not enabled.
        # Test roles of fresh joe:

        self.assertEqual(
            joe_member.getRolesInContext(self.layer['portal']),
            ['Organization', 'Authenticated']
        )
        self.assertEqual(
            joe_member.getRolesInContext(survey),
            ['Organization', 'Authenticated']
        )
        self.assertEqual(sorted(joe_member.getRolesInContext(dummy)),
                         ['Authenticated', u'Creator', u'Editor','Organization', u'Reader'])
