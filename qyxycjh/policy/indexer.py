from plone.indexer.decorator import indexer
from Products.ZCatalog.interfaces import IZCatalog
from qyxycjh.policy.content.orgnization import IOrgnization
from qyxycjh.policy.content.annualsurvey import IOrgnization_annual_survey

@indexer(IOrgnization)
def indexer_orgnization_address(obj, **kw):
    return obj.address

@indexer(IOrgnization)
def indexer_orgnization_legalperson(obj, **kw):
    return obj.legal_person

@indexer(IOrgnization)
def indexer_orgnization_supervisor(obj, **kw):
    return obj.supervisor

@indexer(IOrgnization)
def indexer_orgnization_registercode(obj, **kw):
    return obj.register_code

@indexer(IOrgnization)
def indexer_orgnization_passdate(obj, **kw):
    return obj.passDate

@indexer(IOrgnization_annual_survey)
def indexer_orgnization_annual_survey(obj, **kw):
    return obj.annual_survey

@indexer(IOrgnization_annual_survey)
def indexer_orgnization_survey_year(obj, **kw):
    return obj.year



