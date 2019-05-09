# Predicting Political Bias in News Articles

This project uses Natural Language Processing and deep learning approaches to predict political bias by media outlets based on news article texts. The project is currently in the stage of data collection using the following sources of data:

- Google News RSS (Politics category): This method uses [Beautiful Soup](https://launchpad.net/beautifulsoup) to parse the RSS in order to collect news urls. These urls are then parsed using [newspaper](https://newspaper.readthedocs.io/en/latest/) library.

- Webhose.IO (Politics Category): Pull news articles from [Webhose.IO](https://webhose.io) using the filter for politics news only.

- Webhose.IO (Predetermined domains): Use predetermined domains based on the [Media Bias Chart](https://www.adfontesmedia.com/) dataset.

- [All The News](https://components.one/datasets/all-the-news-articles-dataset/) dataset: 204,135 articles from 18 American publications, a subset of which was used in a Kaggle competition.

# News Outlets
Classification was based on triangulation between the AllSides Bias Rating and MediaBiasFactCheck.com.
A \* means that both AllSides Bias Rating and MediaBiasFactCheck.com both concur on category membership.
A + means the AllSides "Community Feedback" was either "somewhat agree" or "agree".
Any source classified as a "Questionable Source" (e.g., Breitbart) by MediaBiasFactCheck.com was excluded.

### Predicting liberal vs. conservative bias

**Liberal bias label:** The New Yorker\*+, Mother Jones\*+, MSNBC\*+, Slate\*+, The Atlantic\*+, The Guardian\*+, The Washington Post\*+, The New York Times\*, CNN\*, NBC News\*

**Conservative bias label:** Reason\*+, The Washington Times\*+, National Review\*+, Washington Examiner+, The Federalist\*+, Fox News\*, New York Post\*+, The Blaze\*+, The Daily Caller\*+, The Daily Wire\*+

### Predicting degree of bias

**Central:** Associated Press (AP)\*+, Reuters\*+, The Christian Science Monitor\*, FiveThirtyEight+, BBC News+, Forbes+, USA Today+

**Biased Level 1:** The Atlantic\*+, The Guardian\*+, The Washington Post\*+, Reason\*+, The Washington Times\*+, NBC News\*, The New York Times\*, Washington Examiner+

**Biased Level 2:** The New Yorker\*+, CNN\*, Mother Jones\*+, MSNBC\*+, Slate\*+, Democracy Now!\*+, Daily Beast\*+, The Federalist\*+, The Blaze\*+, The Daily Caller\*+, The Daily Wire\*+, National Review\*+, Daily Mail+


# To do:

- Data Cleaning for the most relevant news outlets

- Web based tool for article labelling

- First pass on the Machine Learning model architecture
