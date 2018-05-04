from cgi import escape
from datetime import date
from urllib import unquote

from plone.registry.interfaces import IRegistry

from plone.memoize.view import memoize
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.component import getUtility
from zope.deprecation.deprecation import deprecate
from zope.i18n import translate
from zope.interface import implements, alsoProvides
from zope.viewlet.interfaces import IViewlet

from AccessControl import getSecurityManager
from Acquisition import aq_base, aq_inner

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import ISiteSchema
from Products.CMFPlone.interfaces import ISearchSchema
from Products.CMFPlone.utils import safe_unicode, getSiteLogo
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets.common import LogoViewlet as base
from plone.app.layout.viewlets.common import ViewletBase
from plone.protect.utils import addTokenToUrl

class SearchBoxViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/searchbox.pt')

    def update(self):
        super(SearchBoxViewlet, self).update()

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')

        registry = getUtility(IRegistry)
        search_settings = registry.forInterface(ISearchSchema, prefix='plone')
        self.livesearch = search_settings.enable_livesearch

        folder = context_state.folder()
        self.folder_path = '/'.join(folder.getPhysicalPath())

    @memoize
    def data_pat_livesearch(self):
        navroot = self.navigation_root_url
        out = "ajaxUrl:%s/@@ajax-search;minimumInputLength:2" % navroot
        return out

class PathBarViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/path_bar.pt')

    def update(self):
        super(PathBarViewlet, self).update()

        self.is_rtl = self.portal_state.is_rtl()

        breadcrumbs_view = getMultiAdapter((self.context, self.request),
                                           name='breadcrumbs_view')
        self.breadcrumbs = breadcrumbs_view.breadcrumbs()
