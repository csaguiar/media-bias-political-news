# Fetch and parse articles from Google News
Pull articles from Google News RSS from politics topics.

# Usage
1) Initialize module:
`sg = ScrapeGoogleNews(url=<RSS URL>)`

RSS URL defaults to Politics topics on Google News localized to US

2) Fetch links from RSS:
`sg.fetch_links()`

3) Download articles using [newspaper](https://newspaper.readthedocs.io/en/latest/) library
`sg.fetch_articles()`

4) Save articles to disk
`sg.save_articles_to_disk()`
