#-*- coding: UTF-8 -*-
from five import grok
from plone.directives import dexterity, form

from zope import schema



# Interface class; used to define content-type schema.

class IMemberfolder(form.Schema):
    """
    memberfolder for dexterity member
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/feedsfolder.xml to define the content type
    # and add directives here as necessary.



# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

