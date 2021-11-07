import geopandas
import numpy as np
import pandas as pd
import glob
from matplotlib import pyplot as plt

#Load Safegraph
sg = geopandas.read_file('../00_source_data/2020 Polling Data/polling_pk_master_post.csv')
sg = sg.replace(r'^\s*$', np.nan, regex=True)
sg = sg.astype({'latitude': 'float'})
sg = sg.astype({'longitude': 'float'})
sg = geopandas.GeoDataFrame(
    sg, geometry=geopandas.points_from_xy(sg.longitude, sg.latitude))

#Load and Concatenate CPI
path = r'../00_source_data/2020_Polling_ByState' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = geopandas.read_file(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
cpi = geopandas.GeoDataFrame(frame)

#Tidy Up Lat/Long
def get_lat(row):
    if len(row.geog.replace('(','').replace(')','').strip('POINT').split()) == 0:
        lat = float('NaN')
    else:
        lat = float(row.geog.replace('(','').replace(')','').strip('POINT').split()[1])
    return lat
def get_long(row):
    if len(row.geog.replace('(','').replace(')','').strip('POINT').split()) == 0:
        long = float('NaN')
    else:
        long = float(row.geog.replace('(','').replace(')','').strip('POINT').split()[0])
    return long

cpi['latitude'] = cpi.apply(lambda row: get_lat(row), axis=1)
cpi['longitude'] = cpi.apply(lambda row: get_long(row), axis=1)

#Limit Safegraph to CPI's State List
state_list = list(cpi['state'].unique())
sg_adjusted = sg[sg['address.state'].isin(state_list)]

#Tidy Up CPI
cpi_adjusted = cpi[['state','name','address','geog','latitude','longitude']]
cpi_adjusted = cpi_adjusted.drop_duplicates()
cpi_adjusted = cpi_adjusted.dropna(subset=['latitude', 'longitude'])


###
#Let's Try Buffering
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
cpi_geo = geopandas.GeoDataFrame(cpi_adjusted, geometry=geopandas.points_from_xy(cpi_adjusted.longitude, cpi_adjusted.latitude))
cpi_geo = cpi_geo.set_crs(epsg=4326)
cpi_geo = cpi_geo.to_crs(wkt)
cpi_geo = cpi_geo.reset_index()

sg_geo = geopandas.GeoDataFrame(sg_adjusted, geometry='geometry')
sg_geo = sg_geo.set_crs(epsg=4326)
sg_geo = sg_geo.to_crs(wkt)

#Buffer and Then Merge
buffer = 200
cpi_geo.geometry = cpi_geo.geometry.buffer(buffer)
geo_join = cpi_geo.sjoin(sg_geo, how="left", predicate='contains')

#Make file smaller
geo_join = geo_join[['state','name','address','latitude_left','longitude_left','geometry','pollingHours']]

geo_join.to_csv("../20_intermediate_files/final_2020_polling.csv", index=False)
