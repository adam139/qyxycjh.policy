
from dexterity.membrane.content.member import IMember
from zope import schema
from qyxycjh.policy import _


class IOrganizationMember(IMember):
    """
    Organization Member
    """    

    orgname = schema.Choice(
            title=_(u"company name"),
            vocabulary='qyxycjh.policy.vocabulary.orgnizations',
            required=True
                        )
  
### organization sponsor member
class ISponsorMember(IMember):
    """
    Government department Member
    """
    

    orgname = schema.Choice(
            title=_(u"organization name"),
            vocabulary='qyxycjh.policy.vocabulary.sponsors',
            required=True
                        )     