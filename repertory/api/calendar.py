from datetime import datetime

from django.http import JsonResponse

from repertory.api import _bad_request_method
from repertory.models import EventInstance

def upcoming_events(request):
    if request.method != "GET":
        return _bad_request_method()
    items = []
    filter = {'datetime__gte': datetime.now()}
    qs = EventInstance.objects.filter(**filter)
    for event in qs:
        items.append(event.as_dict)
    return JsonResponse(items, safe=False)