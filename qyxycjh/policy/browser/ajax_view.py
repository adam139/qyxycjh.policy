#-*- coding: UTF-8 -*-
from zope.i18n.interfaces import ITranslationDomain
from zope.component import queryUtility
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
import json
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.memoize.instance import memoize
import datetime

from qyxycjh.policy import _
from qyxycjh.policy.content.annualsurvey import IOrgnization_annual_survey


try:
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
except ImportError: # py24
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
from xtshzz.policy import html_template

class SurveyWorkflow(grok.View):
    "接受前台ajax 事件，处理工作流基类"
    grok.name('survey_workflow')   
    grok.require('zope2.View')
    grok.context(IOrgnization_annual_survey)
    
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
    
    def sendMail(self,subject,mailbody,send_to,send_to_bcc=[],sender=None,debug_mode=False):
        notify_encode = 'utf-8'
        object = aq_inner(self.context)
        portal = getToolByName(object,"portal_url").getPortalObject()
        portal_transforms = getToolByName(object, "portal_transforms")
        if sender ==None:
            send_from = portal.getProperty('email_from_address')
        else:
            send_from = sender
        if send_from and type(send_from)==tuple:
            send_from = send_from[0]
        
        translation_service = getToolByName(object,'translation_service')
        
        html_body = mailbody
        here_url = object.absolute_url()
        url_text = u"%s-%s年度-年检报告" % (object.title,object.year) 
        text = html_template.message % ({'from': send_from ,                                 
                                     'message': html_body,
                                     'url': here_url,
                                     'url_text': url_text,
                                     })        
                            
        if notify_encode:
            text = text.encode(notify_encode)
        try:
            data_to_plaintext = portal_transforms.convert("html_to_web_intelligent_plain_text", text)
        except:
            # Probably Plone 2.5.x
            data_to_plaintext = portal_transforms.convert("html_to_text", text)
        plain_text = data_to_plaintext.getData()
    
        msg = MIMEMultipart('alternative')
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(plain_text, 'plain', _charset=notify_encode)
        part2 = MIMEText(text, 'html', _charset=notify_encode)

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)    
        mail_host = getToolByName(object, 'MailHost')
        try:
            if debug_mode:
                print "Message subject: %s" % subject
                print "Message text:\n%s" % text
                print "Message sent to %s (and to %s in bcc)" % (", ".join(send_to) or 'no-one',
                                                             ", ".join(send_to_bcc) or 'no-one')
            else:
                try:
                    mail_host.secureSend(msg, mto=send_to, mfrom=send_from,
                                     subject=subject, charset=notify_encode, mbcc=send_to_bcc)
                except TypeError:
                    # BBB: Plone 2.5 has problem sending MIMEMultipart... fallback to normal plain text email
                    mail_host.secureSend(plain_text, mto=send_to, mfrom=send_from,
                                     subject=subject, charset=notify_encode, mbcc=send_to_bcc)                
        except Exception, inst:
            putils = getToolByName(object,'plone_utils')
            putils.addPortalMessage(_(u'Not able to send notifications'))
            object.plone_log("Error sending notification: %s" % str(inst))
    
    def render(self):
        """
        workflow process ,this function should be subclass override.
        every subclass link to workflow transition.
        """
