import webhoseio
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

    def _get_params(self):
        return {
            "q": "site_category:politics thread.country:US site_type:news"
        }

    def fetch_articles(self):
        """Uses newspaper library to download and parse the article"""
        webhoseio.config(token=self.token)
        output = webhoseio.query("filterWebContent", self._get_params())
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
