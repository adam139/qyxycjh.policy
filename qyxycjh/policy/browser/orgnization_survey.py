#-*- coding: UTF-8 -*-
from zope.component import getMultiAdapter
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.viewlet.interfaces import IViewlet

from five import grok
import datetime
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions

from plone.app.customerize import registration
from plone.memoize.instance import memoize

from qyxycjh.policy import _
from qyxycjh.policy.content.orgnization import IOrgnization
from qyxycjh.policy.content.annualsurvey import IOrgnization_annual_survey
from qyxycjh.policy.content.orgnizationfolder import IOrgnizationFolder
from dexterity.membrane.content.member import IMember
from qyxycjh.policy.content.member import IOrganizationMember
from qyxycjh.policy.content.member import ISponsorMember
from qyxycjh.policy.behaviors.org import IOrg

grok.templatedir('templates') 

class SurveyView(grok.View):
    grok.context(IOrgnization_annual_survey)
    grok.template('survey_draft_view')
    grok.name('baseview')
    grok.require('zope2.View')
#    
#    def render(self):
#        "this is view base class,this function should be override by subclass using template or render."
      
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)

    @memoize    
    def catalog(self):
        context = aq_inner(self.context)

        pc = getToolByName(context, "portal_catalog")
        return pc
    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm
    
    @memoize    
    def wf(self):
        context = aq_inner(self.context)
        wf = getToolByName(context, "portal_workflow")
        return wf        
            
    @property
    def isEditable(self):
        from Products.CMFCore.permissions import ModifyPortalContent
        return self.pm().checkPermission(ModifyPortalContent,self.context)
    

    
    def formatDatetime(self,Datetimeobj):
        "format Datetime obj to:2015年02月08日"
        year = Datetimeobj.strftime('%Y')
        month = Datetimeobj.strftime('%m')
        day = Datetimeobj.strftime('%d')
        return u"%s年%s月%s日" % (year,month,day)
            
    def created(self):
        "get current context created time. format:2015年02月08日"
        created = self.context.created()
        return self.formatDatetime(created)

    def canbeAuditBySponsor(self):
        status = self.workflow_state()
# checkPermission function must be use Title style permission
        canbe = self.pm().checkPermission("qyxycjh.policy:Review anual report",self.context)
        return (status == 'pending') and canbe

    
    def canbeAuditByAgent(self):
        status = self.workflow_state()
# checkPermission function must be use Title style permission
        canbe = self.pm().checkPermission("qyxycjh.policy:Review lastly anual report",self.context)
        return (status == 'pendingagent') and canbe

    
    def canbeSubmit(self):
        status = self.workflow_state()
# checkPermission function must be use Title style permission
        canbe = self.pm().checkPermission("qyxycjh.policy:Add anual report",self.context)
        return (status == 'private') and canbe and not self.canbeSubmitAgent()
    
    def canbeSubmitAgent(self,sponsor=u"市民政局"):
        status = self.workflow_state()
# checkPermission function must be use Title style permission
        canbe = self.pm().checkPermission("qyxycjh.policy:Add anual report",self.context)
        spon = self.getSponsorOrg()
        base = (status == 'private') and canbe
        if (spon == sponsor):        
            return base
        else:
            return base and (self.context.last_status == "pendingagent")  

    
    def canbeRetract(self):
        status = self.workflow_state()
# checkPermission function must be use Title style permission
        canbe = self.pm().checkPermission("qyxycjh.policy:Review lastly anual report",self.context)
        return (status == 'published') and canbe
              
        
    def getCurrentMember(self):
        member_data = self.pm().getAuthenticatedMember()
        id = member_data.getUserName()
