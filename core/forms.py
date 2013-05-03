from django import forms
from django.conf import settings

from models import Profile


class DatePickerWidget(forms.widgets.DateInput):

    class Media:
        css = {'all': (settings.STATIC_URL + 'css/jquery.ui.all.css',)}
        js = (
            settings.STATIC_URL + 'js/jquery.ui.core.js',
            settings.STATIC_URL + 'js/jquery.ui.widget.js',
            settings.STATIC_URL + 'js/jquery.ui.datepicker.js',
        )

    def __init__(self, **attrs):
        super(DatePickerWidget, self).__init__(**attrs)


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        widgets = {'birthday': DatePickerWidget}
