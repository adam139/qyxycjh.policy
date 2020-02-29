#-*- coding: UTF-8 -*-
from five import grok
from z3c.form import field
from plone.directives import dexterity

from qyxycjh.policy.content.orgnization import IOrgnization
from qyxycjh.policy.content.annualsurvey import IOrgnization_annual_survey
from qyxycjh.policy import _

class EditOrgnizationSurvey(dexterity.EditForm):
    grok.name('ajaxedit')
    grok.context(IOrgnization_annual_survey)    
    label = _(u'Edit Organization Survey')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IOrgnization_annual_survey).select('annual_survey', 'year')  


class EditOrgnization(dexterity.EditForm):
    grok.name('ajaxedit')
    grok.context(IOrgnization)    
    label = _(u'Edit Organization')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IOrgnization).select('title', 'description','address','legal_person',
                                                'supervisor','register_code','passDate')
        
          