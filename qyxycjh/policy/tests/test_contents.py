import unittest

from qyxycjh.policy.testing import POLICY_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
from plone.namedfile.file import NamedImage

class Allcontents(unittest.TestCase):
    layer = POLICY_INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']

        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('qyxycjh.policy.annualsurveyfolder', 'annualsurveyfolder1')
                                                     

        
        portal['annualsurveyfolder1'].invokeFactory('qyxycjh.policy.orgnizationsurvey',
                                                    'orgnizationsurvey1',
                                                   title="orgnizationsurvey1")
        portal['annualsurveyfolder1'].invokeFactory('qyxycjh.policy.orgnizationsurvey',
                                                    'orgnizationsurvey2',
                                                   title="orgnizationsurvey2")       
       
        self.portal = portal
                
    def test_folder_types(self):
        self.assertEqual(self.portal['annualsurveyfolder1'].id,'annualsurveyfolder1')
    
    def test_item_types(self):
        self.assertEqual(self.portal['annualsurveyfolder1']['orgnizationsurvey1'].id,'orgnizationsurvey1')
        self.assertEqual(self.portal['annualsurveyfolder1']['orgnizationsurvey2'].id,'orgnizationsurvey2')
   
        