from django.conf.urls import include, url
from django.contrib import admin

from repertory import urls as repertory_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(repertory_urls)),
]
