from django.conf.urls import include, url
from django.contrib import admin

from importer import urls as importer_urls
from repertory import urls as repertory_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'importer/', include(importer_urls)),
    url(r'', include(repertory_urls)),
]
