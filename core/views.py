# -*- coding: utf-8 -*-
from django.views.generic import DetailView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

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


class HttpRequestView(DetailView):
    template_name = 'http_request.html'
    context_object_name = 'obj'

    def get_object(self):
        return HttpRequest.objects.all().order_by('priority')[:10]

    def post(self, request, *args, **kwargs):
        pr = self.request.POST.get('pr', '')
        obj_pk = self.request.POST.get('obj_pk', '')

        if pr.strip():
            try:
                int(obj_pk)
            except TypeError:
                return HttpResponseRedirect(reverse_lazy('http_request'))

            p = get_object_or_404(HttpRequest, pk=obj_pk)
            if pr.strip() == 'increase':
                p.priority = p.priority - 1
            elif pr.strip() == 'decrease':
                p.priority = p.priority + 1
            p.save()

        return HttpResponseRedirect(reverse_lazy('http_request'))
