from bs4 import BeautifulSoup
from newspaper import Article
from datetime import datetime
import requests
import sys
import csv

# Default RSS URL from google news for politics topics localized to US
DEFAULT_URL = "https://news.google.com/rss/topics/CAAqBwgKMPLc8gowgtnZAg?hl=en-US&gl=US&ceid=US:en"

# Path to file where CSV data, in the format of the
# Kaggle/Components dataset, is saved
CSV_PATH = "data/google_news_{}.csv" \
                .format(datetime.now().strftime("%Y-%m-%d_%H:%M"))


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
        all_items = BeautifulSoup(data, "xml").find_all("item")
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
            try:
                article.download()
                article.parse()
                self.articles.append(article)
                progress(count, total - 1, "Fetching Articles")
                count += 1
            except:
                print("Error fetching {}".format(link))

    def save_articles_to_csv(self):
        """Saves article text and metadata to CSV"""
        csv_data = [
            ["title, publication, authors, date, year, month, url, content"]
        ]

        for article in self.articles:
            if article.publish_date is not None:
                publish_date = article.publish_date.strftime("%m-%d-%Y")
                publish_year = article.publish_date.year
                publish_month = article.publish_date.month
            else:
                publish_date, publish_year, publish_month = None, None, None
            csv_row = [
                article.title,
                article.source_url,
                article.authors,
                publish_date,
                publish_year,
                publish_month,
                article.url,
                article.text
            ]
            csv_data.append(csv_row)

        with open(CSV_PATH, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_data)

        csv_file.close()
