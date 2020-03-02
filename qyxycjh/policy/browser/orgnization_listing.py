#-*- coding: UTF-8 -*-
from zope.component import getMultiAdapter
from five import grok
import json
import datetime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from plone.app.contenttypes.permissions import AddDocument  
from Products.CMFCore.interfaces import ISiteRoot
from plone.directives import dexterity
from plone.directives import form
from plone.memoize.instance import memoize
from qyxycjh.policy import _
from qyxycjh.policy.content.orgnization import IOrgnization
from qyxycjh.policy.content.annualsurvey import IOrgnization_annual_survey
from qyxycjh.policy.content.orgnizationfolder import IOrgnizationFolder
from qyxycjh.policy.browser.orgnization_survey import SurveyView
from qyxycjh.policy.browser.interfaces import IThemeSpecific

grok.templatedir('templates') 

class Orgnizations_adminView(grok.View):
    "social organizations list page"
    grok.context(IOrgnizationFolder)
    grok.template('orgnization_listing_admin')
    grok.name('listview')
    grok.layer(IThemeSpecific)
    grok.require('zope2.View')    
    
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
            
    @property
    def isEditable(self):      
        return self.pm().checkPermission(permissions.ManagePortal,self.context)
    
    @property
    def isAddable(self):
        return self.pm().checkPermission(permissions.AddPortalContent,self.context)     

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
        
    def pendingDefault(self):
        "计算缺省情况下，还剩多少条"
        total = len(self.allitems())
        if total > 10:
            return total -10
        else:
            return 0    
    
    @memoize         
    def getOrgnizationFolder(self):
        topicfolder = self.catalog()({'object_provides': IOrgnizationFolder.__identifier__})
        canManage = self.pm().checkPermission(permissions.AddPortalContent,self.context)        
        if (len(topicfolder) > 0) and  canManage:
            tfpath = topicfolder[0].getURL()
        else:
            tfpath = None            
        return tfpath        
        
    @memoize     
    def getMemberList(self):
        """获取社会组织列表"""
        mlist = []        
        memberbrains = self.catalog()({'object_provides':IOrgnization.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              )
        i = 0
        for brain in memberbrains:
            i = i+1           
            row = {'number':'','id':'', 'name':'', 'url':'',
                    'sponsor':'', 'orgnization_passDate':'', 'legal_person':'','address':'','register_code':'','editurl':'',
                    'delurl':''}
            row['number'] = i
            row['id'] = brain.id
            row['name'] = brain.Title
            row['url'] = brain.getURL()
            row['sponsor'] = brain.orgnization_supervisor
            row['orgnization_passDate'] = brain.orgnization_passDate.strftime('%Y-%m-%d')
            row['legal_person'] = brain.orgnization_legalPerson            
            row['address'] = brain.orgnization_address
            row['register_code'] = brain.orgnization_registerCode
            row['editurl'] = row['url'] + '/confajaxedit'
            row['delurl'] = row['url'] + '/delete_confirmation'            
            mlist.append(row)
        return mlist

class GovernmentDepartmentListing(Orgnizations_adminView):
    "government department admin view"
    grok.template('department_listing')
    grok.name('deparment_listing')    
    
    
    @memoize     
    def getMemberList(self):
        """获取政府部门列表"""
        mlist = []
        from qyxycjh.policy.content.governmentdepartment import IOrgnization as IDepartment        
        memberbrains = self.catalog()({'object_provides':IDepartment.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              )
        i = 0
        for brain in memberbrains:
            i = i+1
            obj = brain.getObject()           
            row = {'number':'','id':'', 'name':'', 'url':'',
                    'operator':'', 'address':'','editurl':'',
                    'delurl':''}
            row['number'] = i
            row['id'] = brain.id
            row['name'] = brain.Title
            row['url'] = brain.getURL()
            row['operator'] = obj.operator           
            row['address'] = obj.address
            row['editurl'] = row['url'] + '/confajaxedit'
            row['delurl'] = row['url'] + '/delete_confirmation'            
            mlist.append(row)
        return mlist            
    
class OrgnizationsView(Orgnizations_adminView):
    """社会组织主视图，包括该组织的年检列表"""
    grok.context(IOrgnization)
    grok.template('orgnization_view')
    grok.name('view')
    grok.require('zope2.View')
    
    def getAnnualSurveyList(self):
        """获取年检结果列表"""       
        
        braindata = self.catalog()({'object_provides':IOrgnization_annual_survey.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                                'review_state':"published",
                             'sort_order': 'reverse',
                             'sort_on': 'created'})
        
        outhtml = ""        
        for i in braindata:            
            out = """<tr>
            <td class="title"><a href="%(objurl)s">%(title)s</a></td>
            <td class="item">%(year)s</td>
            <td class="result">%(annual_survey)s</td></tr>""" % dict(objurl=i.getURL(),
                                            title=i.Title,
                                            annual_survey= self.tranVoc(i.orgnization_annual_survey),
                                            year=i.orgnization_survey_year)           
            outhtml = "%s%s" %(outhtml ,out)
        return outhtml             
    

    
#年检默认视图    
class AnnualsurveyView(SurveyView):
    """年检默认视图"""
    grok.context(IOrgnization_annual_survey)
    grok.template('orgnization_annual_survey')
    grok.name('view')
    grok.require('zope2.View') 
        


class Orgnizations_annualsurveyView(Orgnizations_adminView):
    """年检滚动视图已改为ajax more加载,该视图已废弃，仅仅保留该类作为基类,但首页年检结果滚动数据仍然来自此视图"""
    grok.context(IOrgnizationFolder)
    grok.template('orgnization_annual_survey_roll')
    grok.name('orgnizations_survey')
    grok.require('zope2.View')

    @memoize    
    def allitems(self):
        
#        end = datetime.datetime.today()
#        start = end - datetime.timedelta(365)
        stamp = self.getStart()
        date_range_query = {'query':stamp,'range':'min'}
        braindata = self.catalog()({'object_provides':IOrgnization_annual_survey.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                                'created':date_range_query,
                                'review_state':"published",
                             'sort_order': 'reverse',
                             'sort_on': 'created'})        
        return braindata

    def getStart(self):
        year = datetime.datetime.today().year
        start = datetime.datetime(year,1,1)
        import time
        start = time.mktime(start.timetuple())
        return start    

    def getMemberList(self,start=0,size=0):
        """获取年检结果列表"""    
       
        if size == 0:
            braindata = self.allitems()
        else:
            stamp = self.getStart()            
            date_range_query = {'query':stamp,'range':'min'}            
            braindata = self.catalog()({'object_provides':IOrgnization_annual_survey.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                                'created':date_range_query,
                                'review_state':"published",
                             'sort_order': 'reverse',
#                             'sort_on': 'created',
                             'b_start':start,
                             'b_size':size})

        return self.outputList(braindata)           
            
    def outputList(self,braindata):
        outhtml = ""
      
        for i in braindata:
                        
            out = """<tr>
            <td class="title"><a target="_blank" href="%(objurl)s">%(title)s</a></td>
            <td class="item">%(year)s</td>
            <td class="result">%(annual_survey)s</td></tr>""" % dict(objurl="%s/@@view" % i.getURL(),
                                            title=i.Title,
                                            annual_survey= self.tranVoc(i.orgnization_annual_survey),
                                            year=i.orgnization_survey_year)           
            outhtml = "%s%s" %(outhtml ,out)
        return outhtml        

class AnnualsurveyFullView(Orgnizations_annualsurveyView):
    "all annual survey recorders list"
    grok.context(IOrgnizationFolder)
    grok.template('orgnization_annual_survey_fullview')
    grok.name('orgnizations_survey_fullview')
    grok.require('zope2.View')           

class SurveyMore(grok.View):
    """annual survey list view AJAX action for click more.
    """
    
    grok.context(IOrgnizationFolder)
    grok.name('surveymore')
    grok.layer(IThemeSpecific)
    grok.require('zope2.View')            
    
    def render(self):
       
        form = self.request.form
        formst = form['formstart']
        formstart = int(formst)*10 
        nextstart = formstart + 10               
        favorite_view = getMultiAdapter((self.context, self.request),name=u"orgnizations_survey_fullview")
        favoritenum = len(favorite_view.allitems())
        
        if nextstart >= favoritenum :
            ifmore =  1
            pending = 0
        else :
            ifmore = 0  
            pending = favoritenum - nextstart          

        pending = "%s" % (pending)          
        outhtml = favorite_view.getMemberList(formstart,10)            
        data = {'outhtml': outhtml,'pending':pending,'ifmore':ifmore}
    
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)
 

class SiteRootOrgnizationListingView(Orgnizations_adminView):
    grok.context(ISiteRoot)
    grok.template('orgnization_listings')
    grok.name('orgnization_listings')
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True) 

    def getorgnizations(self,num=10):
 
        """返回前num个organizations
        """
        
        maxlen = len(self.catalog()({'object_provides': IOrgnization.__identifier__}))
        if maxlen > num:
            return self.catalog()({'object_provides': IOrgnization.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on': 'conference_passDate',
                             'sort_limit': num})
        else:
            return self.catalog()({'object_provides': IOrgnization.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on':'conference_passDate'})    

class SiteRootAllOrgnizationListingView(Orgnizations_adminView):
    """
    AJAX 查询，返回分页结果
    """
    grok.context(ISiteRoot)
    grok.template('allorgnization_listings_b3')
    grok.name('allorgnization_listings')
     
    def update(self):
        self.request.set('disable_border', True)                
        
    def test(self,t,a,b):
        """ test method"""   
        if t:
            return a
        else:
            return b
    
    def buildAjaxViewName(self):
        "根据当前上下文，构建ajax view 名称"
        context = aq_inner(self.context)
        if ISiteRoot.providedBy(context):return "oajaxsearch"
        elif IYuhuquOrgnizationFolder.providedBy(context):return "yuhuqusearch"
        elif IYuetangquOrgnizationFolder.providedBy(context):return "yuetangqusearch"
        elif IXiangxiangshiOrgnizationFolder.providedBy(context):return "xiangxiangshisearch"
        elif IXiangtanxianOrgnizationFolder.providedBy(context):return "xiangtanxiansearch"                
        elif IShaoshanshiOrgnizationFolder.providedBy(context):return "shaoshanshisearch"
        else:return "xiangtanshisearch"        
        
    def getorgnizations(self):
 
        """返回 all organizations
        """
        return self.catalog()({'object_provides': IOrgnization.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on':'created'})
#翻译 社团，民非，基金会          
    def getType(self,typekey):
        if typekey == 1:
            return "shetuan"
        elif typekey ==2:
            return "minfei"
        else:
            return "jijinhui"
         
#翻译 成立公告，变更，注销公告  
    def getProvince(self,provincekey):
        if provincekey == 1:
            return "chengli"
        elif provincekey ==2:
            return "biangeng"
        else:
            return "zhuxiao"
         
    def search_multicondition(self,query):  
        return self.catalog()(query)       


class OrgAdminList(SiteRootAllOrgnizationListingView):
    grok.context(IOrgnizationFolder)     
    grok.template('organizations_admin_listings_b3')
    grok.name('view')    


 # ajax multi-condition search       
class ajaxsearch(grok.View):
    """AJAX action for search.
    """    
    grok.context(ISiteRoot)
    grok.name('oajaxsearch')
    grok.layer(IThemeSpecific)
    grok.require('zope2.View')

    def Datecondition(self,key):        
        "构造日期搜索条件"
        end = datetime.datetime.today()
#最近一周        
        if key == 1:  
            start = end - datetime.timedelta(7) 
#最近一月             
        elif key == 2:
            start = end - datetime.timedelta(30) 
#最近一年            
        elif key == 3:
            start = end - datetime.timedelta(365) 
#最近两年                                                  
        elif key == 4:
            start = end - datetime.timedelta(365*2) 
#最近五年               
        else:
            start = end - datetime.timedelta(365*5) 
#            return    { "query": [start,],"range": "min" }                                                             
        datecondition = { "query": [start, end],"range": "minmax" }
        return datecondition  
          
    def render(self):    
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"allorgnization_listings")        
        
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
        provincekey = int(datadic['province'])  # 对应 成立公告，变更公告，注销公告
        typekey = int(datadic['type']) # 对应 社会团体，民非，基金会
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = {'object_provides': IOrgnization.__identifier__}
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
#        origquery['b_size'] = size 
#        origquery['b_start'] = start                 
        
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

        if provincekey != 0:
            conference_province = searchview.getProvince(provincekey)
            origquery['orgnization_announcementType'] = conference_province
        if datekey != 0:
            origquery['orgnization_passDate'] = self.Datecondition(datekey)           
        if typekey != 0:
            origquery['orgnization_orgnizationType'] = searchview.getType(typekey)          

        totalquery = origquery.copy()
        origquery['b_size'] = size 
        origquery['b_start'] = start
        # search all                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)
        # batch search         
        braindata = searchview.search_multicondition(origquery)
#        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains
        data = self.output(start,size,totalnum, braindata)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)       
       
    def output(self,start,size,totalnum,braindata):
        "根据参数total,braindata,返回jason 输出"
        outhtml = ""      
        k = 0
        for i in braindata:          
            out = """<tr class="text-left">
                                <td class="col-md-1">%(num)s</td>
                                <td class="col-md-2 text-left"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="col-md-1">%(code)s</td>
                                <td class="col-md-3 text-left">%(address)s</td>
                                <td class="col-md-2 text-left">%(sponsor)s</td>
                                <td class="col-md-1 text-left">%(legal_person)s</td>
                                <td class="col-md-2">%(pass_date)s</td>                                
                            </tr> """% dict(objurl=i.getURL(),
                                            num=str(k + 1),
                                            title=i.Title,
                                            code= i.orgnization_registerCode,
                                            address=i.orgnization_address,
                                            sponsor=i.orgnization_supervisor,
                                            legal_person = i.orgnization_legalPerson,
                                            pass_date = i.orgnization_passDate.strftime('%Y-%m-%d'))           
            outhtml = "%s%s" %(outhtml ,out)
            k = k + 1 
           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data        


####################################################3333333333
class OrgAdminListAjax(ajaxsearch):
    
    grok.name('org_admin_list')
    
    def render(self):    
        searchview = getMultiAdapter((self.context, self.request),
                                     name=u"allorgnization_listings")               
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        size = int(datadic['size'])      # batch search size
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        origquery = {'object_provides': IOrgnization.__identifier__}
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection 
        totalquery = origquery.copy()
        origquery['b_size'] = size 
        origquery['b_start'] = start                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)         
        braindata = searchview.search_multicondition(origquery)
                 
        del origquery 
        del totalquery,totalbrains
        data = self.output(start,size,totalnum, braindata)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data) 
######################################################                              

from z3c.form import field
class EditAnnualSurvey(dexterity.EditForm):
    grok.name('edit-annual-survey')
    grok.context(IOrgnization_annual_survey)    
    label = _(u'edit annual survey comments and result')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IOrgnization_annual_survey).select('sponsor_comments','annual_survey')                   