class SurveySubmitSponsor(SurveyWorkflow):
    "接受前台ajax 事件，处理工作流，提交上级主管审核"
    grok.name('ajax_submit_sponsor')
          

    def render(self):
        """
            接受提交审批事件，确定下一审核人，发送审核通知邮件，反馈结果到前台。
            确定审核人过程：
                1 根据当前提交资料的社团账号，查询对应社团组织，找主管单位。
                    如果有主管单位，则提取主管单位对应的审核账号；
                    如果没有主管单位，则直接提交民政局审核，提取民政局对应的审核账号。
                2 触发工作流动作，给审核账号发送邮件通知，应该包含对当前年检报告的链接。
                3 更新工作流审批历史
                4 发送反馈到前台：
        input:{status:'pengding';comment:'please approve'}
        output:{}
        """
        data = self.request.form
        subject = data['subject']
        context = aq_inner(self.context)
        # call organization survey draft view
        dview = getMultiAdapter((context, self.request),name=u"draftview")
        sponsor = dview.getSponsorOrg()
        if sponsor:
            # 提交主管单位审核
            send_to = dview.getSponsorOperatorEmail()
            wf = dview.wf()
            wf.doActionFor(context, 'submit2sponsor', comment=subject )
            # set default view as sponsor pending audit
            context.setLayout("sponsorview")
            
            # send notify mail
            mailbody = u"<h3>%(org)s%(year)s年度 年检报告，请审核。</h3>"  % ({"org":context.title,
                                                           "year":context.year})
            self.sendMail(subject, mailbody, send_to)
            ajaxtext = u"%(org)s%(year)s年度 年检报告已成功提交主管单位%(sponsor)s审核！" % ({"org":context.title,
                                                           "year":context.year,
                                                           "sponsor":sponsor})
            callback = {"result":True,'message':ajaxtext}
            self.request.response.setHeader('Content-Type', 'application/json')
            return json.dumps(callback)
            
        else:
            pass            
#            next = dview.getAgentOperator()
                  

class SurveySubmitAgent(SurveyWorkflow):
    "接受前台ajax 事件，处理工作流，直接提交民政局审核。"
    grok.name('ajax_submit_agent')
          
    def render(self):
        """
            接受提交审批事件，确定下一审核人，发送审核通知邮件，反馈结果到前台。
            确定审核人过程：
                1 根据当前提交资料的社团账号，查询对应社团组织，找主管单位。
                    如果有主管单位，则提取主管单位对应的审核账号；
                    如果没有主管单位，则直接提交民政局审核，提取民政局对应的审核账号。
                2 给审核账号发送邮件通知，应该包含对当前年检报告的链接。
                3 更新工作流审批历史
                4 发送反馈到前台：
        input:{status:'pengding';comment:'please approve'}
        output:{}
        """
        data = self.request.form
        subject = data['subject']
        context = aq_inner(self.context)
#        self.portal_state = getMultiAdapter((context, self.request), name=u"plone_portal_state")
        # call organization survey draft view
        dview = getMultiAdapter((context, self.request),name=u"sponsorview")
#        import pdb
#        pdb.set_trace()
        sponsor = dview.getAgentOrg()
        if sponsor:
            # 提交民政局审核
            send_to = dview.getAgentOperatorEmail()
            wf = dview.wf()
            wf.doActionFor(context, 'submit2agent', comment=subject )
            # set default view as agent pending audit
            context.setLayout("agentview")
            # send notify mail
            mailbody = u"<h3>%(org)s%(year)s年度 年检报告，请审核。</h3>"  % ({"org":context.title,
                                                           "year":context.year})
            self.sendMail(subject, mailbody, send_to)
            ajaxtext = u"%(org)s%(year)s年度 年检报告已成功提交民政局审核！" % ({"org":context.title,
                                                           "year":context.year})
            callback = {"result":True,'message':ajaxtext}
            self.request.response.setHeader('Content-Type', 'application/json')
            return json.dumps(callback)
            
        else:
            pass
                     
##pending sponsor status,sponsor reject to owner            
class SurveySponsorReject(SurveyWorkflow):
    "接受前台ajax 事件，处理工作流，上级主管单位驳回."
    grok.name('ajax_sponsor_reject')
          
    def render(self):
        """
            接受提交审批事件，确定下一审核人，发送审核通知邮件，反馈结果到前台。
            确定审核人过程：
                1 根据当前提交资料的社团账号，查询对应社团组织，找主管单位。
                    如果有主管单位，则提取主管单位对应的审核账号；
                    如果没有主管单位，则直接提交民政局审核，提取民政局对应的审核账号。
                2 给审核账号发送邮件通知，应该包含对当前年检报告的链接。
                3 更新工作流审批历史
                4 发送反馈到前台：
        input:{status:'pengding';comment:'please approve'}
        output:{}
        """
        data = self.request.form
        subject = data['subject']
        context = aq_inner(self.context)
