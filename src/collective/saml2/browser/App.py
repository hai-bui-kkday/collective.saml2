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
    data = ''

    def __call__(self):
        """"""
        url_login_default = getToolByName(self.context, "portal_url")() + "/acl_users/saml2sp/login?came_from=" + getToolByName(self.context, "portal_url")() + "/@@app_login"
        url_login = api.portal.get_registry_record('kkday.app_login.url', default=url_login_default)
        if not api.user.is_anonymous():
            alsoProvides(self.request, IDisableCSRFProtection)

            current = api.user.get_current()
            id = current.id
            if not id:
                raise ValueError("id is required")

            acl_users = getToolByName(self.context, "acl_users")

            token = acl_users.jwt_auth.create_token(id)
            self.data = json.dumps({
                "token": token,
                "id": id
            })

            return self._template()

        self.request.response.redirect(url_login)
        return "redirecting"