from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from scrape.forms import ScrapeForm


def index(request):
	if request.method == "POST":
		form = ScrapeForm(request.POST)
		if form.is_valid():
			URL = form.cleaned_data['url']
			page = requests.get(URL)
			soup = BeautifulSoup(page.content, 'html.parser')

			needed_info = form.cleaned_data['data_needed']
			results = ''
			if needed_info == 'text':
				results = soup.text
			elif needed_info == 'headings':
				heading_tags = ["h1", "h2", "h3"]
				results = []
				for tag in soup.find_all(heading_tags):
					results.append(tag)

			elif needed_info == 'links':
				results = soup.find_all('a', href=True)

			context = {
				'results': results,
				'form': form
			}
			return render(request, 'scrape/result.html', context)
	else:
		form = ScrapeForm()

	return render(request, 'scrape/index.html', {'form': form})

