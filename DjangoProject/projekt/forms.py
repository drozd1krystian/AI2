from django import forms

names = (('BTC','BTC'),('ETH','ETH'),('XRP','XRP'),('LTC','LTC'),('TRX','TRX'))
class NameForm(forms.Form):
    coin_name = forms.ChoiceField(choices=names,required = True, widget=forms.Select(
    attrs={'class': 'btn btn-warning'}))
