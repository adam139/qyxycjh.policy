#-*- coding: UTF-8 -*-
from zope import interface
from zope.component import adapts
from zope.component.interfaces import ObjectEvent
from qyxycjh.policy.interfaces import ICreateOrgEvent

class CreateOrgEvent(object):
    interface.implements(ICreateOrgEvent)
    
    def __init__(self,id,title,description,legal_person,\
                 register_code,passDate,supervisor,address):
        """角色,级别,备注"""
        self.id = id
        self.title = title
        self.description = description
        self.address = address 
        self.legal_person = legal_person
        self.supervisor = supervisor
        self.register_code = register_code
        self.passDate = passDate         

       