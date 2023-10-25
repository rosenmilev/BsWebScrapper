from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
from django.urls import reverse
from django.views.generic import CreateView

from scrape.forms import ScrapeForm, CustomUserCreationForm, SaveDataForm
from .models import ScrapedData
from .utils import tokenize_text_to_words, get_keywords, filter_words
from bs4 import BeautifulSoup


@login_required
def index(request):
	success_flag = request.GET.get('success')
	if request.method == "POST":
		form = ScrapeForm(request.POST)
		if form.is_valid():
			URL = form.cleaned_data['url']
			try:
				page = requests.get(URL)
				page.raise_for_status()
			except requests.exceptions.RequestException as e:
				if 'Max retries exceeded with url' in str(e):
					e = 'URL not found'
				else:
					e = 'Unexpected error'

				return render(request, 'error.html', {'error_message': e})
			result = ''
			scraped_data = BeautifulSoup(page.content, 'html.parser')

			action_type = form.cleaned_data['action_type']
			language = form.cleaned_data['website_language']
			text = scraped_data.text

			if action_type == 'text':
				result = scraped_data.text.strip()
			else:
				tokens = tokenize_text_to_words(text)
				filtered_tokens = filter_words(tokens, language)

				if action_type == 'key_words':
					result = get_keywords(filtered_tokens)
				if action_type == 'all_words':
					result = filtered_tokens

			request.session['scraped_content'] = result
			request.session['scraped_url'] = URL

			context = {
				'results': result,
				'form': form,
				'url': URL,
				'action': action_type,
			}
			return render(request, 'result.html', context)
	else:
		form = ScrapeForm()

	return render(request, 'index.html', {'form': form, 'success_flag': success_flag})


def register(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('index')
	else:
		form = CustomUserCreationForm()
	return render(request, 'registration/register.html', {'form': form})


@login_required
def save_data(request):
	scraped_content = request.session.get('scraped_content', '')
	scraped_url = request.session.get('scraped_url', '')
	user = request.user
	success = None

	save_form = SaveDataForm(initial={'website_url': scraped_url, 'scraped_content': scraped_content})

	if request.method == "POST":
		save_form = SaveDataForm(request.POST)
		if save_form.is_valid():
			save_form.instance.user = user
			save_form.save()

			return HttpResponseRedirect(reverse('index') + f'?success=OK')

	context = {
		'scraped_content': scraped_content,
		'scraped_url': scraped_url,
		'form': save_form
	}
	return render(request, 'save_data.html', context)
