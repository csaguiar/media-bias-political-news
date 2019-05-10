"""Fetches articles from Webhose API and saves to a set of CSV Files"""
import os
from data_collection.webhose.scraper import WebhoseScrape

liberal_news = [
    "newyorker.com",
    "motherjones.com",
    "slate.com",
    "msnbc.com",
    "vanityfair.com",
    "cnn.com",
    "washingtonpost.com",
    "theguardian.com",
    "nytimes.com",
    "politico.com",
    "democracynow.org",
    "npr.org",
    "theatlantic.com",
    "nbcnews.com"
]

conservative_news = [
    "spectator.org",
    "foxnews.com",
    "nationalreview.com",
    "reason.com",
    "dailywire.com",
    "thefederalist.com",
    "washingtontimes.com",
    "washingtonexaminer.com",
    "nypost.com",
    "theblaze.com",
    "dailycaller.com"
]

if __name__ == '__main__':
    api_key = os.environ['WEBHOSE_API_KEY']
    for domain in liberal_news + conservative_news:
        print("============================================================")
        print("FETCHING {}".format(domain))
        print("============================================================")
        base_name = "webhose_{}".format(domain)
        sc = WebhoseScrape(token=api_key, base_name=base_name)
        sc.fetch_articles(num_pages=2, only_politics=False, domain=domain)
