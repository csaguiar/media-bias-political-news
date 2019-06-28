import sys
import json
from datetime import datetime
sys.path.append("../../preprocessing")
sys.path.append("../../word_embeddings/models")

from filter_articles import filter
from clean_articles import clean_dataset
from join_files import concat_files
from train import Input, Model

RAW_DATA_FOLDERS = ["../../data_raw/google_news", "../../data_raw/webhose"]

with open('../../preprocessing/contractions.json', 'r') as contractions_file:
    contractions_dict = json.load(contractions_file)


# Load Raw data and join in one file
print("=> PROCESSING RAW FILES")
dataset_raw = concat_files(RAW_DATA_FOLDERS)

# Clean unused articles
print("=> PROCESS TEXT")
dataset = (
    dataset_raw.pipe(filter)
               .pipe(clean_dataset, contractions_dict=contractions_dict)
)

print("=> SAVING DATA")
date_today = datetime.now().strftime("%Y_%m_%d")
# All data
filename_all = "webhose_google_news_{}.csv".format(date_today)
dataset.to_csv("../../data_processed/{}".format(filename_all), index=False)
# Only label
filename_bias = "../../data_processed/webhose_google_with_bias_label_{}.csv".format(date_today)
dataset[["content", "label"]].to_csv(filename_bias, index=False)
# Only level
filename_level = "../../data_processed/webhose_google_with_bias_level_{}.csv".format(date_today)
dataset[["content", "level"]].to_csv(filename_level, index=False)
