from django.conf.urls import url

from repertory import api as repertory_api
from repertory.views import *

urlpatterns = [
    url(r'^$', FBLoginView.as_view(), name='login'),
    url(r'^api/user/loginOrRegister', repertory_api.login_or_register,
      name='api-login-or-register'),
]
