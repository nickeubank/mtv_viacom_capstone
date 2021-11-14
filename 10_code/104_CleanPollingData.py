import geopandas as gpd
import numpy as np
import pandas as pd
import glob

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

#Load 2020 Data
p20 = pd.read_csv("../20_intermediate_files/final_2020_polling.csv")
p20 = p20.replace(r"^\s*$", np.nan, regex=True)
p20 = p20.astype({"latitude_left": "float"})
p20 = p20.astype({"longitude_left": "float"})
p20 = gpd.GeoDataFrame(p20, geometry=gpd.points_from_xy(p20.longitude_left, p20.latitude_left))
p20 = p20[['latitude_left','longitude_left','state','address','geometry']]
p20 = p20.rename(columns={'latitude_left': 'Latitude', 'longitude_left': 'Longitude', 'state': 'State'})
p20 = p20.set_crs(epsg=4326)
p20 = p20.to_crs(wkt)
p20.to_file("../20_intermediate_files/2020_clean.geojson", driver='GeoJSON')

#Load 2018 Data

p18 = gpd.read_file('../Data/2018 Polling Data/2018 Geocoded Polling Data.csv')
p18 = gpd.GeoDataFrame(
    p18, geometry=gpd.points_from_xy(p18.Longitude, p18.Latitude)
)
p18 = p18.set_crs(epsg=4326)
p18 = p18.to_crs(wkt)
p18 = p18.drop_duplicates()
p18 = p18[['Latitude','Longitude','State','address','geometry']]
p18.to_file("../20_intermediate_files/2018_clean.geojson", driver='GeoJSON')

#Load 2016 Data

p16 = gpd.read_file('../Data/2016 Polling Data/2016 Geocoded Polling Data.csv')
p16 = gpd.GeoDataFrame(
    p16, geometry=gpd.points_from_xy(p16.Longitude, p16.Latitude)
)
p16 = p16.set_crs(epsg=4326)
p16 = p16.to_crs(wkt)
p16 = p16.drop_duplicates()
p16 = p16[['Latitude','Longitude','State','address','geometry']]
p16.to_file("../20_intermediate_files/2016_clean.geojson", driver='GeoJSON')

#Load 2012 Data

p12 = gpd.read_file("../00_source_data/2012 Geocoded Polling Data.csv")
p12 = p12[p12['Latitude'] != '0']
p12 = p12.drop_duplicates()
p12 = p12[['Latitude','Longitude','State','address','geometry']]
p12 = gpd.GeoDataFrame(
    p12, geometry=gpd.points_from_xy(p12.Longitude, p12.Latitude)
)
p12 = p12.set_crs(epsg=4326)
p12 = p12.to_crs(wkt)
p12 = p12.drop_duplicates()
p12 = p12[['Latitude','Longitude','State','address','geometry']]
p12.to_file("../20_intermediate_files/2012_clean.geojson", driver='GeoJSON')



