#-*- coding: UTF-8 -*-
from five import grok
from zope import schema
from zope.interface import Interface
import datetime
from plone.directives import form, dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from collective import dexteritytextindexer
from qyxycjh.policy.utility import fileSizeConstraint
from qyxycjh.policy import _

    
class IOrgnization_annual_survey(form.Schema,IBasic):

#所属社会组织
    title = schema.Choice(
            title=_(u"organization name"),
            vocabulary='qyxycjh.policy.vocabulary.orgnizations',
            required=True
                        )

# 上级主管单位
    sponsor = schema.Text(title=_(u"sponsor"), required=False)
# 上级主管单位意见    
    sponsor_comments = schema.Text(title=_(u"sponsor comments"), required=False)
# # 民政局意见      
#     agent_comments = schema.Text(title=_(u"civil agent comments"), required=False)    
   
# 上级主管单位审核日期 
    sponsor_audit_date = schema.Text(title=_(u"sponsor audit date"), required=False)
# # 民政局审核日期      
#     agent_audit_date = schema.Text(title=_(u"civil agent audit date"), required=False) 
    
#年度           
    year = schema.TextLine(title=_(u"the year for survey"),
                             default=u"2019",
                             required=False,)

#年检报告书    
    report = NamedBlobFile(title=_(u"report"),
        description=_(u"Attach your anual report (word, etc)."),
        constraint=fileSizeConstraint,
        required=True
    )
# 上次工作流状态
    last_status = schema.TextLine(title=_(u"last status of the annual survey"),                             
                             required=False,)
    
#年检结果            
    annual_survey = schema.Choice(
        title=_(u"the result of annual survey"),
        vocabulary="qyxycjh.policy.vocabulary.annualsurvey"
    )       
# 审核历史
  
    
    form.omitted('description','sponsor','sponsor_comments','sponsor_audit_date','last_status','annual_survey')    


@form.default_value(field=IOrgnization_annual_survey['year'])
def surveyYearDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return (datetime.datetime.today() + datetime.timedelta(-365)).strftime("%Y") 
         