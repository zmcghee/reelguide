from django.http import JsonResponse

def _bad_request_method():
    res = {'error': "Invalid request method."}
    return JsonResponse(res, status=400)

def _not_authenticated():
    res = {'error': "You're not logged in."}
    return JsonResponse(res, status=401)

# Avoid circular imports
from repertory.api.login_or_register import *
from repertory.api.user_events import *