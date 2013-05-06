from django.contrib import admin

from models import Profile, HttpRequest
from sorl.thumbnail.admin import AdminImageMixin


class ProfileAdmin(AdminImageMixin, admin.ModelAdmin):
    pass
admin.site.register(Profile, ProfileAdmin)


class HttpRequestAdmin(admin.ModelAdmin):

    list_display = ('url', 'time', 'priority')
    list_filter = ('time', 'priority')

admin.site.register(HttpRequest, HttpRequestAdmin)
