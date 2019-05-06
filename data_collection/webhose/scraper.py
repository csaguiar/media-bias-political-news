import webhoseio
import time
from datetime import datetime, timedelta
from dateutil.parser import parse
from data_collection.article_set import ArticleSet


class AttrDict(dict):
    """Class to access dictionary keys as attributtes"""
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class WebhoseScrape(ArticleSet):
    """Use Webhose.io API to collect political news from U.S."""
    def __init__(self, *args, **kwargs):
        self.base_name = "webhose"
        self.token = kwargs.get("token")
        self.articles = []

    def _build_query(self, domain, only_politics):
        queries = [
            "thread.country:US",
            "language:english",
            "site_type:news"
        ]
        if domain is not None:
            queries.append("site:" + domain)

        if only_politics:
            queries.append("site_category:politics")

        return queries

    def _get_params(self, domain, only_politics):
        queries = self._build_query(domain, only_politics)
        time_30_days = datetime.now() + timedelta(-30)

        return {
            "q": " ".join(queries),
            "sort": "crawled",
            "ts": time_30_days.strftime('%s')
        }

    def _reset_news(self):
        self.articles = []

    def fetch_articles(self, *args, **kwargs):
        """Uses Webhose IO to fetch articles

        Args:
            **kwargs: - domain: Source Domain
                      - num_pages: Number of pages to fetch
                      - waiting_time: Waiting time between requests
                      - only_politics: Returns only politics articles
                        (Defaults to True)
        """
        domain = kwargs.get("domain")
        num_pages = kwargs.get("num_pages", 1)
        waiting_time = kwargs.get("waiting_time", 100)
        only_politics = kwargs.get("only_politics", True)
        webhoseio.config(token=self.token)
        self._reset_news()
        params = self._get_params(domain, only_politics)
        output = webhoseio.query("filterWebContent", params)
        for i in range(0, num_pages):
            for post in output["posts"]:
                publish_date = parse(post["thread"]["published"])
                article = AttrDict({
                    "title": post["thread"]["title"],
                    "source_url": post["thread"]["site_full"],
                    "authors": post["author"],
                    "publish_date": publish_date,
                    "url": post["url"],
                    "text": post["text"]
                })
                self.articles.append(article)

            if num_pages > 1:
                print("Saving page {}".format(i + 1))
                self.save_articles_to_csv()
                self._reset_news()

            if i < num_pages-1:
                message = "Waiting {} seconds. Next page {}"
                print(message.format(waiting_time, i + 2))
                time.sleep(waiting_time)
                output = webhoseio.get_next()
