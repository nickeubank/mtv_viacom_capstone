import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import geopy.distance
from shapely.ops import nearest_points

polling = pd.read_csv(
    "../20_intermediate_files/final_2020_polling.csv"
)
early = pd.read_csv("../00_source_data/2020 Polling Data/earlyVote_pk_master.csv")
dropoff = pd.read_csv("../00_source_data/2020 Polling Data/dropoff_pk_master.csv")

#Data Cleaning Before Creating Geodataframe
polling = polling.replace(r"^\s*$", np.nan, regex=True)
polling = polling.astype({"latitude_left": "float"})
polling = polling.astype({"longitude_left": "float"})
polling_gdf = gpd.GeoDataFrame(
    polling, geometry=gpd.points_from_xy(polling.longitude_left, polling.latitude_left)
)
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
polling_gdf = polling_gdf.set_crs(epsg=4326)
polling_gdf = polling_gdf.to_crs(wkt)
polling_gdf.head()

# Load Final List of Colleges and Subset of Colleges

subset_col = gpd.read_file("../20_intermediate_files/10_HIFLD_campus_polygons.geojson")
subset_col = subset_col.set_crs(wkt,allow_override=True)

#Subset By CPI States
state_list = list(polling_gdf['state'].unique())
subset_college = subset_col[subset_col['STATE'].isin(state_list)]

# Get distance to nearest
college_trad_poll = subset_college.sjoin_nearest(polling_gdf, distance_col="distances")
#Rename
college_trad_poll = college_trad_poll.rename(columns={'latitude_left': 'Latitude_right', 'longitude_left': 'Longitude_right'})
#Add Miles
college_trad_poll['distance_miles'] = college_trad_poll['distances']/1609.34

college_trad_poll.to_csv(
    "../20_intermediate_files/subset_college_nearest_poll_2020.csv", index=False
)



