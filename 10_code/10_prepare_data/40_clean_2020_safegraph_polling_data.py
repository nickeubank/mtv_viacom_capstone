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


sg_geo = geopandas.GeoDataFrame(sg, geometry="geometry")
sg_geo = sg_geo.set_crs(epsg=4326)
#sg_geo = sg_geo.to_crs(wkt)

sg_geo.to_file(
    "../../20_intermediate_files/10_polling_places/2020_safegraph.geojson",
    driver="GeoJSON",
)
