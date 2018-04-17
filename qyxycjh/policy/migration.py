# -*- coding: utf-8 -*-
from plone import api
from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer
import datetime
from plone.app.contenttypes.behaviors.richtext import IRichText

from plone.i18n.normalizer.interfaces import INormalizer
from zope.component import getUtility
from Acquisition import aq_parent
from plone.app.textfield.value import RichTextValue
from qyxycjh.policy.setuphandlers import STRUCTURE,_create_content
from plone.namedfile.file import NamedImage


def create_tree(context):
    "create directory tree."
    
    # create directory structure 
    portal = api.portal.get()
    members = portal.get('events', None)
    if members is not None:
        api.content.delete(members)
    members = portal.get('news', None)
    if members is not None:
        api.content.delete(members)
    members = portal.get('Members', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject() 

    for item in STRUCTURE:
        _create_content(item, portal)    
    members = portal.get('help', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject()
    members = portal.get('sqls', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject()
       
                      