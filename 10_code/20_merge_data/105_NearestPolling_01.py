import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import geopy.distance
from shapely.ops import nearest_points

wkt = """PROJCS["USA_Contiguous_Equidistant_Conic",
        GEOGCS["GCS_North_American_1983",
            DATUM["North_American_Datum_1983",
                SPHEROID["GRS_1980",6378137,298.257222101]],
            PRIMEM["Greenwich",0],
            UNIT["Degree",0.017453292519943295]],
        PROJECTION["Equidistant_Conic"],
        PARAMETER["False_Easting",0],
        PARAMETER["False_Northing",0],
        PARAMETER["Longitude_Of_Center",-96],
        PARAMETER["Standard_Parallel_1",33],
        PARAMETER["Standard_Parallel_2",45],
        PARAMETER["Latitude_Of_Center",39],
        UNIT["Meter",1],
        AUTHORITY["EPSG","102005"]]"""

#Load 2020 Data
polling = gpd.read_file("../20_intermediate_files/2020_clean.geojson")
polling = polling.set_crs(wkt,allow_override=True)

# Load Final List of Colleges and Subset of Colleges

subset_col = gpd.read_file("../20_intermediate_files/20_campus_polygons_w_demographics.geojson")
subset_col = subset_col.set_crs(wkt,allow_override=True)

#Subset By CPI States
state_list = list(polling['State'].unique())
subset_college = subset_col[subset_col['STATE'].isin(state_list)]

# Get distance to nearest
college_trad_poll = subset_college.sjoin_nearest(polling, distance_col="distances")
#Rename
college_trad_poll = college_trad_poll.rename(columns={'latitude_left': 'Latitude_right', 'longitude_left': 'Longitude_right'})
#Add Miles
college_trad_poll = college_trad_poll.drop_duplicates(subset=['UNIQUEID'], keep='first')
college_trad_poll['distance_miles'] = college_trad_poll['distances']/1609.34

#Create 2020 File with all 50 states
college_full_poll = subset_col.sjoin_nearest(polling, distance_col="distances")
college_full_poll = college_full_poll.drop_duplicates(subset=['UNIQUEID'], keep='first')
college_full_poll['distance_miles'] = college_full_poll['distances']/1609.34
college_full_poll = college_full_poll.rename(columns={'Latitude_right': 'Latitude', 'Longitude_right': 'Longitude'})
college_full_poll.to_csv(
    "../20_intermediate_files/full_nearest_poll_2020.csv", index=False
)

#Repeat for 2018
p18 = gpd.read_file("../20_intermediate_files/2018_clean.geojson")
p18 = p18.set_crs(wkt,allow_override=True)
college_poll_18 = subset_college.sjoin_nearest(p18, distance_col="distances")
college_poll_18 = college_poll_18.drop_duplicates(subset=['UNIQUEID'], keep='first')
college_poll_18['distance_miles'] = college_poll_18['distances']/1609.34

#Repeat for 2016

p16 = gpd.read_file("../20_intermediate_files/2016_clean.geojson")
p16 = p16.set_crs(wkt,allow_override=True)
college_poll_16 = subset_college.sjoin_nearest(p16, distance_col="distances")
college_poll_16 = college_poll_16.drop_duplicates(subset=['UNIQUEID'], keep='first')
college_poll_16['distance_miles'] = college_poll_16['distances']/1609.34


#Repeat for 2012
p12 = gpd.read_file("../20_intermediate_files/2012_clean.geojson")
p12 = p12.set_crs(wkt,allow_override=True)
college_poll_12 = subset_college.sjoin_nearest(p12, distance_col="distances")
college_poll_12 = college_poll_12.drop_duplicates(subset=['UNIQUEID'], keep='first')
college_poll_12['distance_miles'] = college_poll_12['distances']/1609.34

#Concatenate Dataframes

college_trad_poll = college_trad_poll.rename(columns={'Latitude_right': 'Latitude', 'Longitude_right': 'Longitude'})
college_poll_18 = college_poll_18.rename(columns={'Latitude_right': 'Latitude', 'Longitude_right': 'Longitude'})
college_poll_16 = college_poll_16.rename(columns={'Latitude_right': 'Latitude', 'Longitude_right': 'Longitude'})
college_poll_12 = college_poll_12.rename(columns={'Latitude_right': 'Latitude', 'Longitude_right': 'Longitude'})
college_trad_poll['year'] = 2020
college_poll_18['year'] = 2018
college_poll_16['year'] = 2016
college_poll_12['year'] = 2012
mixed = [college_trad_poll, college_poll_18, college_poll_16, college_poll_12]
result = pd.concat(mixed)
result.to_csv(
    "../20_intermediate_files/concat_nearest_poll.csv", index=False
)