import requests
from bs4 import BeautifulSoup


class CrawlerStage:
    def crawl_page(self, url):
        #url = f"https://en.wikipedia.org/wiki/{page_name}"
        title, text = self.scrapeWikiArticle(url)
        return title, text

    def scrapeWikiArticle(self, url):
        response = requests.get(url=url,)
    
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find(id="firstHeading")
        scrapeResults = self.getAllParagraphFromPage(soup)

        return title, scrapeResults

    def getAllParagraphFromPage(self, soup):
        allParagraph = soup.find(id="bodyContent").find_all("p")
        results = []
        for paragraph in allParagraph:
            if (len(paragraph.text.strip()) > 0):
                results.append(paragraph.text.strip())
        return results
