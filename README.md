# mtv_viacom_capstone

## Long-Term Planning
Our long-term planning can be found in this Gantt Chart: https://docs.google.com/spreadsheets/d/1HWH5hh6ox8acLfQ1_6jpGFs9mc5kYe1hEaEqWNq4oJg/edit?usp=sharing

## Short-Term Planning
Our short term task management is shown via the Github Issues tab of this repository.

## File Table of Contents

1. File Name: 102_2020Merge.py <br>
   Description: Merges the CPI and Safegraph polling data using a buffer. <br>
   Input: 00_source_data/2020 Polling Data/polling_pk_master_post.csv and 00_source_data/2020_Polling_ByState <br>
   Output: 20_intermediate_files/final_2020_polling.csv <br>
<br>

2. File Name: 105_NearestPolling_01.py <br>
   Description: Finds the nearest polling place to each campus polygon and calculates distance in meters. <br>
   Input: 20_intermediate_files/final_2020_polling.csv and 20_intermediate_files/10_HIFLD_campus_polygons.geojson <br>
   Output: 20_intermediate_files/subset_college_nearest_poll_2020.csv <br>
<br>

3. File Name: 110_ARCGIS_College_Polygons.py <br>
   Description: Computes the centroid of the data, text preprocessing from ARCGIS shape file and stores as a geojson and csv. <br>
   Input: 00_source_data/CollegeUniversityCampuses/CollegeUniversityCampuses.shp <br>
   Output: 00_source_data/College_Data/Raw_College_Polygon.csv and 00_source_data/College_Data/Raw_College_Polygon.geojson <br>
<br>

4. File Name: 111_merging_arcgis_master.py <br>
   Description: Performs text preprocessing for the +1 Master College Table and inner joins with the raw college polygon file. <br>
   Input: /00_source_data/College_Data/Raw_College_Polygon.geojson and /00_source_data/College_Data/SLSV Master Campus Sheet - Master         Sheet.csv (+1 Master College Data) <br>
   Output: /00_source_data/College_Data/Merged_College_Polygon.csv <br>
<br>

5. File Name: 112_distance_api.py <br>
   Description: Calculates the Driving, Walking, Transit time and duration from the college and its nearest polling location through the Google Maps API <br>
   Input: Have to add in the command line (argument) the nearest college polling data from /20_intermediate_files/. For example: 
   ```python 112_distance_api.py subset_college_nearest_poll_2016``` <br>
   Output: /20_intermediate_files/subset_college_nearest_poll_2016_distanceAPI.csv <br>
<br>
