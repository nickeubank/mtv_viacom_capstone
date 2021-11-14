import geopandas as gpd
import numpy as np
import pandas as pd

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
    pp_df = pp_df.to_crs(wkt)
    pp_df = pp_df.drop_duplicates()
    pp_df = pp_df[["Latitude", "Longitude", "State", "address", "geometry"]].copy()
    pp_df = pp_df.rename({"State": "state"}, axis="columns")
    pp_df.to_file(
        f"../../20_intermediate_files/10_polling_places/{year}_elecday_cpi.geojson",
        driver="GeoJSON",
    )