#        self.portal_state = getMultiAdapter((context, self.request), name=u"plone_portal_state")
        # call organization survey draft view
        dview = getMultiAdapter((context, self.request),name=u"sponsorview")
        send_to = dview.creator()
        if send_to:
            # 提交民政局审核
#            send_to = dview.creator()
            wf = dview.wf()
            wf.doActionFor(context, 'sponsorreject', comment=subject )
            # set default view as agent pending audit
            context.setLayout("draftview")
            # set sponsor_audit_date
            
            context.sponsor_audit_date = datetime.datetime.now().strftime("%Y-%m-%d")
            #update last workflow status
            context.last_status = "pendingsponsor"             
            context.sponsor_comments = subject
            # send notify mail
            mailbody = u"<h3>%(org)s%(year)s年度 年检报告被打回，请根据审核意见，仔细核对。</h3>"  % ({"org":context.title,
                                                           "year":context.year})
            self.sendMail(subject, mailbody, send_to)
            ajaxtext = u"%(org)s%(year)s年度 年检报告已被主管单位打回！" % ({"org":context.title,
                                                           "year":context.year})
            callback = {"result":True,'message':ajaxtext}
            self.request.response.setHeader('Content-Type', 'application/json')
            return json.dumps(callback)
            
        else:
            pass 

##pending agent status,agent veto transition
class SurveySponsorVeto(SurveyWorkflow):
    "接受前台ajax 事件，处理工作流，上级主管单位否决，年检不合格，并转到民政局审批。"
    grok.name('ajax_sponsor_veto')
          
    def render(self):
        """
            接受提交审批事件，确定下一审核人，发送审核通知邮件，反馈结果到前台。
            确定审核人过程：
                1 根据当前提交资料的社团账号，查询对应社团组织，找主管单位。
                    如果有主管单位，则提取主管单位对应的审核账号；
                    如果没有主管单位，则直接提交民政局审核，提取民政局对应的审核账号。
                2 给审核账号发送邮件通知，应该包含对当前年检报告的链接。
                3 更新工作流审批历史
                4 发送反馈到前台：
        input:{status:'pengding';comment:'please approve'}
        output:{}
        """
        data = self.request.form
        subject = data['subject']
        context = aq_inner(self.context)
#        self.portal_state = getMultiAdapter((context, self.request), name=u"plone_portal_state")
        # call organization survey draft view
        dview = getMultiAdapter((context, self.request),name=u"sponsorview")
        sponsor = dview.getAgentOrg()
        if sponsor:
            # 提交民政局审核
            send_to = dview.getAgentOperatorEmail()
            wf = dview.wf()
            wf.doActionFor(context, 'sponsorveto', comment=subject )            
            # set default view as agent pending audit
            context.setLayout("agentview")
            context.agent_audit_date = datetime.datetime.now().strftime("%Y-%m-%d")
            context.sponsor_comments = u"不合格"
#            context.annual_survey = "buhege"
            #update last workflow status
            context.last_status = "pendingsponsor"
            context.reindexObject()            
            # send notify mail
            mailbody = u"<h3>%(org)s%(year)s年度 年检报告已被上级主管单位否决，主管单位的意见为：不合格。</h3>"  % ({"org":context.title,
                                                           "year":context.year})
            self.sendMail(subject, mailbody, send_to)
            ajaxtext = u"%(org)s%(year)s年度 年检报告已被上级主管单位否决，本次年检不合格！" % ({"org":context.title,
                                                           "year":context.year})
            callback = {"result":True,'message':ajaxtext}
            self.request.response.setHeader('Content-Type', 'application/json')
            return json.dumps(callback)
            
        else:
            pass
        

