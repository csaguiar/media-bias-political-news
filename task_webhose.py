"""Fetches articles from Webhose API and saves to a set of CSV Files"""
import os
import sys
from data_collection.webhose.scraper import WebhoseScrape

liberal_news = [
    "newyorker.com",
    "motherjones.com",
    "thedailybeast.com",
    "slate.com",
    "vanityfair.com",
    "cnn.com",
    "washingtonpost.com",
    "theguardian.com",
    "nytimes.com",
    "politico.com",
    "democracynow.org",
    "npr.org",
    "theatlantic.com"
]

conservative_news = [
    "spectator.org",
    "breitbart.com",
    "cbn.com",
    "foxnews.com",
    "nationalreview.com",
    "reason.com",
    "dailywire.com",
    "thefederalist.com",
    "wsj.com",
    "washingtontimes.com"
]

if __name__ == '__main__':
    api_key = os.environ['WEBHOSE_API_KEY']

    only_politics = False
    for arg in sys.argv:
        if arg == "--only-politics":
            only_politics = True

    if only_politics:
        print("============================================================")
        print("FETCHING ONLY POLITICS")
        print("============================================================")
        sc = WebhoseScrape(token=api_key, base_name="only-politics")
        sc.fetch_articles(num_pages=100, only_politics=True)
    else:
        for domain in liberal_news + conservative_news:
            print("============================================================")
            print("FETCHING PREDEFINED SOURCE: {}".format(domain))
            print("============================================================")
            base_name = "webhose_{}".format(domain)
            sc = WebhoseScrape(token=api_key, base_name=base_name)
            sc.fetch_articles(num_pages=2, only_politics=False, domain=domain)
