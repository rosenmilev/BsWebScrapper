from django import forms


class ScrapeForm(forms.Form):
    url = forms.URLField(
        label='Website URL',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        initial='http://',
        required=True
    )

    data_needed = forms.ChoiceField(
        label='Select type of data you want to scrap:',
        choices=[('text', 'Text'), ('headings', 'Headings'), ('links', 'Links')],
        widget=forms.Select(attrs={'class': 'form-control custom-select'})
    )