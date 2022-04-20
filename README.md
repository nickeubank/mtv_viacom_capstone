# mtv_viacom_capstone

## Introduction
This github repository contains all of the data, code, and analysis from our capstone project in partnership with MTV. In this study we looked at voting access on college campuses in 2012, 2016, 2018, and 2020. We used distance from the college campus to the nearest polling place as a proxy for access. The source data and code files can be used to recreate our intermediate files and consequently run our analysis files. All code files should be run in numerical order within a folder. Our final presentation slides and report can be found in the 40_docs folder.

## Long-Term Planning
Our long-term planning can be found in this Gantt Chart: https://docs.google.com/spreadsheets/d/1HWH5hh6ox8acLfQ1_6jpGFs9mc5kYe1hEaEqWNq4oJg/edit?usp=sharing

## Short-Term Planning
Our short term task management is shown via the Github Issues tab of this repository.

## File Table of Contents
#### 10_code
##### 10_prepare_data
1.  File Name: 10_import_HIFLD_College_Polygons.py  <br>
   Description: Loading and Cleaning HIFLD data. <br>
   Input: 00_source_data/HIFLD_CollegeUniversityCampuses/HIFLD_CollegeUniversityCampuses.shp <br>
   Output: /20_intermediate_files/10_HIFLD_campus_polygons.csv <br>
<br>

##### 20_merge_data
   File Name: 10_merging_HIFLD_w_demographics.py  <br>
   Description: Merging the HIFLD and demographics data through inner join and manual matching <br>
   Input: 20_intermediate_files/10_HIFLD_campus_polygons.geojson and 00_source_data/PlusOne_College_Demographic_Data/SLSV Master Campus Sheet - Master Sheet.csv <br>
   Output: 20_intermediate_files/20_campus_polygons_w_demographics.geojson" <br>
<br>
   File Name: college_enrollment_data.py  <br>
   Description: Merging the college name and the enrollment data (HD2020 and EF2020B) <br>
   Input:/00_source_data/college_enrollment_data/college_name.csv and 00_source_data/college_enrollment_data/enrollment_data.csv <br>
   Output: /20_intermediate_files/college_enrollment_data_merge.csv <br>
<br>

##### 30_analysis

   File Name: 112_distance_api.py <br>
   Description: Calculates the Driving, Walking, Transit time and duration from the college and its nearest polling location through the Google Maps API <br>
   Input: 30_campuses_w_dist_to_nearest_pp.geojson<br>
   Output: /20_intermediate_files/30_campuses_w_dist_to_nearest_pp.geojson <br>
<br>

   File Name: 120_regions.py <br>
   Description: Appending Region to each state <br>
   Input: /20_intermediate_files/30_campuses_w_dist_to_nearest_pp.csv <br>
   Output: /20_intermediate_files/30_campuses_w_dist_to_nearest_pp.csv <br>
<br>

   File Name: 2012_2016_2018_results.ipynb <br>
   Description: Yearly results using the Google API <br>

<br>

-----------------------------------------------------------------------
   File Name: 102_2020Merge.py <br>
   Description: Merges the CPI and Safegraph polling data using a buffer. <br>
   Input: 00_source_data/2020 Polling Data/polling_pk_master_post.csv and 00_source_data/2020_Polling_ByState <br>
   Output: 20_intermediate_files/final_2020_polling.csv <br>
<br>
   File Name: 105_NearestPolling_01.py <br>
   Description: Finds the nearest polling place to each campus polygon and calculates distance in meters. <br>
   Input: 20_intermediate_files/final_2020_polling.csv and 20_intermediate_files/10_HIFLD_campus_polygons.geojson <br>
   Output: 20_intermediate_files/subset_college_nearest_poll_2020.csv <br>
<br>

   File Name: 110_ARCGIS_College_Polygons.py <br>
   Description: Computes the centroid of the data, text preprocessing from ARCGIS shape file and stores as a geojson and csv. <br>
   Input: 00_source_data/CollegeUniversityCampuses/CollegeUniversityCampuses.shp <br>
   Output: 00_source_data/College_Data/Raw_College_Polygon.csv and 00_source_data/College_Data/Raw_College_Polygon.geojson <br>
<br>

   File Name: 111_merging_arcgis_master.py <br>
   Description: Performs text preprocessing for the +1 Master College Table and inner joins with the raw college polygon file. <br>
   Input: /00_source_data/College_Data/Raw_College_Polygon.geojson and /00_source_data/College_Data/SLSV Master Campus Sheet - Master         Sheet.csv (+1 Master College Data) <br>
   Output: /00_source_data/College_Data/Merged_College_Polygon.csv <br>
<br>


