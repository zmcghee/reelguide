from datetime import datetime

from django.shortcuts import render
from django.views.generic.base import TemplateView

from repertory.models import EventInstance

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
        context = {'events': my_events, 'logged_in': True}
    else:
        context = {'events': False, 'logged_in': False}
    return render(request, "mine.html", context)

class AppView(TemplateView):
    template_name = "app.html"

    def get_context_data(self, **kwargs):
        context = super(AppView, self).get_context_data(**kwargs)
        context['events'] = upcoming_events()
        return context