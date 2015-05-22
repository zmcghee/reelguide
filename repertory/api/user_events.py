from django.http import JsonResponse

from repertory.api import _not_authenticated, _bad_request_method
from repertory.models import ReelUser, EventInstance

def _user_to_event(request, add=False, remove=False):
    if request.method != "POST":
        return _bad_request_method()
    if not request.user.is_authenticated():
        return _not_authenticated()
    # Got your event instance ID?
    eventInstanceId = request.POST.get('eventInstanceId', False)
    if not eventInstanceId:
        res = {'error': "eventInstanceId is required."}
        return JsonResponse(res, status=400)
    try:
        event_instance = EventInstance.objects.get(pk=eventInstanceId)
    except EventInstance.DoesNotExist:
        res = {'error': "Could not find object with eventInstanceId."}
        return JsonResponse(res, status=404)
    if add:
        request.user.reeluser.event_instances.add(event_instance)
        res = {'success': "You were added to the event!",
               'eventInstanceId': int(eventInstanceId)}
    elif remove:
        request.user.reeluser.event_instances.remove(event_instance)
        res = {'success': "You were removed from the event.",
               'eventInstanceId': int(eventInstanceId)}
    return JsonResponse(res, status=200)

def add_user_to_event(request):
    return _user_to_event(request, add=True)

def remove_user_from_event(request):
    return _user_to_event(request, remove=True)

