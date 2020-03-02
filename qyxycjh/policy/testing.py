#-*- coding: UTF-8 -*-
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting,FunctionalTesting

from plone.testing import z2
from zope.configuration import xmlconfig

from plone.app.testing import (
IntegrationTesting,
FunctionalTesting,
login, logout, setRoles,
PLONE_FIXTURE,
TEST_USER_NAME,
SITE_OWNER_NAME,
)


class SitePolicy(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        import Products.membrane
        self.loadZCML(package=Products.membrane)
        z2.installProduct(app, 'Products.membrane')
        import dexterity.membrane
        import qyxycjh.policy
        import plone.app.contenttypes
        import qyxycjh.theme
        import my315ok.products
        import plone.namedfile

        xmlconfig.file('configure.zcml', plone.app.contenttypes, context=configurationContext)
        xmlconfig.file('configure.zcml', Products.membrane, context=configurationContext)        
        xmlconfig.file('configure.zcml', dexterity.membrane, context=configurationContext)
        xmlconfig.file('configure.zcml', my315ok.products, context=configurationContext)
        xmlconfig.file('configure.zcml', qyxycjh.theme, context=configurationContext)
        xmlconfig.file('configure.zcml', qyxycjh.policy, context=configurationContext)
        xmlconfig.file('configure.zcml', plone.namedfile, context=configurationContext)        
       
    
    def tearDownZope(self, app):

        z2.uninstallProduct(app, 'Products.membrane')        
        
    def setUpPloneSite(self, portal):

        applyProfile(portal, 'plone.app.contenttypes:default')
#         applyProfile(portal, 'Products.membrane:default') 
        applyProfile(portal, 'qyxycjh.policy:default')       
#         applyProfile(portal, 'dexterity.membrane:default')


class IntegrationSitePolicy(SitePolicy):      
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.contenttypes:default')        
#         applyProfile(portal, 'Products.membrane:default') 
        applyProfile(portal, 'qyxycjh.policy:default')
#         applyProfile(portal, 'dexterity.membrane:default')

        #make global request work
        from zope.globalrequest import setRequest
        setRequest(portal.REQUEST)
        # login doesn't work so we need to call z2.login directly
        z2.login(portal.__parent__.acl_users, SITE_OWNER_NAME)
#        setRoles(portal, TEST_USER_ID, ('Manager',))
#        login(portal, TEST_USER_NAME)
              
        self.portal = portal 

POLICY_FIXTURE = SitePolicy()
POLICY_INTEGRATION_FIXTURE = IntegrationSitePolicy()
POLICY_INTEGRATION_TESTING = IntegrationTesting(bases=(POLICY_INTEGRATION_FIXTURE,), name="Site:Integration")
FunctionalTesting = FunctionalTesting(bases=(POLICY_FIXTURE,), name="Site:FunctionalTesting")