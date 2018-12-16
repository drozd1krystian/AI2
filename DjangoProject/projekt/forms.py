from django import forms

class NameForm(forms.Form):
    coin_name = forms.CharField( required = True)

    def clean_renewal_date(self):
        data = self.cleaned_data['coin_name']

        return data
