# -*- coding: utf8 -*-

import urllib

class GraphApi(object):
    
    def __init__(token):
        self.token = token
    
class RestApi(object):
    
    def __init__(token):
        self.token = token

    def call(method, params):
        pass


class FBPY(object):

    def __init__(config):
        self.app_key    = config.get("app_key") 
        self.rest_api   = RestApi(self.auth_token)
        self.graph_api  = GraphApi(self.auth_token)

    """
    gets the login url to the your facebook application
    @params:
        - api_key
        - cancel_url
        - next
        - req_perms
    """
    @staticmethod
    def getLoginUrl(params):
        query_string = {
            "return_session"  : 1,
            "session_version" : 3,
            "v"               : '1.0'
        }
        query_string.update(params)
        return "https://www.facebook.com/login.php?%s" % urllib.urlencode(query_string)
    
    """
    gets the logout url:
    @params:
        - api_key
        - next
        - session_key
    """
    @staticmethod
    def getLogoutUrl(params):
        return "https://www.facebook.com/logout.php?%s" % urllib.urlencode(params)
    


print FBPY.getLogoutUrl({
    "api_key"         : "6f26525beb155be03e88bb4cd85165b3",
    "next"            : "http://ilanlar.adnity.com",
    "session_key"     : "ehe",  
})

