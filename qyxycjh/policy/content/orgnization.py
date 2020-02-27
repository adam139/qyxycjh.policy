#-*- coding: UTF-8 -*-
from five import grok
from zope import schema
from zope.interface import Interface
import datetime

from plone.directives import form, dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from collective import dexteritytextindexer

from qyxycjh.policy import _


class IOrgnization(form.Schema,IBasic):
    """
    orgnization content type
    """
#名称
    dexteritytextindexer.searchable('title')    
    title = schema.TextLine(title=_(u"orgnization name"),
                             default=u"",
                            required=True,) 
#经营范围        
    description = schema.TextLine(title=_(u"sector"),
                             default=u"",
                             required=False,)
#   住所 
    address = schema.TextLine(title=_(u"Address"),
                             default=u"",
                             required=False,)
#   法人     
    legal_person = schema.TextLine(title=_(u"legal person"),
                             default=u"",
                             required=True,)
#登记证号    
    register_code = schema.ASCIILine(
            title=_("label_register_code",
                default=u"register code"),
            description=_("help_register_code",
                default=u"A code identifying this organization."),
            required=False)    
# 主管单位    
    supervisor = schema.TextLine(title=_(u"supervisor organization"),
                             default=u"",
                             required=True,)    
# 日期
    passDate = schema.Date(
        title=_(u"Pass Date"),
        description=u'',
        required=False,
    )

@form.default_value(field=IOrgnization['passDate'])
def passDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(-1) 
    
         