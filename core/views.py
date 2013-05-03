# -*- coding: utf-8 -*-
from django.views.generic import DetailView

from models import *


class IndexView(DetailView):
    template_name = 'index.html'
    context_object_name = 'obj'

    def get_object(self):
        try:
            return Profile.objects.all()[0]
        except IndexError:
            return

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        ctx['first_urls'] = HttpRequest.objects.all()[:10]
        return ctx
