import requests
from bs4 import BeautifulSoup
import random
import time
import sys, re

if len(sys.argv) != 2:
  sys.stderr.write('Usage: {} <Wiki Page Name>\n'.format(sys.argv[0]))
  exit(1)

wikiPageName = sys.argv[1]
url = "https://en.wikipedia.org/wiki/" + wikiPageName

def scrapeWikiArticle(url):
	response = requests.get(
		url=url,
	)
	
	soup = BeautifulSoup(response.content, 'html.parser')
	title = soup.find(id="firstHeading")
	scrapeResult = getAllParagraphFromPage(soup)

	# For testing purposes 
	printWikiPage(title, scrapeResult)

	allLinks = soup.find(id="bodyContent").find_all("a")
	random.shuffle(allLinks)
	linkToScrape = 0

	for link in allLinks:
		# slow down otherwise wiki server will block you
		# time.sleep(2)
		# We are only interested in other wiki articles
		if link['href'].find("/wiki/") == -1: 
			continue

		# Use this link to scrape
		linkToScrape = link
		break

	print('Link to scrape:\t{}'.format(linkToScrape['href']))
	# scrapeWikiArticle("https://en.wikipedia.org" + linkToScrape['href'])
	return scrapeResult


def getAllParagraphFromPage(soup):
	allParagraph = soup.find(id="bodyContent").find_all("p")
	results = []
	for paragraph in allParagraph:
		results.append(paragraph.text)
	return results

def printWikiPage(title, scrapeResult):
	print("===========Start of wiki page============")
	print('Title of the page:\t'.format(title.text))
	for scrapeParagraph in scrapeResult:
		print(scrapeParagraph)
	print("===========End of wiki page============\n\n")

scrapeWikiArticle(url)
# scrapeWikiArticle("https://en.wikipedia.org/wiki/El_Dorado_Fire")