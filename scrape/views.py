from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import requests
from scrape.forms import ScrapeForm
from .utils import tokenize_text_to_words, get_keywords
from bs4 import BeautifulSoup


def index(request):
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
				result = scraped_data.get_text()
			elif action_type == 'key_words':
				tokens = tokenize_text_to_words(text)
				keywords_with_freq = get_keywords(tokens, language)
				result = keywords_with_freq
			elif action_type == 'all_words':
				result = tokenize_text_to_words(text)

			context = {
				'results': result,
				'form': form
			}
			return render(request, 'result.html', context)
	else:
		form = ScrapeForm()

	return render(request, 'index.html', {'form': form})

