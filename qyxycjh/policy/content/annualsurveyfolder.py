from five import grok
from zope import schema

from plone.directives import form, dexterity

from qyxycjh.policy import _

class IAnnualSurveyFolder(form.Schema):
    """
    a folder contain some annual survey information for social organizations
    """
