# -*- coding: utf-8 -*-
from django.views.generic import DetailView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from models import *
from forms import ProfileForm


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class IndexView(DetailView):
    template_name = 'index.html'
    context_object_name = 'obj'

    def get_object(self):
        try:
            return Profile.objects.all()[0]
        except IndexError:
            return


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'profile_edit.html'
    form_class = ProfileForm
    success_url = reverse_lazy('index')

    def get_object(self):
        return Profile.objects.all()[0]
