from base64 import b64encode

from datetime import datetime

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView

from repertory.models import EventInstance, ReelUser
from repertory.api.calendar import _get_all_formats

def upcoming_events():
    items = []
    filter = {'datetime__gte': datetime.now()}
    qs = EventInstance.objects.filter(**filter)
    for event in qs:
        items.append(event.as_dict(python_datetime=True))
    return items

def mine(request):
    if request.user.is_authenticated():
        my_events = request.user.reeluser.calendar(python_datetime=True)
        ical = request.user.reeluser.ical
        context = {'ical': ical, 'events': my_events, 'logged_in': True}
    else:
        context = {'ical': False, 'events': False, 'logged_in': False}
    return render(request, "events_mine.html", context)

def theirs(request, public):
    reeluser = get_object_or_404(ReelUser, public=public.lower())
    context = {
        'public': public,
        'events': reeluser.calendar(python_datetime=True)
    }
    return render(request, "events_theirs.html", context)

class AppView(TemplateView):
    template_name = "app.html"

    def get_context_data(self, **kwargs):
        context = super(AppView, self).get_context_data(**kwargs)
        context['events'] = upcoming_events()
        context['formats'] = _get_all_formats()
        return context

def appview_from_cache(request):
    refresh_cache = request.GET.get('refresh', False)
    if not refresh_cache:
        cache_result = cache.get("MainAppView")
        if cache_result:
            output = "%s%s" % ("<!--cache-->", cache_result) 
            return HttpResponse(output)
    response = AppView.as_view()(request)
    cache.set("MainAppView", response.rendered_content, None)
    return response