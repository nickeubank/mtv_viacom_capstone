import geopandas as gpd
import numpy as np
import pandas as pd
import glob
from matplotlib import pyplot as plt

# Load Ballot Ready Early Voting
data = pd.read_excel('../../00_source_data/Early_Voting_Data/BallotReady_2018_2020_Early Voting Data.xlsx',sheet_name='2020 In-Person Early Voting')

###
# Creat Geodataframe
###

from shapely import wkt
data['st_astext'] = data['st_astext'].apply(wkt.loads)
data = gpd.GeoDataFrame(data,geometry='st_astext')

#Project and Save 

data_geo = data.set_crs(epsg=4326)
#data_geo = data_geo.to_crs(wkt)

data_geo.to_file(
    "../../20_intermediate_files/10_polling_places/2020_BallotReady_Early.geojson",
    driver="GeoJSON",
)
