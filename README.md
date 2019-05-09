# Predicting Political Bias in News Articles

This project uses Natural Language Processing and deep learning approaches to predict political bias by media outlets based on news article texts. The project is currently in the stage of data collection using the following sources of data:

- Google News RSS (Politics category): This method uses [Beautiful Soup](https://launchpad.net/beautifulsoup) to parse the RSS in order to collect news urls. These urls are then parsed using [newspaper](https://newspaper.readthedocs.io/en/latest/) library.

- Webhose.IO (Politics Category): Pull news articles from [Webhose.IO](https://webhose.io) using the filter for politics news only.

- Webhose.IO (Predetermined domains): Use predetermined domains based on the [Media Bias Chart](https://www.adfontesmedia.com/) dataset.

- [All The News](https://components.one/datasets/all-the-news-articles-dataset/) dataset: 204,135 articles from 18 American publications, a subset of which was used in a Kaggle competition.

# News Outlets

### Predicting liberal vs. conservative bias
(Listed in order of factual ranking based on MediaBiasChart.com)

**Liberal bias label:** NBC News, The New York Times, The Washington Post, Politico, The Guardian, The New Yorker, The Atlantic, Slate, The Daily Beast, Vanity Fair, Mother Jones, MSNBC, CNN (Online News)

**Conservative bias label:** National Review, The Weekly Standard, Reason, Washington Examiner, The Washington Times, The American Conservative, The Federalist, New York Post, Daily Mail, Fox News

### Predicting degree of bias
Source classification was based on triangulation between MediaBiasFactCheck and AllSides Bias Rating. Sources where AllSides "Community Feedback" is either "somewhat agree" or "agree" are starred.

**Central:** Associated Press (AP)\*, Reuters\*, NPR (Online News)\*, BBC\*, The Hill, The Christian Science Monitor, Bloomberg, Al Jazeera, Wall Street Journal (Online News)

**Biased Level 1:** The Atlantic\*, The Guardian\*, The Washington Post\*, Reason\*, Washington Examiner\*, The Washington Times\*, Fox News, CNN (Online News), NBC News, The New York Times, Politico

**Biased Level 2:** Mother Jones\*, MSNBC\*, The New Yorker\*, Slate\*, Democracy Now!\*, The Daily Beast\*, The Federalist\*, Breitbart\*, The Blaze\*, The Daily Caller\*, Daily Mail\*, The Daily Wire\*, National Review\*


# To do:

- Data Cleaning for the most relevant news outlets

- Web based tool for article labelling

- First pass on the Machine Learning model architecture
