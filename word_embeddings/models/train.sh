python train.py --dataset ../../data_processed/webhose_google_with_bias_label_5_10.csv --output wb_gn_5_10_full --num-words 100000 &&
python train.py --dataset ../../data_processed/webhose_google_with_bias_label_5_10.csv --output wb_gn_5_10_liberal --num-words 100000 --select 0 &&
python train.py --dataset ../../data_processed/webhose_google_with_bias_label_5_10.csv --output wb_gn_5_10_conservative --num-words 100000 --select 1 &&
python train.py --dataset ../../data_processed/ALL_NEWS_bias_label.csv --output atn_5_10_full --num-words 100000 &&
python train.py --dataset ../../data_processed/ALL_NEWS_bias_label.csv --output atn_5_10_liberal --num-words 100000 --select 0 &&
python train.py --dataset ../../data_processed/ALL_NEWS_bias_label.csv --output atn_5_10_conservative --num-words 100000 --select 1
