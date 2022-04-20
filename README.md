# mtv_viacom_capstone

## Introduction
This github repository contains all of the data, code, and analysis from our capstone project in partnership with MTV. In this study we looked at voting access on college campuses in 2012, 2016, 2018, and 2020. We used distance from the college campus to the nearest polling place as a proxy for access. The source data and code files can be used to recreate our intermediate files and consequently run our analysis files. All code files should be run in numerical order within a folder. Our final presentation slides and report can be found in the 40_docs folder.

<img align="center" width="614" alt="Screen Shot 2022-04-20 at 5 32 20 PM" src="https://user-images.githubusercontent.com/30974949/164326523-3e959034-ce9a-4d36-b5e2-17e7fe02a667.png">


## Long-Term Planning
Our long-term planning can be found in this Gantt Chart: https://docs.google.com/spreadsheets/d/1HWH5hh6ox8acLfQ1_6jpGFs9mc5kYe1hEaEqWNq4oJg/edit?usp=sharing

## Short-Term Planning
Our short term task management is shown via the Github Issues tab of this repository.

## File Table of Contents

### 00_source_data Folder
In this folder we have our original data files. Our polling data for 2012, 2016, 2018, and 2020 comes from the Center for Public Integrity. It was added to this folder after it was geocoded with geocodio. Our 2020 & 2018 early voting data from Ballot Ready is also in this folder. This folder also holds our original college campus, college demographic, and college enrollment data.

### 10_code Folder
In this folder we have code files that help us prepare our source data, merge data sources together, and conduct meaningful analysis. We will explain some of the most important files in our code folder.

##### 10_prepare_data Sub-Folder
This sub-folder contains all of the code used to clean and prepare college campus data and polling place data. There are files that clean polling data from each year, early voting data, and our college polygons. Below the college polygon file details are given as an example:

   File Name: 10_import_HIFLD_College_Polygons.py  <br>
   Description: Loading and Cleaning HIFLD data. <br>
   Input: 00_source_data/HIFLD_CollegeUniversityCampuses/HIFLD_CollegeUniversityCampuses.shp <br>
   Output: /20_intermediate_files/10_HIFLD_campus_polygons.csv <br>
<br>

##### 20_merge_data Sub-Folder
This sub-folder contains all of the code used to merge college campus data, college demographic data, and polling place data. There are files that merge college campuses with college demographic information, calculate the distance to the nearest polling place for each college, and merge college enrollment data with the nearest polling place information. Below the college demographic and enrollment file details are given as an example:

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

##### 30_analysis Sub-Folder
This sub-folder contains all of our analysis notebooks and code used to add relevant analysis details (like region or urban/rural census designation). There are files that connect our data with the google distance API to obtain travel times, add regions, and add an urban/rural census designation. Our analysis files detail our temporal analysis, our urban/rural analysis, our dropbox analysis, and other analysis areas. Below the distance API, regions, and 2012-2018 results file details are given as an example:

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

### 20_intermediate_files Folder
In this folder we have any files that were output from our 10_code folder files. We have our cleaned polling place files and files from our campus merges. One of our most important intermediate files is '30_campuses_w_dist_to_nearest_pp.geojson' because it contains all campuses with their nearest polling place and is the basis for much of our analysis.

### 40_docs Folder
In this folder we have our important documents from the course of the project. Our backwards design and team charter are documents from the beginning of our project. Our major semester milestone and end of semester report were intermediate deliverables to our capstone client. And finally we have our final report and symposium slides as our final capstone deliverables.



