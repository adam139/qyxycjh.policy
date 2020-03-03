# -*- coding: UTF-8 -*-
from dexterity.membrane.content.member import IMember
from qyxycjh.policy.content.governmentdepartment import IOrgnization
from qyxycjh.policy.content.orgnizationfolder import IOrgnizationFolder
from qyxycjh.policy.interfaces import ICreateOrgEvent
from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent
from zope.component import getMultiAdapter
from zope.site.hooks import getSite
from plone.dexterity.utils import createContentInContainer

def CreateOrgEvent(event):
    """this event be fired by member join event, username,address password parameters to create a membrane object"""
    site = getSite()
     
    catalog = getToolByName(site,'portal_catalog')
    try:
        newest = catalog.unrestrictedSearchResults(
                {'object_provides': IOrgnizationFolder.__identifier__})
    except:
        return      

    memberfolder = newest[0].getObject()       
    try:
        item =createContentInContainer(memberfolder,
                                       "qyxycjh.policy.orgnization",
                                       checkConstraints=False,
                                       id=event.id)
#        setattr(memberfolder,'registrant_increment',memberid)
        item.title = event.title
        item.description = event.description
        item.address = event.address
        item.legal_person = event.legal_person 
        item.supervisor = event.supervisor
        item.register_code = event.register_code
        
        import datetime
        datearray = event.passDate.split('-')
        if len(datearray) >= 3:
            val = map(int,datearray)               
            item.passDate = datetime.date(*val)  
        else:
            item.passDate = datetime.date.today()
        item.reindexObject()                     
    except:
        return

def getMember(context, email):
    "get member object from email"
    catalog = getToolByName(context, "portal_catalog")
    memberbrains = catalog(object_provides=IMember.__identifier__,
                           email=email)

    if len(memberbrains) == 0:
        return None
    return memberbrains[0].getObject()


def updateSponsorOperator(obj, event):
    "创建sponsormember对象时，触发，更新该sponsormember关联的governmentorganization的operator记录"

    catalog = getToolByName(obj, 'portal_catalog')
    bns = catalog.unrestrictedSearchResults({'object_provides': IOrgnization.__identifier__,
                                             'id': obj.orgname})
    if bns:
        org = bns[0].getObject()
        org.operator = obj.email
        org.reindexObject()
    else:
        pass


def userLoginedIn(event):
    """Redirects  logged in users to getting started wizard"""

    portal = getSite()
    user = event.object
    email = user.getUserName()
    if "@" not in email:
        return
    # check if is sponsor
    # check if we have an access to request object
    request = getattr(portal, 'REQUEST', None)
    if not request:
        return
    # now complile and render our expression to url
    catalog = getToolByName(portal, 'portal_catalog')

    try:
        bn = catalog({'object_provides': IMember.__identifier__, "email": email})[0]
        url = bn.getURL()
#         url = member_url_view()
    except Exception, e:
        logException(u'Error during user login in redirect')
        return
    else:
        # check if came_from is not empty, then clear it up, otherwise further
        # Plone scripts will override our redirect
        if request.get('came_from'):
            request['came_from'] = ''
            request.form['came_from'] = ''
        request.RESPONSE.redirect(url)
