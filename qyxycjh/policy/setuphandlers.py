# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone import api
from plone.app.dexterity.behaviors import constrains
from plone.app.textfield.value import RichTextValue
from zope.dottedname.resolve import resolve
from Products.Five.utilities.marker import mark
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone.namedfile.file import NamedImage

from logging import getLogger
logger = getLogger(__name__)

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'qyxycjh.policy:uninstall',
        ]


# for image field data

def _load_image(slider):
    from plone.namedfile.file import NamedImage
    import os
    filename = os.path.join(
        os.path.dirname(__file__),
        'browser',
        'static',
        'slide_{0}.jpg'.format(slider),
    )
    return NamedImage(
        data=open(filename, 'r').read(),
        filename=u'slide_{0}.jpg'.format(slider)
    )
image1 = _load_image(1)
image2 = _load_image(2)
image3 = _load_image(3)


default = { 'i': 'portal_type',
           'o': 'plone.app.querystring.operation.selection.any',
            'v': ['Document','Link']}
query = []
defaultpath = {
                    'i': 'path',
                    'o': 'plone.app.querystring.operation.string.path',
                    'v': '/',
                }
import copy

defaultpath.update({'v':'/guanyuqixie'})
guanyuqixie = [default,defaultpath]

xiehuidongtaipath = copy.copy(defaultpath)
xiehuidongtaipath.update({'v':'/xiehuidongtai'})
xiehuidongtai = [default,xiehuidongtaipath]

hangyezixunpath = copy.copy(defaultpath)
hangyezixunpath.update({'v':'/hangyezixun'})
hangyezixun = [default,hangyezixunpath]

zhengcefaguipath = copy.copy(defaultpath)
zhengcefaguipath.update({'v':'/zhengcefagui'})
zhengcefagui = [default,zhengcefaguipath] 

meitibaodaopath = copy.copy(defaultpath)
meitibaodaopath.update({'v':'/meitibaodao'})
meitibaodao = [default,meitibaodaopath]

huiyuandanweipath = copy.copy(defaultpath)
huiyuandanweipath.update({'v':'/huiyuandanwei'})
huiyuandanwei = [default,huiyuandanweipath]



STRUCTURE = [
    {
        'type': 'Folder',
        'title': u'关于企协',
        'id': 'guanyuqixie',
        'description': u'关于企协',
        'layout': 'tableview'
    },
    {
        'type': 'Folder',
        'title': u'协会动态',
        'id': 'xiehuidongtai',
        'description': u'协会动态',
        'layout': 'tableview',
        'children': [
                     {
            'type': 'my315ok.products.productfolder',
            'title': u'图片新闻',
            'id': 'tupianxinwen',
            'description': u'图片新闻',
            'children': [
                     {                                                                                     
            'type': 'my315ok.products.product',
            'title': u'图片新闻',
            'id': 'prdt1',
            'image':image1,            
            'description': u'图片新闻'
                        } ,
                         {
            'type': 'my315ok.products.product',
            'title': u'图片新闻2',
            'id': 'prdt2',
            'image':image2,            
            'description': u'图片新闻2'
                        } ,
                         {
            'type': 'my315ok.products.product',
            'title': u'图片新闻3',
            'id': 'prdt3',
            'image':image3,            
            'description': u'图片新闻3'
                        }                                                                           
                         ]                      
                      }                                                                         
                     ]
    },             
    {
        'type': 'Folder',
        'title': u'行业资讯',
        'id': 'hangyezixun',
        'description': u'行业资讯',
        'layout': 'tableview'
    },             
    {
        'type': 'Folder',
        'title': u'政策法规',
        'id': 'zhengcefagui',
        'description': u'政策法规',
        'layout': 'tableview'
   
    },              
    {
        'type': 'Folder',
        'title': u'会员单位',
        'id': 'huiyuandanwei',
        'description': u'会员单位',
        'layout': 'tableview'
 
    },              
    {
        'type': 'Folder',
        'title': u'媒体报道',
        'id': 'meitibaodao',
        'description': u'媒体报道',
        'layout': 'tableview'        
    },             
    {
        'type': 'Folder',
        'title': u'查询集',
        'id': 'sqls',
        'description': u'查询集',
        'children': [
                     {
                     'type':'Collection',
                     'title':u'协会动态',
                     'description': u'协会动态查询集',
                     'id':'xiehuidongtai',
                     'sort_on':'created',
                     'sort_reversed':True,
                     'query':xiehuidongtai,
                     },
                     {                     
                     'type':'Collection',
                     'title':u'行业资讯',
                     'description': u'行业资讯查询集',
                     'id':'hangyezixun',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':hangyezixun,
                     },
                     {                     
                     'type':'Collection',
                     'title':u'会员单位',
                     'description': u'会员单位查询集',
                     'id':'huiyuandanwei',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':huiyuandanwei,
                     },
                    {
                     'type':'Collection',
                     'title':u'政策法规',
                     'description': u'最新政策法规',
                     'id':'zhengcefagui',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':zhengcefagui,
                     },                     
                    {
                     'type':'Collection',
                     'title':u'媒体报道',
                     'description': u'媒体报道',
                     'id':'meitibaodao',
                     'sort_on':'created',
                     'sort_reversed':True,                     
                     'query':meitibaodao,
                     }                                                                                                                               
                     ]
    },
    {
        'type': 'qyxycjh.policy.orgnizationfolder',
        'title': u'企业库',
        'id': 'organizations',
        'description': u'企业数据库',
        'layout': 'view',
    },
    {
        'type': 'qyxycjh.policy.memberfolder',
        'title': u'会员库',
        'id': 'memberfolder',
        'description': u'会员数据库',
        'layout': 'adminb3_view',
    },                                                     
    {
        'type': 'Folder',
        'title': u'帮助',
        'id': 'help',
        'description': u'帮助',
        'layout': 'tableview',
    }
               
]


