from django import forms


class ScrapeForm(forms.Form):
    url = forms.URLField(
        label='Website URL',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        initial='http://'
    )