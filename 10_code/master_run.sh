
# Data Prep
cd 10_prepare_data
python 10_import_HIFLD_College_Polygons.py
python 20_clean_2020_cpi_polling_data.py
python 30_clean_2012_2016_2018_cpi_polling_data.py
python 40_clean_2020_safegraph_polling_data.py

cd ../20_merge_data