def isNotCurrentProfile(context):
    return context.readDataFile('policy_marker.txt') is None


def post_install(context):
    """Setuphandler for the profile 'default'
    """
#     if isNotCurrentProfile(context):
#         return

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
    
    import_article(portal)
    members = portal.get('sqls', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject()
    members = portal.get('help', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject()
    members = portal.get('organizations', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject()
    members = portal.get('memberfolder', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject()              

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
    
def _create_content(item, container):
    new = container.get(item['id'], None)

    if not new:
        new = api.content.create(
            type=item['type'],
            container=container,
            title=item['title'],
            description=item['description'],            
            id=item['id'],
            safe_id=False)
        logger.info('Created item {}'.format(new.absolute_url()))
    
    if item.get('layout', False):
        new.setLayout(item['layout'])
    if item.get('query', False):
        new.query = item['query']
    if item.get('sort_on', False):
        new.sort_on = item['sort_on']
    if item.get('sort_reversed', False):
        new.sort_reversed = item['sort_reversed']                
    if item.get('image', False):
        new.image = item['image']               
    if item.get('markif', False):
        try:
            ifobj = resolve(item['markif'])
            mark(new,ifobj)
        except:
            pass                
    if item.get('default-page', False):
        new.setDefaultPage(item['default-page'])
    if item.get('allowed_types', False):
        _constrain(new, item['allowed_types'])
    if item.get('local_roles', False):
        for local_role in item['local_roles']:
            api.group.grant_roles(
                groupname=local_role['group'],
                roles=local_role['roles'],
                obj=new)
    if item.get('publish', False):
        api.content.transition(new, to_state=item.get('state', 'published'))
    new.reindexObject()
    # call recursively for children
    for subitem in item.get('children', []):
        _create_content(subitem, new)

    
def _constrain(context, allowed_types):
    behavior = ISelectableConstrainTypes(context)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setLocallyAllowedTypes(allowed_types)
    behavior.setImmediatelyAddableTypes(allowed_types)


article = {"id":'example','title':u'测试文档','content':u'<p>这是一个测试文档</p>'}

def _create_article(article, container):
    id = str(article['id'])

    new = container.get(id, None)
    if not new:
        new = api.content.create(
            type='Document',
            container=container,
            title=article['title'],
            text = RichTextValue(article['content']),            
            id=id,
            safe_id=False)          
        new.reindexObject()         

def import_article(portal):    
    "migrate articles to document" 

    containers = list(item['id'] for item in STRUCTURE if item['id'] not in ["sqls","help"])
    for con in containers:
        container =  portal[con]                                 
        try:
            _create_article(article,container)
        except:
            continue 