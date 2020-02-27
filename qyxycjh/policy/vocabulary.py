from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from five import grok
from zope.schema.interfaces import IVocabularyFactory
from qyxycjh.policy.content.orgnization import IOrgnization

from qyxycjh.policy import _

class OrgnizationVocabulary(object):

    def __call__(self, context):
        catalog = getToolByName(context,"portal_catalog")
        terms = []      
        all = catalog.unrestrictedSearchResults({"object_provides":IOrgnization.__identifier__})
        for bs in all:
            title = bs.Title
            id = bs.id
            terms.append(SimpleVocabulary.createTerm(id,id,title))
        return SimpleVocabulary(terms)        


grok.global_utility(OrgnizationVocabulary, IVocabularyFactory,
        name="qyxycjh.policy.vocabulary.orgnizationo")



annualsurvey_result=[    ('hege','hege',_(u'hege')),
                  ('jibenhege','jibenhege',_(u'jibenhege')),
                  ('buhege','buhege',_(u'buhege')),
                        ]
annualsurvey_result_terms = [SimpleTerm(value, token, title) for value, token, title in annualsurvey_result ]

class AnnualsurveyResult(object):

    def __call__(self, context):
        return SimpleVocabulary(annualsurvey_result_terms)

grok.global_utility(AnnualsurveyResult, IVocabularyFactory,
        name="qyxycjh.policy.vocabulary.annualsurvey")




