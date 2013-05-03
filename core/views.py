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
