# Fetch articles from Webhose IO
Pull articles using Webhose API and save them to a CSV file.

# Usage
1) Initialize module:
`sg = WebhoseScrape(token=<Webhose API TokenL>)`

Set up the API module to fetch new articles. The API token can be obtained from [webhose.io](https://webhose.io/)

2) Download articles from `filterWebContent` endpoint.
`sg.fetch_articles(domain=None, num_pages=1, waiting_time=100, only_politics=True)`

Optional parameters:

* `domain`: Source Domain (e.g. cnn.com or foxnews.com)
* `num_pages`: Number of pages to fetch (integer)
* `waiting_time`: Waiting time between requests (integer)
* `only_politics`: Returns only politics articles (boolean, defaults to True)

3) Save articles
* To a datetime labeled CSV file with columns [`title, publication, authors, date, year, month, url, content`]:
`sg.save_articles_to_csv()`