#        id = "12@qq.com"   # 测试时适应
        query = {"object_provides":IMember.__identifier__,'email':id}
        bns = self.catalog()(query)
        if bns:
            member = bns[0]
            return member
        else:
            return None

    @memoize
    def getSponsorOrg(self):
        "获取上级监管单位名称"
        
        sid = self.context.sponsor
        if sid: return sid
        try:
            sponsor = IOrg(self.getCurrentMember().getObject()).getSponsor()
            self.context.sponsor = sponsor
            return sponsor
        except:
            return ""
        
    def dateformatTransfer(self,old):
        "转换2012-02-12为2012年02月12日"
        lt = old.split("-")
        new = "%s年%s月%s日"  % (lt[0],lt[1],lt[2])
        return new
    
    def getSponsorAuditDate(self):
        "获取审核日期"
        
        old = self.context.sponsor_audit_date
        if old == "" or old ==None:return ""
        return self.dateformatTransfer(old)       
        
    def getSponsorOperator(self):
        "获取经收人姓名"
        return self.email2Title(self.getSponsorOperatorEmail())
    
    @memoize
    def getSponsorOperatorEmail(self):
        "获取上级监管单位的经手人，该经手人，在启用该监管单位账号时，由事件更新返回邮件地址"
               
        sponsor = self.getSponsorOrg()
        if not sponsor:return None
        from qyxycjh.policy.content.governmentdepartment import IOrgnization
        # 获得该政府部门
        query = {"object_provides":IOrgnization.__identifier__,'Title':sponsor}
        bs = self.catalog()(query)     
        if bs: 
            email = bs[0].getObject().operator
            return email
        return None
    
    def email2Title(self,email):
        "根据登陆邮件地址，查询用户名"
        
        query = {"object_provides":IMember.__identifier__,'email':email}
        bns = self.catalog()(query)
        if bns:
            member = bns[0]
            return member.Title
        else:
            return email        
        
    def getOrg(self):
        "获取协会对象,它是年检对象的父对象。"
        org = aq_parent(self.context)
        return org
             
    def getLegalPerson(self):
        "获取该协会的法人名称，协会对象是年检对象的父对象。"
#        org = aq_parent(self.context)
        return self.getOrg().legal_person
        
    def getAgentOrg(self):
        "获取民政局,为民政局 单位对象指定id:minzhengju,以此简便获取到民政局对象"
        
        from qyxycjh.policy.content.governmentdepartment import IOrgnization
        # 获得该政府部门
        query = {"object_provides":IOrgnization.__identifier__,'id':"minzhengju"}
        bs = self.catalog()(query)
#        import pdb
#        pdb.set_trace()        
        if bs: return bs[0].Title
        return None
    
    def getAgentAuditDate(self):
        "获取民政局审核日期"
        old = self.context.sponsor_audit_date
        if old == "" or old ==None:return ""
        return self.dateformatTransfer(old)
    
    @memoize
    def getAgentOperator(self):
        "获取民政局经手人"
        return self.email2Title(self.getAgentOperatorEmail())
            
    @memoize
    def getAgentOperatorEmail(self):
        "获取民政局经手人邮件"
        from qyxycjh.policy.content.governmentdepartment import IOrgnization
        # 获得该政府部门
        query = {"object_provides":IOrgnization.__identifier__,'id':"minzhengju"}
        bs = self.catalog()(query)
        if bs: 
            email = bs[0].getObject().operator
            return email
        return None
    
    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(self.context,'translation_service')
        title = translation_service.translate(
                                                  value,
                                                  domain='qyxycjh.policy',
                                                  mapping={},
                                                  target_language='zh_CN',
                                                  context=self.context,
                                                  default="")
        return title   
        
    def fromid2title(self,id):
        """根据对象id，获得对象title"""
                
        brains = self.catalog()({'id':id})
        if len(brains) >0:
            return brains[0].Title
        else:
            return id
        
    def creator(self):
        "get survey report's creator"
        creator = self.context.creators[0]
        return creator
    
    def workflow_state(self):
        "context workflow status"
        context = self.context
        review_state = self.wf().getInfoFor(context, 'review_state')
        return review_state
    
    def workflowHistory(self, complete=True):
        """Return workflow history of this context.

        Taken from plone_scripts/getWorkflowHistory.py
        """
        context = aq_inner(self.context)
        # check if the current user has the proper permissions
