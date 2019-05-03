from data_collection.webhose.scraper import WebhoseScrape

API_KEY = "e63cf4c3-05ee-4d9c-aa6d-9a7921a7d70c"

sc = WebhoseScrape(token=API_KEY)
sc.fetch_articles(num_pages=200)


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
