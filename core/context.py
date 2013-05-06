from django.conf import settings

from models import HttpRequest


def variables(request):
    context_extras = {}
    context_extras['DJSETTINGS'] = settings
    context_extras['FIRST_REQ'] = HttpRequest.objects.all().order_by('-priority')[:10]
    return context_extras
