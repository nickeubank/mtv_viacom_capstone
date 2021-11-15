import geopandas
import numpy as np
import pandas as pd
import glob
from matplotlib import pyplot as plt

# Load Safegraph
sg = geopandas.read_file(
    "../../00_source_data/2020_polling_data_safegraph/polling_pk_master_post.csv"
)
sg = sg.replace(r"^\s*$", np.nan, regex=True)
sg = sg.astype({"latitude": "float"})
sg = sg.astype({"longitude": "float"})
sg = geopandas.GeoDataFrame(
    sg, geometry=geopandas.points_from_xy(sg.longitude, sg.latitude)
)

###
# Project and save
###

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

sg_geo = geopandas.GeoDataFrame(sg, geometry="geometry")
sg_geo = sg_geo.set_crs(epsg=4326)
sg_geo = sg_geo.to_crs(wkt)

sg_geo.to_file(
    "../../20_intermediate_files/10_polling_places/2020_safegraph.geojson",
    driver="GeoJSON",
)
