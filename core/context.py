from django.conf import settings


def variables(request):
    context_extras = {}
    context_extras['DJSETTINGS'] = settings
    return context_extras