##pending sponsor status,sponsor agree transition
class SurveySponsorAgree(SurveyWorkflow):
    "接受前台ajax 事件，处理工作流"
    grok.name('ajax_sponsor_agree')
          
    def render(self):
        """
            接受提交审批事件，确定下一审核人，发送审核通知邮件，反馈结果到前台。
            确定审核人过程：
                1 根据当前提交资料的社团账号，查询对应社团组织，找主管单位。
                    如果有主管单位，则提取主管单位对应的审核账号；
                    如果没有主管单位，则直接提交民政局审核，提取民政局对应的审核账号。
                2 给审核账号发送邮件通知，应该包含对当前年检报告的链接。
                3 更新工作流审批历史
                4 发送反馈到前台：
        input:{status:'pengding';comment:'please approve'}
        output:{}
        """
        data = self.request.form
        subject = data['subject']
        quality = data['quality']
        context = aq_inner(self.context)
#        self.portal_state = getMultiAdapter((context, self.request), name=u"plone_portal_state")
        # call organization survey draft view
        dview = getMultiAdapter((context, self.request),name=u"sponsorview")
#        import pdb
#        pdb.set_trace()
        sponsor = dview.getAgentOrg()
        if sponsor:
            # 提交民政局审核
            send_to = dview.getAgentOperatorEmail()
            wf = dview.wf()
#            wf.doActionFor(context, 'submit2sponsor', comment=subject )
            wf.doActionFor(context, 'sponsoragree', comment=subject )
            # set default view as agent pending audit
            context.setLayout("agentview")
            context.sponsor_audit_date = datetime.datetime.now().strftime("%Y-%m-%d")
            #update last workflow status
            context.last_status = "pendingsponsor"            
            context.sponsor_comments = dview.tranVoc(quality)            
            # send notify mail
            mailbody = u"<h3>%(org)s%(year)s年度 年检报告通过了主管单位的初审，请民政局领导审核。</h3>"  % ({"org":context.title,
                                                           "year":context.year})
            self.sendMail(subject, mailbody, send_to)
            ajaxtext = u"%(org)s%(year)s年度 年检报告已成功提交民政局！" % ({"org":context.title,
                                                           "year":context.year})
            callback = {"result":True,'message':ajaxtext}
            self.request.response.setHeader('Content-Type', 'application/json')
            return json.dumps(callback)
            
        else:
            pass 

##pending agent status,agent reject transition
class SurveyAgentReject(SurveyWorkflow):
    "接受前台ajax 事件，处理工作流"
    grok.name('ajax_agent_reject')
          
    def render(self):
        """
            接受提交审批事件，确定下一审核人，发送审核通知邮件，反馈结果到前台。
            确定审核人过程：
                1 根据当前提交资料的社团账号，查询对应社团组织，找主管单位。
                    如果有主管单位，则提取主管单位对应的审核账号；
                    如果没有主管单位，则直接提交民政局审核，提取民政局对应的审核账号。
                2 给审核账号发送邮件通知，应该包含对当前年检报告的链接。
                3 更新工作流审批历史
                4 发送反馈到前台：
        input:{status:'pengding';comment:'please approve'}
        output:{}
        """
        data = self.request.form
        subject = data['subject']
        context = aq_inner(self.context)
#        self.portal_state = getMultiAdapter((context, self.request), name=u"plone_portal_state")
        # call organization survey draft view
        dview = getMultiAdapter((context, self.request),name=u"agentview")
        send_to = dview.creator()
        if send_to:
            # 提交民政局审核
#            send_to = dview.creator()
            wf = dview.wf()
