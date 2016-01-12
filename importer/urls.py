from django.conf.urls import url

from importer import views as importer_views

urlpatterns = [
    url(r'^$', importer_views.index),
    url(r'^bridge', importer_views.bridge),
    url(r'^user', importer_views.user),
    url(r'^api/drafthouse', importer_views.drafthouse_api),
    url(r'^api/export', importer_views.export_api),
]
