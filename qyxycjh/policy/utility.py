from qyxycjh.policy import _
from zope.interface import Invalid

def imageSizeConstraint(value):
    # value implements the plone.namedfile.interfaces.INamedBlobImageField interface
    width, height = value.getImageSize()
    if width > 300 or height > 300:
        raise Invalid(_(u"Your image is too large"))
    
def fileSizeConstraint(value):
    # value implements the plone.namedfile.interfaces.INamedBlobImageField interface
    size = value.getSize()
    if size > 1024 * 300:
        raise Invalid(_(u"Your image is too large"))    