#            wf.doActionFor(context, 'submit2sponsor', comment=subject )
#            wf.doActionFor(context, 'sponsoragree', comment=subject )
            wf.doActionFor(context, 'agentreject', comment=subject )
            # set default view as agent pending audit
            context.setLayout("draftview")
            context.agent_audit_date = datetime.datetime.now().strftime("%Y-%m-%d")
            #update last workflow status
            context.last_status = "pendingagent"            
            context.agent_comments = subject            
            # send notify mail
            mailbody = u"<h3>%(org)s%(year)s年度 年检报告被民政局打回，请根据审核意见仔细核对、修改后重新提交。</h3>"  % ({"org":context.title,
                                                           "year":context.year})
            self.sendMail(subject, mailbody, send_to)
            ajaxtext = u"%(org)s%(year)s年度 年检报告已被民政局打回！" % ({"org":context.title,
                                                           "year":context.year})
            callback = {"result":True,'message':ajaxtext}
            self.request.response.setHeader('Content-Type', 'application/json')
            return json.dumps(callback)
            
        else:
            pass 

##pending agent status,agent agree transition
class SurveyAgentAgree(SurveyWorkflow):
    "接受前台ajax 事件，处理工作流，民政局同意，年检合格，并发布为published状态。"
    grok.name('ajax_agent_agree')
          
    def render(self):
        """
            接受提交审批事件，确定下一审核人，发送审核通知邮件，反馈结果到前台。
            确定审核人过程：
                1 根据当前提交资料的社团账号，查询对应社团组织，找主管单位。
                    如果有主管单位，则提取主管单位对应的审核账号；
                    如果没有主管单位，则直接提交民政局审核，提取民政局对应的审核账号。
                2 给审核账号发送邮件通知，应该包含对当前年检报告的链接。
                3 更新工作流审批历史
                4 发送反馈到前台：
        input:{status:'pengding';comment:'please approve'}
        output:{}
        """
        data = self.request.form
        subject = data['subject']
        quality = data['quality']
        context = aq_inner(self.context)
#        self.portal_state = getMultiAdapter((context, self.request), name=u"plone_portal_state")
        # call organization survey draft view
        dview = getMultiAdapter((context, self.request),name=u"agentview")
        send_to = dview.creator()
#        import pdb
#        pdb.set_trace()
        if send_to:
            # 提交民政局审核
#            send_to = dview.creator()
            wf = dview.wf()
#            wf.doActionFor(context, 'submit2sponsor', comment=subject )
#            wf.doActionFor(context, 'sponsoragree', comment=subject )
            wf.doActionFor(context, 'agentagree', comment=subject )            
            # set default view as agent pending audit
            context.setLayout("publishedview")
            context.agent_audit_date = datetime.datetime.now().strftime("%Y-%m-%d")
            context.agent_comments = dview.tranVoc(quality)
            #update last workflow status
            context.last_status = "pendingagent"
            context.annual_survey = quality
            context.reindexObject()            
            # send notify mail
            mailbody = u"<h3>%(org)s%(year)s年度 年检报告，已由民政局审核通过。</h3>"  % ({"org":context.title,
                                                           "year":context.year})
            self.sendMail(subject, mailbody, send_to)
            ajaxtext = u"%(org)s%(year)s年度 年检报告已通过民政局审核！" % ({"org":context.title,
                                                           "year":context.year})
            callback = {"result":True,'message':ajaxtext}
            self.request.response.setHeader('Content-Type', 'application/json')
            return json.dumps(callback)
            
        else:
            pass 

##pending agent status,agent veto transition
class SurveyAgentVeto(SurveyWorkflow):
    "接受前台ajax 事件，处理工作流，民政局否决，年检不合格，并发布为published状态。"
    grok.name('ajax_agent_veto')
          
    def render(self):
        """
            接受提交审批事件，确定下一审核人，发送审核通知邮件，反馈结果到前台。
            确定审核人过程：
                1 根据当前提交资料的社团账号，查询对应社团组织，找主管单位。
                    如果有主管单位，则提取主管单位对应的审核账号；
                    如果没有主管单位，则直接提交民政局审核，提取民政局对应的审核账号。
                2 给审核账号发送邮件通知，应该包含对当前年检报告的链接。
                3 更新工作流审批历史
                4 发送反馈到前台：
        input:{status:'pengding';comment:'please approve'}
        output:{}
        """
        data = self.request.form
        subject = data['subject']
        context = aq_inner(self.context)
