import hashlib
import requests

from django.conf import settings

from urlparse import parse_qs

def authorize_fb_token(fb_access_token, fb_user_id):
    """return fb_user or None"""
    payload = {
        'grant_type': 'fb_exchange_token',
        'client_id': settings.FB_APP_ID,
        'client_secret': settings.FB_APP_SECRET,
        'fb_exchange_token': fb_access_token
    }
    fb_url = "https://graph.facebook.com/oauth/access_token"
    res = requests.get(fb_url, params=payload)
    if res.status_code != 200:
        return False
    params = parse_qs(res.text)
    return params['access_token'][0]