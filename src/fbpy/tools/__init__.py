# -*- coding: utf8 -*-

import simplejson

from fbpy import FBPY

from django.conf import settings

class FBPYMiddleware(object):
    
    def process_request(self, request):
        request.facebook = FBPY()
        """
        if this request is login
        """
        if request.GET.has_key("session"):
            try:
                fb_user = simplejson.loads(request.GET["session"])
                request.session["fb_user"] = fb_user
                request.facebook.set_token(fb_user["access_token"])
                request.facebook.set_config(settings.FACEBOOK_CONFIG)
            except:
                pass

    def process_response(self, request, response):
        response['P3P'] = 'CP="NOI DSP COR NID ADMa OPTa OUR NOR"'
        return response