#        self.portal_state = getMultiAdapter((context, self.request), name=u"plone_portal_state")
        # call organization survey draft view
        dview = getMultiAdapter((context, self.request),name=u"agentview")
        send_to = dview.creator()
        if send_to:
            # 提交民政局审核
#            send_to = dview.creator()
            wf = dview.wf()
            wf.doActionFor(context, 'agentveto', comment=subject )            
            # set default view as agent pending audit
            context.setLayout("publishedview")
            context.agent_audit_date = datetime.datetime.now().strftime("%Y-%m-%d")
            context.agent_comments = u"不合格"
            context.annual_survey = "buhege"
            #update last workflow status
            context.last_status = "pendingagent"
            context.reindexObject()            
            # send notify mail
            mailbody = u"<h3>%(org)s%(year)s年度 年检报告已被民政局否决，本次年检不合格。</h3>"  % ({"org":context.title,
                                                           "year":context.year})
            self.sendMail(subject, mailbody, send_to)
            ajaxtext = u"%(org)s%(year)s年度 年检报告已被民政局否决，本次年检不合格！" % ({"org":context.title,
                                                           "year":context.year})
            callback = {"result":True,'message':ajaxtext}
            self.request.response.setHeader('Content-Type', 'application/json')
            return json.dumps(callback)
            
        else:
            pass
        
##published status,agent retract transition
class SurveyAgentRetract(SurveyWorkflow):
    "接受前台ajax 事件，处理工作流，民政局将published状态年检报告收回成draft状态。"
    grok.name('ajax_agent_retract')
          
    def render(self):
        """
            接受提交审批事件，确定下一审核人，发送审核通知邮件，反馈结果到前台。
            确定审核人过程：
                1 根据当前提交资料的社团账号，查询对应社团组织，找主管单位。
                    如果有主管单位，则提取主管单位对应的审核账号；
                    如果没有主管单位，则直接提交民政局审核，提取民政局对应的审核账号。
                2 给审核账号发送邮件通知，应该包含对当前年检报告的链接。
                3 更新工作流审批历史
                4 发送反馈到前台：
        input:{status:'pengding';comment:'please approve'}
        output:{}
        """
        data = self.request.form
        subject = data['subject']
        context = aq_inner(self.context)
#        self.portal_state = getMultiAdapter((context, self.request), name=u"plone_portal_state")
        # call organization survey draft view
        dview = getMultiAdapter((context, self.request),name=u"agentview")
        send_to = dview.creator()
        if send_to:
            # 提交民政局审核
            wf = dview.wf()
            wf.doActionFor(context, 'retract', comment=subject )  
            # set default view as agent pending audit
            context.setLayout("draftview")
            context.agent_audit_date = datetime.datetime.now().strftime("%Y-%m-%d")
            context.agent_comments = subject
            # clear last status
            context.last_status = ""                       
            # send notify mail
            mailbody = u"<h3>%(org)s%(year)s年度 年检报告已被民政局收回，可以重新开启新一轮审批流程。</h3>"  % ({"org":context.title,
                                                           "year":context.year})
            self.sendMail(subject, mailbody, send_to)
            ajaxtext = u"%(org)s%(year)s年度 年检报告已被民政局收回！" % ({"org":context.title,
                                                           "year":context.year})
            callback = {"result":True,'message':ajaxtext}
            self.request.response.setHeader('Content-Type', 'application/json')
            return json.dumps(callback)
            
        else:
            pass                
