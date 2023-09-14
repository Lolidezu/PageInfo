from django import forms

class UrlForm(forms.Form):
    url = forms.CharField(label='Enter website URL', max_length=2000)
