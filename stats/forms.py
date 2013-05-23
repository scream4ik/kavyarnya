from django import forms


class VisitorAdminInlineFormset(forms.models.BaseInlineFormSet):

    def clean(self):
        check = {}
        for form in self.forms:
            check[form.cleaned_data.get('type')] = check.get(form.cleaned_data.get('type'), 0) + 1
        for x in check.values():
            if x > 1:
                raise forms.ValidationError('Pls use unique types')
