from base64 import b64decode

from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from repertory.api import _not_authenticated, _bad_request_method
from repertory.models import ReelUser, EventInstance
from repertory.utils.ical import ics_for_user

def set_user_public(request):
    if request.method != "POST":
        return _bad_request_method()
    if not request.user.is_authenticated():
        return _not_authenticated()
    request.user.reeluser.public = request.POST.get('public', '')
    try:
        request.user.reeluser.save()
    except:
        res = {'error': 'Sorry, that name is not available.'}
    else:
        if request.user.reeluser.public:
            res = {'success': "Your public profile has been published."}
        else:
            res = {'success': "Your profile is no longer public."}
    res['public'] = request.user.reeluser.public
    return JsonResponse(res, status=200)

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
        if request.user.reeluser.ical:
            ics = ics_for_user(request.user.reeluser, action='event',
              event_instance=event_instance)
        res = {'success': "You were added to the event!",
               'eventInstanceId': int(eventInstanceId)}
    elif remove:
        request.user.reeluser.event_instances.remove(event_instance)
        if request.user.reeluser.ical:
            ics = ics_for_user(request.user.reeluser, action='cancel',
              event_instance=event_instance)
        res = {'success': "You were removed from the event.",
               'eventInstanceId': int(eventInstanceId)}
    return JsonResponse(res, status=200)

def add_user_to_event(request):
    return _user_to_event(request, add=True)

def remove_user_from_event(request):
    return _user_to_event(request, remove=True)

def user_calendar(request):
    if request.method != "GET":
        return _bad_request_method()
    if not request.user.is_authenticated():
        return _not_authenticated()
    return JsonResponse(request.user.reeluser.calendar(), safe=False)

def user_ical_feed(request, facebook_id, secret):
    if request.method != "GET":
        return _bad_request_method()
    reeluser = get_object_or_404(ReelUser,
      facebook_id=facebook_id, ical=secret)
    refresh_cache = request.GET.get('refresh', False)
    res = ics_for_user(reeluser, refresh=refresh_cache)
    return HttpResponse(res, content_type='text/calendar')

def user_meta(request):
    if request.method != "POST":
        return _bad_request_method()
    if not request.user.is_authenticated():
        return _not_authenticated()
    # Get iCal link
    reeluser = request.user.reeluser
    if not reeluser.ical:
        reeluser.set_ical_key()
        reeluser.save()
    ical_params = {'secret': reeluser.ical,
      'facebook_id': reeluser.facebook_id}
    ical_url = reverse('api-user-ical-feed', kwargs=ical_params)
    res = { 'ical': "http://%s%s" % (request.get_host(), ical_url),
            'public': reeluser.public }
    return JsonResponse(res)