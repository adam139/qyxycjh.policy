#-*- coding: UTF-8 -*-
from five import grok
from zope import schema
from zope.interface import Interface
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage
from plone.directives import form, dexterity
from collective import dexteritytextindexer

from qyxycjh.policy import _

class IOrgnization(form.Schema,IImageScaleTraversable):
    """
    内容类型接口，注册为：qyxycjh.policy.governmentorgnization
    政府部门单位：市教育局等
    """
#名称
    dexteritytextindexer.searchable('title')    
    title = schema.TextLine(title=_(u"orgnization name"),
                             default=u"",
                            required=True,) 
#描述       
    description = schema.TextLine(title=_(u"organization summary"),
                             default=u"",
                             required=False,)
#   住所 
    address = schema.TextLine(title=_(u"Address"),
                             default=u"",
                             required=False,)
#   经办人 
    operator = schema.TextLine(title=_(u"operator"),
                             default=u"",
                             required=False,)
    
#   公章     
    image = NamedBlobImage(title=_(u"public sign"),
                             description=_(u"a image of the public sign"),
                             required=False,)        