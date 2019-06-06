# Script to train word embeddings

This folder contains the final embeddings for training in 6 different datasets:

- `wb_gn_full`: Webhose and Google News with all articles
- `wb_gn_conservative`: Webhose and Google News with only conservative sources
- `wb_gn_liberal`: Webhose and Google News with with only liberal sources
- `atn_full`: "All the news" dataset with all articles
- `atn_conservative`: "All the news" dataset with only conservative sources
- `atn_liberal`: "All the news" dataset with with only liberal sources

This version uses an embedding size of 128, vocabulary size of 10000 words, skip window size 1 and It was trained for 100000 steps.

## Usage

**Mandatory arguments**:

`--dataset <file name>`: CSV file with the dataset, in the format `content, label`

`--output <base name>`: Base name to build the files with embeddings and vocalulary (Dict: `{"dictionary": dictionary, "reversed_dictionary": reversed_dictionary}`)

**Optional argument**:

`--select <label>`: Label to be used in the training, using the column `label` of the CSV file

```
python train.py --dataset <file name> --output <base name> [--select <label>]
```
