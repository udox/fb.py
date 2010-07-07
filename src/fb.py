# -*- coding: utf8 -*-

import urllib, simplejson

"""
fb.py is a python client library for facebook api. it supports both *old rest api*
and *new graph api*.

you can find official documentation at facebook:
    * old rest api: http://developers.facebook.com/docs/reference/rest/
    * graph api: http://graph.facebook.com

for the installation tips and usage examples, take a look to the readme.
"""

class GraphApiException(Exception):
    """
    custom exception class for graph api response errors.
    """
    def __init__(self, type, message):
        Exception.__init__(self, message)
        self.type = type
        
class RestApiException(Exception):
    """
    custom exception class for rest api response errors.
    """
    def __init__(self, error_code, message):
        Exception.__init__(self, message)
        self.error_code = error_code

class RestApi(object):
    """
    Facebook RestApi Backend For the FBPY.
    documentation for the official methods can be found at: http://developers.facebook.com/docs/reference/rest/
    """

    def __init__(self, token):
        self.auth_token = token
        
    """
    handles api-response errors
    """
    def _handle_errors(self, api_response):
        if isinstance(api_response, dict) and api_response["error_code"]:
            raise RestApiException(api_response["error_code"], api_response["error_msg"])
        
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
        f = urllib.urlopen("https://api.facebook.com/method/%s?%s" % (call_method, urllib.urlencode(query_string)))
        api_response = simplejson.loads(f.read())
        self._handle_errors(api_response)
        
        return api_response

           
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
        
    """
    handles api-response errors
    """
    def _handle_errors(self, api_response):
        if isinstance(api_response, dict) and api_response.has_key("error"):
            raise GraphApiException(api_response["error"]["type"], api_response["error"]["message"])
    
    def _get_request(self, request_path, extra_params = None):
        """
        makes a HTTP (GET) request to the facebook graph api servers for given parameters. 
        (just for the information getter methods.)
        """
        parameters = {
            "access_token" : self.auth_token,
        }
        
        if extra_params:
            parameters.update(extra_params)
        
        f = urllib.urlopen("https://graph.facebook.com/%s?%s" % (request_path, urllib.urlencode(parameters)))

        api_response = simplejson.loads(f.read())
        self._handle_errors(api_response)
        
        return api_response
        

    def get_picture(self, user_alias, picture_size = None):
        """
        shortcut method to retrieve user avatars easily by selected size.
        possible types: small, square, large.
        example:
            - fbpy_instance.graph().get_picture(USER_ID, "small")
        """
        extra_params = {}
        if user_alias == 'me':
            result = self.get_object("me")
            user_alias = result["id"]
        if picture_size and picture_size in ["small", "square", "large"]:
            extra_params.update({
                "type": picture_size,
            })

        return "https://graph.facebook.com/%s/picture?%s" % (user_alias, urllib.urlencode(extra_params))
    
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
        api_response = simplejson.loads(f.read())
        self._handle_errors(api_response)
        
        return api_response
    
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

    def __init__(self, token = None):
        self.auth_token = token
        self.graph_api_instance = None
        self.rest_api_instance  = None
    
    def set_token(self, token):
        self.auth_token = token
    
    def is_authenticated(self):
        return bool(self.auth_token)
        
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

    

