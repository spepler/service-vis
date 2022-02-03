from django.contrib import admin
from servicevis.models import *

# Register your models here.
# customise the Rack admin interface
#class RackAdmin(admin.ModelAdmin):
#    list_display = ('name', 'room')
#    list_filter = ('room',)
#    ordering = ('name', 'room')
admin.site.register(Service)
admin.site.register(Link)
admin.site.register(Graph)
