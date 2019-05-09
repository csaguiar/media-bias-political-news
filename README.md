# Predicting Political Bias in News Articles

This project is intended to use Natural Language Processing and Deep Learning to predict media bias. The project is currently in the stage of data collection using the following sources of data:

- Google News RSS (Politics category): This method uses [Beautiful Soup](https://launchpad.net/beautifulsoup) to parse the RSS in order to collect news urls. These urls are then parsed using [newspaper](https://newspaper.readthedocs.io/en/latest/) library.

- Webhose.IO (Politics Category): Pull news articles from [Webhose.IO](https://webhose.io) using the filter for politics news only.

- Webhose.IO (Predetermined domains): Use predetermined domains based on the [Media Bias Chart](https://www.adfontesmedia.com/) dataset.

- [All The News](https://components.one/datasets/all-the-news-articles-dataset/) dataset: 204,135 articles from 18 American publications, a subset of which was used in a Kaggle competition.

# News Outlets

*Liberal bias label:* The New Yorker, Mother Jones, The Daily Beast, Slate, Vanity Fair, CNN, The Washington Post, The Guardian, The New York Times, Politico, The Atlantic, NBC

*Conservative bias label:* Fox News, National Review, The Washington Times, Reason, The Federalist, New York Post, Daily Mail, Washington Examiner


# To do:

- Data Cleaning for the most relevant news outlets

- Web based tool for article labelling

- First pass on the Machine Learning model architecture
