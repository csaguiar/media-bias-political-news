python train.py --dataset ../../data_processed/dataset_with_bias_label.csv --output wb_gn_full --num-words 50000 && 
python train.py --dataset ../../data_processed/dataset_with_bias_label.csv --output wb_gn_liberal --num-words 50000 --select 0 &&
python train.py --dataset ../../data_processed/dataset_with_bias_label.csv --output wb_gn_conservative --num-words 50000 --select 1 &&
python train.py --dataset ../../data_processed/ALL_NEWS_bias_label.csv --output atn_full --num-words 50000 &&
python train.py --dataset ../../data_processed/ALL_NEWS_bias_label.csv --output atn_liberal --num-words 50000 --select 0 &&
python train.py --dataset ../../data_processed/ALL_NEWS_bias_label.csv --output atn_conservative --num-words 50000 --select 1