#        if not (_checkPermission('Request review', context) or
#            _checkPermission('Review portal content', context)):
#            return []

        workflow = self.wf()
        membership = self.pm()
        review_history = []
        try:
            # get total history
            review_history = workflow.getInfoFor(context, 'review_history')
            if not complete:
                # filter out automatic transitions.
                review_history = [r for r in review_history if r['action']]
            else:
                review_history = list(review_history)

            portal_type = context.portal_type
            anon = _(u'label_anonymous_user', default=u'Anonymous User')
            for r in review_history:
                r['type'] = 'workflow'
                r['transition_title'] = workflow.getTitleForTransitionOnType(
                    r['action'], portal_type) or _("Create")
                r['state_title'] = workflow.getTitleForStateOnType(
                    r['review_state'], portal_type)
                actorid = r['actor']
                r['actorid'] = actorid
                if actorid is None:
                    # action performed by an anonymous user
                    r['actor'] = {'username': anon, 'fullname': anon}
                    r['actor_home'] = ''
                else:
                    r['actor'] = membership.getMemberInfo(actorid)
                    if r['actor'] is not None:
                        r['actor_home'] = self.navigation_root_url + '/author/' + actorid
                    else:
                        # member info is not available
                        # the user was probably deleted
                        r['actor_home'] = ''
            review_history.reverse()

        except WorkflowException:
            log('plone.app.layout.viewlets.content: '
                '%s has no associated workflow' % context.absolute_url(),
                severity=logging.DEBUG)

        return review_history
    
    
    @memoize         
    def getOrgnizationFolder(self):

        topicfolder = self.catalog()({'object_provides': IOrgnizationFolder.__identifier__})

        canManage = self.pm().checkPermission(permissions.AddPortalContent,self.context)        
        if (len(topicfolder) > 0) and  canManage:
            tfpath = topicfolder[0].getURL()
        else:
            tfpath = None            
        return tfpath
    
### load viewlet
    def __getitem__(self,name):
        viewlet = self.setUpViewletByName(name)
        if viewlet is None:
            active_layers = [ str(x) for x in self.request.__provides__.__iro__]
            active_layers = tuple(active_layers)
            raise RuntimeError("Viewlet does not exist by name %s for the active theme "% name)
        viewlet.update()
        return viewlet.render()
    
    def getViewletByName(self,name):
        views = registration.getViews(IBrowserRequest)
        for v in views:
            if v.provided == IViewlet:
                if v.name == name:
#                    if str(v.required[1]) == '<InterfaceClass plone.app.discussion.interfaces.IDiscussionLayer>':
                        return v
        return None
    
    def setUpViewletByName(self,name):
        context = aq_inner(self.context)
        request = self.request
        reg = self.getViewletByName(name)
        if reg == None:
            return None
        factory = reg.factory
        try:
            viewlet = factory(context,request,self,None).__of__(context)
        except TypeError:
            raise RuntimeError("Unable to initialize viewlet %s. Factory method %s call failed."% name)
        return viewlet    
         
class SurveyDraftView(SurveyView):
    """survey report view based workflow status: 'draft'"""
    grok.template('survey_draft_view')
    grok.name('draftview')
    grok.require('zope2.View')    

    
       
class SurveyPendingSponsorView(SurveyView):
    """survey report view based workflow status: 'pending'"""
    grok.template('survey_pending_sponsor_view')
    grok.name('sponsorview')
    grok.require('zope2.View')
#    
#    def render(self):
#        pass     
#    
class SurveyPendingAgentView(SurveyView):
    """survey report view based workflow status: 'pendingagent'"""
    grok.template('survey_pending_agent_view')
    grok.name('agentview')
    grok.require('zope2.View')             
#
#    def render(self):
#        pass
#
class SurveyPublishedView(SurveyView):
    """survey report view based workflow status: 'published'"""
    grok.template('survey_published_view')
    grok.name('publishedview')
    grok.require('zope2.View')
    

        




                 