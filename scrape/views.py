from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from scrape.forms import ScrapeForm
from django.http import Http404



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

			soup = BeautifulSoup(page.content, 'html.parser')
			needed_info = form.cleaned_data['data_needed']
			results = ''
			if needed_info == 'text':
				results = soup.text
			elif needed_info == 'headings':
				heading_tags = ["h1", "h2", "h3"]
				results = []
				for tag in soup.find_all(heading_tags):
					results.append(tag.text.strip())

			elif needed_info == 'links':
				results = soup.find_all('a', href=True)

			context = {
				'results': results,
				'form': form
			}
			return render(request, 'result.html', context)
	else:
		form = ScrapeForm()

	return render(request, 'index.html', {'form': form})

