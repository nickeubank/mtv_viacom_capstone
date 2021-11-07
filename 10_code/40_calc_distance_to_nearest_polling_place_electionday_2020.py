import pandas as pd
import geopandas as gpd
import numpy as np

# Load Polling Place Data (2020)

polling = gpd.read_file(
    "../00_source_data/2020 Polling Data/polling_pk_master_post.csv"
)
early = gpd.read_file("../00_source_data/2020 Polling Data/earlyVote_pk_master.csv")
dropoff = gpd.read_file("../00_source_data/2020 Polling Data/dropoff_pk_master.csv")


# Data cleaning before creating GeoDataFrame
polling = polling.replace(r"^\s*$", np.nan, regex=True)
polling = polling.astype({"latitude": "float"})
polling = polling.astype({"longitude": "float"})
polling_gdf = gpd.GeoDataFrame(
    polling, geometry=gpd.points_from_xy(polling.longitude, polling.latitude)
)


polling_gdf.head()


# Load Final List of Colleges and Subset of Colleges
subset_col = gpd.read_file(
    "../20_intermediate_files/20_campus_polygons_w_demographics.geojson"
)


# Find Nearest Traditional Polling Place for Subset of Colleges
polling_gdf = polling_gdf.set_crs(epsg=4326)

# Project into US Equidistant Conic
# https://en.wikipedia.org/wiki/Equidistant_conic_projection
# Still includes hawaii and Alaska, but not built for them so
# probably shouldn't trust those states.
# https://epsg.io/102005

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

subset_college = subset_college.to_crs(wkt)
polling_gdf = polling_gdf.to_crs(wkt)

# Get distance to nearest
college_trad_poll = subset_college.sjoin_nearest(polling_gdf, distance_col="distances")

college_trad_poll.to_csv(
    "../20_intermediate_files/subset_college_nearest_poll_2020.csv", index=False
)


# Find Nearest Early Voting Place for Subset of Colleges


# Data cleaning before creating GeoDataFrame
early = early.replace(r"^\s*$", np.nan, regex=True)
early = early.astype({"latitude": "float"})
early = early.astype({"longitude": "float"})
early_gdf = gpd.GeoDataFrame(
    early, geometry=gpd.points_from_xy(early.longitude, early.latitude)
)

early_gdf = early_gdf.set_crs(epsg=4326)
early_gdf = early_gdf.to_crs(wkt)

# Subset our college to only states with early voting data
state_list = list(early_gdf["address.state"].unique())
college_early = subset_college[subset_college["State"].isin(state_list)]

# Get distance to nearest
college_early = college_early.sjoin_nearest(early_gdf, distance_col="distances")

college_early.to_csv(
    "../20_intermediate_files/subset_college_nearest_early_poll_2020.csv", index=False
)
