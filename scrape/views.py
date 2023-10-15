from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def index(request):
	output = []
	URL = "https://realpython.github.io/fake-jobs/"
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find(id="ResultsContainer")
	job_elements = results.find_all("div", class_="card-content")
	results = results.prettify()
	for job_element in job_elements:
		title = job_element.find('h2', class_='title')
		company = job_element.find('h3', class_='company')
		location = job_element.find('p', class_='location')
		output.append([title.text, company.text, location.text])

	context = {

		'result': output
	}
	return render(request, 'index.html', context)