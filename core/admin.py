from django.contrib import admin

from models import Profile
from sorl.thumbnail.admin import AdminImageMixin


class ProfileAdmin(AdminImageMixin, admin.ModelAdmin):
    pass
admin.site.register(Profile, ProfileAdmin)
