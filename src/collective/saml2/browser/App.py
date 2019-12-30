from Products.Five import BrowserView
from plone import api
from Products.CMFCore.utils import getToolByName
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import json
import re
import urllib2

class Login(BrowserView):

    _template = ViewPageTemplateFile('app_login.pt')
    token = ''

    def __call__(self):
        """"""
        url_login_default = getToolByName(self.context, "portal_url")() + "/acl_users/saml2sp/login?came_from=" + getToolByName(self.context, "portal_url")() + "/@@app_login"
        url_login = api.portal.get_registry_record('kkday.app_login.url', default=url_login_default)
        if not api.user.is_anonymous():
            alsoProvides(self.request, IDisableCSRFProtection)

            current = api.user.get_current()
            email = current.id
            if not email:
                raise ValueError("email is required")

            acl_users = getToolByName(self.context, "acl_users")
            acl_users.jwt_auth.store_tokens = True
            timeout = api.portal.get_registry_record('kkday.app_login.timeout', default=3600)

            token = acl_users.jwt_auth.create_token(email, timeout=timeout)
            self.token = token

            return self._template()

        self.request.response.redirect(url_login)
        return "redirecting"