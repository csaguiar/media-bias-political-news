# Predicting Political Bias in News Articles

This project uses Natural Language Processing and deep learning approaches to predict political bias by media outlets based on news article texts. The project is currently in the stage of data collection using the following sources of data:

- Google News RSS (Politics category): This method uses [Beautiful Soup](https://launchpad.net/beautifulsoup) to parse the RSS in order to collect news urls. These urls are then parsed using [newspaper](https://newspaper.readthedocs.io/en/latest/) library.

- Webhose.IO (Politics Category): Pull news articles from [Webhose.IO](https://webhose.io) using the filter for politics news only.

- Webhose.IO (Predetermined domains): Use predetermined domains based on the [Media Bias Chart](https://www.adfontesmedia.com/) dataset.

- [All The News](https://components.one/datasets/all-the-news-articles-dataset/) dataset: 204,135 articles from 18 American publications, a subset of which was used in a Kaggle competition.

# News Outlets

### Predicting liberal vs. conservative bias
(Listed in order of factual ranking based on MediaBiasFactCheck.com)

**Liberal bias label:** NBC News, The New York Times, The Washington Post, The Guardian, The New Yorker, The Atlantic, Slate, The Daily Beast, Vanity Fair, Mother Jones, MSNBC, CNN (Online News)

**Conservative bias label:** National Review, The Weekly Standard, Reason, Washington Examiner, The Washington Times, The American Conservative, The Federalist, New York Post, Daily Mail, Fox News

### Predicting degree of bias
Source classification was based on triangulation between the AllSides Bias Rating and MediaBiasFactCheck.com.
\* means that both AllSides Bias Rating and MediaBiasFactCheck.com both concur on category membership.
+ means the AllSides "Community Feedback" was either "somewhat agree" or "agree".
Any source classified as a "Questionable Source" (e.g., Breitbart) by MediaBiasFactCheck.com was excluded.

**Central:** Associated Press (AP)\*+, Reuters\*+, The Christian Science Monitor\*, FiveThirtyEight+, BBC News+, Forbes+, USA Today+

**Biased Level 1:** The Atlantic\*+, The Guardian\*+, The Washington Post\*+, Reason\*+, The Washington Times\*+, NBC News\*, The New York Times\*, Washington Examiner+

**Biased Level 2:** The New Yorker\*+, CNN\*, Mother Jones\*+, MSNBC\*+, Slate\*+, Democracy Now!\*+, Daily Beast\*+, The Federalist\*+, The Blaze\*+, The Daily Caller\*+, The Daily Wire\*+, National Review\*+, Daily Mail+


# To do:

- Data Cleaning for the most relevant news outlets

- Web based tool for article labelling

- First pass on the Machine Learning model architecture
