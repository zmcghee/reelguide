from django.contrib import admin
from repertory.models import *

class EventInstanceAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'event', 'venue', 'format', 'series')

admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(Series)
admin.site.register(EventInstance, EventInstanceAdmin)
admin.site.register(ReelUser)