import urllib
import json
from settings import BASEURL, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET

LOGIN_URL = 'https://www.facebook.com/dialog/oauth'
REDIRECT_URL = BASEURL + '/fb/process'
ACCESS_TOKEN_URL = 'https://graph.facebook.com/oauth/access_token'
RESOURCE_URL = 'https://graph.facebook.com/me'    

class FacebookClient():
    
    def __init__(self):
        pass
        
    def get_authentication_url(self):
        params = urllib.urlencode({
            'client_id': FACEBOOK_APP_ID,
            'redirect_uri': REDIRECT_URL,
            #'scope':'',
            #'state':'',
        })
        
        return '%s?%s' % (LOGIN_URL, params)
    
    def get_access_token_from_code(self, code):
        params = urllib.urlencode({
            'client_id': FACEBOOK_APP_ID,
            'client_secret': FACEBOOK_APP_SECRET,
            'code':code,
            'redirect_uri': REDIRECT_URL,
        })
        
        response = urllib.urlopen('%s?%s' % (ACCESS_TOKEN_URL, params)).read()
        
        for pair in response.split('&'):
            if 'access_token' in pair:
                access_token = pair.split('=')[1]
        
        return access_token
        
    def get_user_details(self, token):
        params = urllib.urlencode({
            'access_token': token,
        })
        
        return json.load(urllib.urlopen('%s?%s' % (RESOURCE_URL, params)))
    
    def process(self, code):
        if code:
            token = self.get_access_token_from_code(code)
            
            return self.get_user_details(token)
            
        else:
            return None