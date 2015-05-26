from django.core.cache import cache
from django.template import Context
from django.template.loader import get_template

def ics_for_user(reeluser, refresh=False, action=None, event_instance=None):
    cache_key = "ical_user_%s" % reeluser.pk
    user_ical = cache.get(cache_key)
    if refresh or not user_ical:
        user_ical = {
            "cache": "",
            "pieces": [],
            "sequences": {}
        }
    templates = {
        "start": get_template("ical/start.ics"),
        "end": get_template("ical/end.ics"),
        "event": get_template("ical/event.ics"),
        "update": get_template("ical/update.ics"),
        "cancel": get_template("ical/cancel.ics")
    }
    if not user_ical['pieces']:
        for event_obj in reeluser.calendar(python_datetime=True):
            id = int(event_obj['event_id'])
            user_ical['sequences'][id] = 0
            sequence = user_ical['sequences'][id]
            context = { "sequence": sequence, "event": event_obj }
            piece = templates['event'].render(context)
            user_ical['pieces'].append(piece)
    if action and event_instance:
        id = int(event_instance.pk)
        sequence = user_ical['sequences'].get(id, -1)
        user_ical['sequences'][id] = sequence + 1
        sequence = user_ical['sequences'][id]
        context = { "sequence": sequence,
          "event": event_instance.as_dict(python_datetime=True)}
        piece = templates[action].render(context)
        user_ical['pieces'].append(piece)
    start = templates['start'].render({})
    end = templates['end'].render({})
    meat = "\n".join(user_ical['pieces'])
    user_ical['cache'] = "%s\n%s\n%s" % (start, meat, end)
    cache.set(cache_key, user_ical, None)
    return user_ical['cache']