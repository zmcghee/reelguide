from django.contrib import admin
from repertory.models import Event, Venue, Series, EventInstance

class EventInstanceAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'event', 'venue', 'format', 'series')

admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(Series)
admin.site.register(EventInstance, EventInstanceAdmin)