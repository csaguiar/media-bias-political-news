DATE_REF="2019_06_28"

python train.py --dataset ../../data_processed/webhose_google_with_bias_label_${DATE_REF}.csv --output wb_gn_${DATE_REF}_full --num-words 100000 &&
python train.py --dataset ../../data_processed/webhose_google_with_bias_label_${DATE_REF}.csv --output wb_gn_${DATE_REF}_liberal --num-words 100000 --select 0 &&
python train.py --dataset ../../data_processed/webhose_google_with_bias_label_${DATE_REF}.csv --output wb_gn_${DATE_REF}_conservative --num-words 100000 --select 1 &&
python train.py --dataset ../../data_processed/ALL_NEWS_bias_label.csv --output atn_${DATE_REF}_full --num-words 100000 &&
python train.py --dataset ../../data_processed/ALL_NEWS_bias_label.csv --output atn_${DATE_REF}_liberal --num-words 100000 --select 0 &&
python train.py --dataset ../../data_processed/ALL_NEWS_bias_label.csv --output atn_${DATE_REF}_conservative --num-words 100000 --select 1
