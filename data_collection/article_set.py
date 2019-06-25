import csv
from datetime import datetime

# Path to file where CSV data, in the format of the
# Kaggle/Components dataset, is saved
BASE_CSV_PATH = "data_raw"


class ArticleSet:
    """Class to handle set of articles while fetching from remote."""

    def _filename(self):
        datetime_now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        return "{}/{}_{}.csv" \
            .format(BASE_CSV_PATH, self.base_name, datetime_now)

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

        with open(self._filename(), 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_data)

        csv_file.close()
