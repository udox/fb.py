# -*- coding: utf8 -*-
from fb import FBPY

import simplejson

class FBPYMiddleware(object):
    
    def process_request(self, request):
        request.facebook = FBPY()

        if request.GET.has_key("session"):
            try:
                fb_user = simplejson.loads(request.GET["session"])
                request.session["fb_user"] = fb_user
                request.facebook.set_token(fb_user["access_token"])
            except:
                pass

    def process_response(self, request, response):
        # internet explorer hack 
        response['P3P'] = 'CP="NOI DSP COR NID ADMa OPTa OUR NOR"'
        return response
