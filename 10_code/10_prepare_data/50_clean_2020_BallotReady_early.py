import geopandas as gpd
import numpy as np
import pandas as pd
import glob
from matplotlib import pyplot as plt

# Load Ballot Ready Early Voting
data = pd.read_excel('../../00_source_data/Early Voting Data/BallotReady_2018_2020_Early Voting Data.xlsx',sheet_name='2020 In-Person Early Voting')

###
# Creat Geodataframe
###

from shapely import wkt
data['st_astext'] = data['st_astext'].apply(wkt.loads)
data = gpd.GeoDataFrame(data,geometry='st_astext')

#Project and Save 
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

data_geo = data.set_crs(epsg=4326)
data_geo = data_geo.to_crs(wkt)

data_geo.to_file(
    "../../20_intermediate_files/10_polling_places/2020_BallotReady_Early.geojson",
    driver="GeoJSON",
)
