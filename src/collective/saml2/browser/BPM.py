from Products.Five import BrowserView
from plone import api
import urllib2
from Products.CMFCore.utils import getToolByName

import re

class BPM(BrowserView):

    def __call__(self):
        """"""

        if not api.user.is_anonymous():

            current = api.user.get_current()
            email = current.id

            plone_utils = getToolByName(self.context, 'plone_utils')
            bpm_url = api.portal.get_registry_record('kkday.bpm.url', default='')
            if not bpm_url:
                plone_utils.addPortalMessage(u'BPM url is undefined', 'error')
                self.request.response.redirect(self.context.absolute_url())
                return "redirecting"
 
            try:
                myurl = bpm_url.format(email)
                page = urllib2.urlopen(myurl, timeout = 3)
            except:
                plone_utils.addPortalMessage(u'cannot connect BPM', 'error')
                self.request.response.redirect(self.context.absolute_url())
                return "redirecting"

            url =  page.info().getheader('kkday_bpm_sso_url')

            if url:
                self.request.response.redirect(url)
                return "redirecting"
            else:
                plone_utils.addPortalMessage(u'cannot get BPM url', 'error')
                self.request.response.redirect(self.context.absolute_url())
                return "redirecting"


        self.request.response.redirect(self.context.absolute_url())
        return "redirecting"

