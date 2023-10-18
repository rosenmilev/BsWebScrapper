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
			results = soup.find_all('h3')

			context = {
				'results': results,
				'form': form
			}
			return render(request, 'scrape/result.html', context)
	else:
		form = ScrapeForm()

	return render(request, 'scrape/index.html', {'form': form})

