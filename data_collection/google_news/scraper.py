from bs4 import BeautifulSoup
from newspaper import Article
import base64
import requests
import sys

# Default RSS URL from google news for politics topics localized to US
DEFAULT_URL = "https://news.google.com/rss/topics/CAAqBwgKMPLc8gowgtnZAg?hl=en-US&gl=US&ceid=US:en"


# From: https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
def progress(count, total, status=''):
    """Displays an inline progress bar"""
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


class ScrapeGoogleNews:
    """Scrape Google News RSS to save article texts"""

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get("url", DEFAULT_URL)
        # List of URL for each news article
        self.links = []
        # List of Article objects
        self.articles = []

    def _reset_data(self):
        self.links = []
        self.articles = []

    def fetch_links(self):
        """Fetches articles links from Google News RSS links"""
        self._reset_data()
        request = requests.get(self.url)
        data = request.text
        all_items = BeautifulSoup(data,  "xml").find_all("item")
        count = 0
        total = len(all_items)
        for item in all_items:
            link = item.find("link")
            if link:
                self.links.append(link.text)
            progress(count, total - 1, "Fetching Links")
            count += 1

    def fetch_articles(self):
        """Uses newspaper library to download and parse the article"""
        count = 0
        total = len(self.links)

        for link in self.links:
            article = Article(link)
            article.download()
            article.parse()
            self.articles.append(article)
            progress(count, total - 1, "Fetching Articles")
            count += 1

    def save_articles_to_disk(self):
        """Writes each article into a file with name defined by the url b64 encoded"""
        for article in self.articles:
            filename = base64.b64encode(article.url.encode('utf-8')).decode("utf-8")
            f = open(filename, "w")
            f.write(article.text)
            f.close()
