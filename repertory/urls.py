from django.conf.urls import url

from repertory import api as repertory_api

urlpatterns = [
    url(r'^$', 'repertory.views.appview_from_cache', name='login'),
    url(r'^mine$', 'repertory.views.mine',
      name='ajax-user-calendar'),
    url(r'^@(\w+)', 'repertory.views.theirs',
      name='public-user-calendar'),
    url(r'^api/calendar/(?P<facebook_id>\d+)/(?P<secret>.*)/rep.ics',
      repertory_api.user_ical_feed, name='api-user-ical-feed'),
    url(r'^api/calendar', repertory_api.upcoming_events,
      name='api-calendar'),
    url(r'^api/me$', repertory_api.user_meta,
      name='api-user-info'),
    url(r'^api/me/login', repertory_api.login_or_register,
      name='api-login-or-register'),
    url(r'^api/me/logout', repertory_api.logout,
      name='api-logout'),
    url(r'^api/me/event/add$', repertory_api.add_user_to_event,
      name='api-add-user-to-event'),
    url(r'^api/me/event/remove$', repertory_api.remove_user_from_event,
      name='api-remove-user-from-event'),
    url(r'^api/me/public$', repertory_api.set_user_public,
      name='api-set-user-public'),
    url(r'^api/me/calendar$', repertory_api.user_calendar,
      name='api-user-calendar'),
]
