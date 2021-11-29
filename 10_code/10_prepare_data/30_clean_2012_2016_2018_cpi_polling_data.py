import geopandas as gpd
import numpy as np
import pandas as pd


# Load and project 2012-2018 Data

for year in ["2012", "2016", "2018"]:
    pp_df = gpd.read_file(
        f"../../00_source_data/{year}_polling_data_cpi/{year} Geocoded Polling Data.csv"
    )

    if year == "2012":
        pp_df = pp_df[pp_df["Latitude"] != "0"]

    pp_df = gpd.GeoDataFrame(
        pp_df, geometry=gpd.points_from_xy(pp_df.Longitude, pp_df.Latitude)
    )
    pp_df = pp_df.set_crs(epsg=4326)
    #pp_df = pp_df.to_crs(wkt)
    pp_df = pp_df.drop_duplicates()
    pp_df = pp_df[["Latitude", "Longitude", "State", "address", "geometry"]].copy()
    pp_df = pp_df.rename({"State": "state"}, axis="columns")
    pp_df.to_file(
        f"../../20_intermediate_files/10_polling_places/{year}_elecday_cpi.geojson",
        driver="GeoJSON",
    )
