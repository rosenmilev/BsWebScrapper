from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ScrapeForm(forms.Form):
    url = forms.URLField(
        label='Website URL',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        initial='http://',
        required=True
    )

    action_type = forms.ChoiceField(
        label='Select what you want to do:',
        choices=[('key_words', 'Extract 20 most used keywords with frequencies'),
                 ('all_words', 'Extract all words tokenized'), ('text', 'Extract plain text')],
        widget=forms.Select(attrs={'class': 'form-control custom-select'})
    )

    website_language = forms.ChoiceField(
        label='Choose language of the website you want to scrape:',
        choices=[('english', 'English'), ('bulgarian', 'Bulgarian')],
        widget=forms.Select(attrs={'class': 'form-control custom-select'})
    )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')