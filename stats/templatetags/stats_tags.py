from django import template

from stats.models import Visitor

register = template.Library()


@register.filter
def get_visitors(cat):
    return Visitor.objects.filter(place__category=cat)
