from django.contrib import admin

from models import Category, Place, Visitor
from forms import VisitorAdminInlineFormset


admin.site.register(Category)


class VisitorAdminInline(admin.TabularInline):
    formset = VisitorAdminInlineFormset
    model = Visitor
    extra = 1


class PlaceAdmin(admin.ModelAdmin):

    inlines = [VisitorAdminInline, ]

admin.site.register(Place, PlaceAdmin)
