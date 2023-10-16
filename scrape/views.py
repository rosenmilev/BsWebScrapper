from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def index(request):
	output_all_jobs = []
	output_python_jobs = []
	URL = "https://realpython.github.io/fake-jobs/"
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find(id="ResultsContainer")
	job_elements = results.find_all("div", class_="card-content")

	def html_to_text(html_result, output):
		for el in html_result:
			title = el.find('h2', class_='title')
			company = el.find('h3', class_='company')
			location = el.find('p', class_='location')
			if title:
				output.append([title.text, company.text, location.text])
		return output

	python_jobs = results.find_all(
		"h2", string=lambda text: "python" in text.lower()
	)

	html_to_text(job_elements, output_all_jobs)
	html_to_text(python_jobs, output_python_jobs)

	context = {

		'all_jobs': output_all_jobs,
		'python_jobs': output_python_jobs
	}
	return render(request, 'index.html', context)