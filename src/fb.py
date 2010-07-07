# -*- coding: utf8 -*-

import urllib

class RestApi(object):
    """
    Facebook RestApi Backend For the FBPY.
    documentation for the official methods can be found at: http://developers.facebook.com/docs/reference/rest/
    """

    def __init__(self, token):
        self.auth_token = token
        
    def get_object(self, call_method, **kargs):
        """
        @params:
            - call_method : method for the rest api.
            (http://developers.facebook.com/docs/reference/rest/)
            - 
        """
        return self._get_request(call_method, **kargs)

    def _get_request(self, call_method, **kargs):
        """
        makes a HTTP (GET) request to the facebook rest api servers for given parameters. 
        """
        query_string = {
            "access_token": self.auth_token,
            "format": "json"
        }
        query_string.update(kargs)
        f = urllib.urlopen("https://api.facebook.com/method/%s?%s" % (call_method, urllib.urlencode(query_string)) )
        return f.read()
 
    def _put_request(self):
        pass
           
class GraphApi(object):
    """
    Facebook GraphApi Backend For the FBPY. 
    documentation for the official methods can be found at: https://graph.facebook.com/
    """
    
    def __init__(self, token):
        self.auth_token = token
    
    """
    gets the given object from facebook api.
    """
    def get_object(self, request_path):
        return self._get_request(request_path)
        
    """
    puts the given object to the facebook api_key.
    """
    def put_object(self, request_path, post_data):
        return self._put_request(request_path, post_data)

    def _get_request(self, request_path):
        """
        makes a HTTP (GET) request to the facebook graph api servers for given parameters. 
        (just for the information getter methods.)
        """
        f = urllib.urlopen("https://graph.facebook.com/%s?access_token=%s" % (request_path, self.auth_token))
        return f.read()
    
    def _put_request(self, request_path, post_data):
        """
        makes a HTTP (POST) request to the facebook graph api servers for given parameters. 
        (just for the information setter methods.)
        """
        post_data.update({
            "access_token": self.auth_token,
        })
        post_data = urllib.urlencode(post_data)
        f = urllib.urlopen("https://graph.facebook.com/%s" % request_path, post_data)
        return f.read()
    
    def put_wall_post(self, user_alias, post_data):
        """
        helper/shortcut function for wall postings
        @params:
            - user alias (profile id or username)
            - post_data (dictionary)
                - example = {
                    "message": "foo bar",
                    "picture": "https://github.com/images/modules/header/logov3.png",
                    "link"   : "http://www.github.com/emre/",
                    "name"   : "github logo",
                    "description": "buraya bakarlar description alani"
                }
        * if you want to post to your running user's wall, just send user_alias parameter as "me".
        """
        return self._put_request("%s/feed" % user_alias, post_data)
        

class FBPY(object):
    """
    base FBPY object
    """

    def __init__(self, token):
        self.auth_token = token
        self.graph_api_instance = None
        self.rest_api_instance  = None
        
    def graph(self):
        """
        returns graph api interface
        """
        if not self.graph_api_instance:
            self.graph_api_instance = GraphApi(self.auth_token)

        return self.graph_api_instance
    
    def rest(self):
        """
        returns rest api interface
        """
        if not self.rest_api_instance:
            self.rest_api_instance = RestApi(self.auth_token)

        return self.rest_api_instance

    @staticmethod
    def get_login_url(params):
        """
        gets the login url to the your facebook application
        @params:
            - api_key
            - cancel_url
            - next
            - req_perms
        """
        query_string = {
            "return_session"  : 1,
            "session_version" : 3,
            "v"               : '1.0'
        }
        query_string.update(params)
        return "https://www.facebook.com/login.php?%s" % urllib.urlencode(query_string)
    

    @staticmethod
    def get_logout_url(params):
        """
        gets the logout url:
        @params:
            - api_key
            - next
            - session_key
        """
        return "https://www.facebook.com/logout.php?%s" % urllib.urlencode(params)
    

