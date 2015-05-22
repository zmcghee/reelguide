from django.conf.urls import url

from repertory import api as repertory_api
from repertory.views import *

urlpatterns = [
    url(r'^$', FBLoginView.as_view(), name='login'),
    url(r'^api/me/login', repertory_api.login_or_register,
      name='api-login-or-register'),
    url(r'^api/me/event/add$', repertory_api.add_user_to_event,
      name='api-add-user-to-event'),
    url(r'^api/me/event/remove$', repertory_api.remove_user_from_event,
      name='api-remove-user-from-event'),
    url(r'^api/me/calendar$', repertory_api.user_calendar,
      name='api-remove-user-from-event'),
]
