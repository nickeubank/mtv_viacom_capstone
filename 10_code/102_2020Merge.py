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

#Merge on Latitude/Longitude
new_df = pd.merge(sg_adjusted, cpi_adjusted, how="inner",on=["latitude","longitude"])
print(len(new_df))
new_df.head()

###
#Try rounding Latitude/Longitude to x decimal places
###

def inner_match(n,sg_adjusted,cpi_adjusted):
    temp_sg = sg_adjusted.copy()
    temp_cpi = cpi_adjusted.copy()
    temp_sg['latitude'] = round(temp_sg['latitude'],n)
    temp_sg['longitude'] = round(temp_sg['longitude'],n)
    temp_cpi['latitude'] = round(temp_cpi['latitude'],n)
    temp_cpi['longitude'] = round(temp_cpi['longitude'],n)
    temp_cpi = temp_cpi.reset_index()
    new_df = pd.merge(temp_sg, temp_cpi, how="inner",on=["latitude","longitude"])
    return new_df
def track_merge():
    unique_matches = []
    cpi_overlap = []
    sg_overlap = []
    for i in range(2,30):
        rounddf = inner_match(i,sg_adjusted,cpi_adjusted)
        uniq_q = rounddf.drop_duplicates(subset="query_id")
        uniq_i = rounddf.drop_duplicates(subset="index")
        #Overlap is the number of excess unique values that appear
        cpi_overlap.append(len(uniq_q['query_id'].unique()) - len(uniq_q['index'].unique()))
        sg_overlap.append(len(uniq_i['index'].unique()) - len(uniq_i['query_id'].unique()))
        unique_matches.append(min(len(uniq_i['query_id'].unique()),len(uniq_i['index'].unique())))
    return pd.DataFrame({"Unique Matches":unique_matches, "CPI Overlap":cpi_overlap, "SG Overlap":sg_overlap})

final_df = track_merge()

f1 = plt.figure()
f2 = plt.figure()
f3 = plt.figure()
ax1 = f1.add_subplot(111)
ax2 = f2.add_subplot(111)
ax3 = f3.add_subplot(111)

#Plot Num of Matches
ax1.plot(final_df.index,final_df['Unique Matches'],linestyle='-', marker='o')
ax1.set_xlabel('Number of Decimals')
ax1.set_ylabel('Matches')
ax1.set_title('Matches by Decimal Rounding')

#Plot CPI Overlap
ax2.plot(final_df.index,final_df['CPI Overlap'],linestyle='-', marker='o')
ax2.set_xlabel('Number of Decimals')
ax2.set_ylabel('CPI Overlap')
ax2.set_title('CPI Overlap by Decimal Rounding')

#Plot SG Overlap
ax3.plot(final_df.index,final_df['SG Overlap'],linestyle='-', marker='o')
ax3.set_xlabel('Number of Decimals')
ax3.set_ylabel('SG Overlap')
ax3.set_title('SG Overlap by Decimal Rounding')

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

def track_buffer():
    unique_matches = []
    cpi_overlap = []
    sg_overlap = []
    buffer_vals = []
    div = 10000000000.0
    for i in range(1,200):
        cpi_geo_temp = cpi_geo.copy()
        #Add buffer
        cpi_geo_temp.geometry = cpi_geo_temp.geometry.buffer(i/div)
        #Join
        geo_join = cpi_geo_temp.sjoin(sg_geo, how="inner", predicate='contains')
        #Check for overlap
        uniq_q = geo_join.drop_duplicates(subset="query_id")
        uniq_i = geo_join.drop_duplicates(subset="index")
        cpi_overlap.append(len(uniq_q['query_id'].unique()) - len(uniq_q['index'].unique()))
        sg_overlap.append(len(uniq_i['index'].unique()) - len(uniq_i['query_id'].unique()))
        unique_matches.append(min(len(uniq_i['query_id'].unique()),len(uniq_i['index'].unique())))
        buffer_vals.append(i/div)
    return pd.DataFrame({"Unique Matches":unique_matches, "CPI Overlap":cpi_overlap, "SG Overlap":sg_overlap, "Buffer Value":buffer_vals})

#Can take a few minutes to run
geo_df = track_buffer()

f4 = plt.figure()
f5 = plt.figure()
f6 = plt.figure()
ax4 = f4.add_subplot(111)
ax5 = f5.add_subplot(111)
ax6 = f6.add_subplot(111)

#Plot Matches
ax4.plot(geo_df['Buffer Value'],geo_df['Unique Matches'],linestyle='-', marker='o')
ax4.set_xlabel('Buffer Value')
ax4.set_ylabel('Number of Matches')
ax4.set_title('Number of Matches by Buffer Value')

#Plot CPI Overlap
ax5.plot(geo_df['Buffer Value'],geo_df['CPI Overlap'],linestyle='-', marker='o')
ax5.set_xlabel('Buffer Value')
ax5.set_ylabel('CPI Overlap')
ax5.set_title('CPI Overlap by Buffer Value')

#Plot SG Overlap
ax6.plot(geo_df['Buffer Value'],geo_df['SG Overlap'],linestyle='-', marker='o')
ax6.set_xlabel('Buffer Value')
ax6.set_ylabel('SG Overlap')
ax6.set_title('SG Overlap by Buffer Value')

plt.show()