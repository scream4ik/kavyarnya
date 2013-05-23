from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404

from models import *


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class StatsView(LoginRequiredMixin, ListView):
    template_name = 'stats.html'
    context_object_name = 'obj'
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser and not self.request.user.is_staff:
            raise Http404
        return super(StatsView, self).get(request, *args, **kwargs)
