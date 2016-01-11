from datetime import datetime

from django.http import JsonResponse, Http404

from repertory.api import _bad_request_method
from repertory.models import EventInstance

def upcoming_events(request):
    if request.method != "GET":
        return _bad_request_method()
    items = []
    filter = {'datetime__gte': datetime.now()}
    qs = EventInstance.objects.filter(**filter)
    sort = request.GET.get('sort', '')
    if sort == 'title':
        qs = qs.order_by('event__sort_title', 'datetime')
    else:
        qs = qs.order_by('datetime')
    for event in qs:
        items.append(event.as_dict())
    return JsonResponse(items, safe=False)

def _get_all_formats():
    return list(EventInstance.objects.order_by('format').values_list(
      'format', flat=True).distinct())

def update_format(request):
    if request.method != "POST":
        return _bad_request_method()
    instance_id = request.POST.get('event_id', None)
    format = request.POST.get('format', None)
    if not instance_id or not format:
        raise Http404
    if format not in _get_all_formats():
        raise Http404
    try:
        obj = EventInstance.objects.get(pk=instance_id)
    except EventInstance.DoesNotExist:
        raise Http404
    else:
        obj.format = format
        obj.save()
    return JsonResponse({'success': True, 'format': obj.format})
