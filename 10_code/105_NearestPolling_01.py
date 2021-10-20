import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import geopy.distance
from shapely.ops import nearest_points

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


college = gpd.read_file(
    "../20_intermediate_files/final_college_polygons.csv",
    GEOM_POSSIBLE_NAMES="geometry",
    KEEP_GEOM_COLUMNS="NO",
)
print(len(college))


subset_college = gpd.read_file(
    "../20_intermediate_files/subset_final_college_polygon.csv",
    GEOM_POSSIBLE_NAMES="geometry",
    KEEP_GEOM_COLUMNS="NO",
)
print(len(subset_college))


# Find Nearest Traditional Polling Place for Subset of Colleges


college.crs = 4326
subset_college.crs = 4326
polling_gdf.crs = 4326


def nearest_poll_idx(row, polling_df):
    polling_index = polling_df["geometry"].distance(row.geometry).sort_values().index[0]
    return polling_index


def nearest_poll_dist(row, polling_df):
    polling_distance = (
        polling_df["geometry"].distance(row.geometry).sort_values().values[0]
    )
    return polling_distance


def nearest_poll_name(row, polling_df):
    polling_place_name = polling_df.loc[row.nearest_polling_index][
        "address.locationName"
    ]
    return polling_place_name


def nearest_poll_geom(row, polling_df):
    polling_place_geom = polling_df.loc[row.nearest_polling_index]["geometry"]
    return polling_place_geom


college_trad_poll = subset_college.copy()
college_trad_poll.head()

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


# Subset our college to only states with early voting data
state_list = list(early_gdf["address.state"].unique())
college_early = subset_college[subset_college["State_x"].isin(state_list)]


college_early.head()

college_early.to_csv(
    "../20_intermediate_files/subset_college_nearest_early_poll_2020.csv", index=False
)
