import geopandas as gpd
import numpy as np
import pandas as pd
import glob
from matplotlib import pyplot as plt

# Load Ballot Ready Early Voting 2020
data = pd.read_excel('../../00_source_data/Early_Voting_Data/BallotReady_2018_2020_Early Voting Data.xlsx',sheet_name='2020 In-Person Early Voting')

# Load Ballot Ready Early Voting 2018
data18 = pd.read_excel('../../00_source_data/Early_Voting_Data/BallotReady_2018_2020_Early Voting Data.xlsx',sheet_name='2018 In Person Early Voting')

#Dropoff
drop20 = pd.read_excel('../../00_source_data/Early_Voting_Data/BallotReady_2018_2020_Early Voting Data.xlsx',sheet_name='2020 Dropoff Locations')
drop18 = pd.read_excel('../../00_source_data/Early_Voting_Data/BallotReady_2018_2020_Early Voting Data.xlsx',sheet_name='2018 Dropoff Locations')

###
# Creat Geodataframe
###

from shapely import wkt
data['st_astext'] = data['st_astext'].apply(wkt.loads)
data = gpd.GeoDataFrame(data,geometry='st_astext')

#Drop NA geometries in 2018
data18 = data18[data18['st_astext'].notna()]
data18['st_astext'] = data18['st_astext'].apply(wkt.loads)
data18 = gpd.GeoDataFrame(data18,geometry='st_astext')

drop20['st_astext'] = drop20['st_astext'].apply(wkt.loads)
drop20 = gpd.GeoDataFrame(drop20,geometry='st_astext')

#Drop NA geometries in 2018
drop18 = drop18[drop18['st_astext'].notna()]
drop18['st_astext'] = drop18['st_astext'].apply(wkt.loads)
drop18 = gpd.GeoDataFrame(drop18,geometry='st_astext')

#Project and Save 
data_geo = data.set_crs(epsg=4326)
data18_geo = data18.set_crs(epsg=4326)
drop18_geo = drop18.set_crs(epsg=4326)
drop20_geo = drop20.set_crs(epsg=4326)

data_geo.to_file(
    "../../20_intermediate_files/10_polling_places/2020_BallotReady_Early.geojson",
    driver="GeoJSON",
)
data18_geo.to_file(
    "../../20_intermediate_files/10_polling_places/2018_BallotReady_Early.geojson",
    driver="GeoJSON",
)
drop18_geo.to_file(
    "../../20_intermediate_files/10_polling_places/2018_BallotReady_Dropoff_Early.geojson",
    driver="GeoJSON",
)
drop20_geo.to_file(
    "../../20_intermediate_files/10_polling_places/2020_BallotReady_Dropoff_Early.geojson",
    driver="GeoJSON",
)
