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

    def _get_params(self, domain):
        queries = [
            "site_category:politics",
            "thread.country:US",
            "language:english",
            "site_type:news"
        ]
        if domain is not None:
            queries.append("site:" + domain)

        time_30_days = datetime.now() + timedelta(-30)

        return {
            "q": " ".join(queries),
            "sort": "crawled",
            "ts": time_30_days.strftime('%s')
        }

    def _reset_news(self):
        self.articles = []

    def fetch_articles(self, domain=None, num_pages=1):
        """Uses newspaper library to download and parse the article"""
        webhoseio.config(token=self.token)
        self._reset_news()
        output = webhoseio.query("filterWebContent", self._get_params(domain))
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
                print("Waiting 100 seconds. Next page {}".format(i + 2))
                time.sleep(120)
                output = webhoseio.get_next()
