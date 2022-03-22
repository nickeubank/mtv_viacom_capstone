import pandas as pd
import geopandas as gpd
import numpy as np


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

# Load Final List of Colleges and Subset of Colleges
campuses = gpd.read_file(
    "../../20_intermediate_files/20_campus_polygons_w_demographics.geojson"
)
#Drop excess columns
campuses = campuses.drop(columns=['SLSV Coalition', 'ALL IN', 'AGF', 'Ask Every Student', 'Campus Vote Project','Voter Friendly Campus', 'StudentPIRGs', 'Aliento Education Fund', 'Alliance for Youth Organizing', 'American Democracy Project', 
                   " Arizona Students' Association", 'Baltimore Collegetown Network\t\t', 'Black Girls Vote', 
                   'Boston Votes Coalition', 'California Campus Compact ', 'CALPIRG Students', 'CEEP', 'Civic Nebraska', 
                   'Common Cause', 'Count US IN', 'Creative Campus Voting Project', 'Day on Democracy', 'Democracy Works', 
                   'Engage Miami', 'Every Vote Counts', 'Forward Montana', 'Georgia Shift', 'Hillel International', 
                   'IGNITE National', 'IA & MN Campus Compact', 'LeadMN', 'Loud Light', 'Maine Students Vote', 'MARYPIRG', 
                   'MI Familia Vota', 'Minnesota Youth Collective', 'Mississippi Votes', 'NASPAA', 'New Era Colorado', 
                   'NYPIRG', 'NCAAT', 'NCPIRG', 'NC Campus Compact', 'Ohio Campus Compact', 'PIRGIM Campus Action', 
                   'Project Pericles', 'TurnUp Activism', 'Up to Us/ Net Impact', 'VoteRiders', 'Washington Student Association', 'Xceleader (Vote HBCU)', 'NVEW 2020', 'NVRD\n2017', 'NVRD 2018', 'NVRD 2020'])

campuses = campuses.to_crs(wkt)

campuses = campuses.copy()
print('Pre # of campuses: {}'.format(len(campuses)))

##################
#Get sets of states common to all polling place data
##################

#Load 2020 Early
p = gpd.read_file(
        f"../../20_intermediate_files/10_polling_places/2020_BallotReady_Early.geojson"
    )
ev_state_set = set(p['state'].unique())

#Load 2020 Election Day
q = gpd.read_file(
        f"../../20_intermediate_files/10_polling_places/2020_elecday_cpi.geojson"
    )
ed_state_set = set(q['state'].unique())

#Load 2012
r1 = gpd.read_file(
        f"../../20_intermediate_files/10_polling_places/2012_Polling_Clean/Tier1_2012_clean_23States_geocoded.csv"
    )
r2 = gpd.read_file(
        f"../../20_intermediate_files/10_polling_places/2012_Polling_Clean/Tier2_2012_clean_4States_geocoded.csv"
    )
r = pd.concat([r1,r2], ignore_index=True)
state_set_12 = set(r['State'].unique())

#Load 2016
s = gpd.read_file(
        f"../../00_source_data/2016_polling_data_cpi/2016_final_geocoded_geocodio_2.csv"
    )
state_set_16 = set(s['State'].unique())

#Load 2018
t = gpd.read_file(
        f"../../20_intermediate_files/10_polling_places/2018_Polling_Clean/cleaned_2018_polling_place.csv"
    )
state_set_18 = set(t['State'].unique())

max_state_set = ev_state_set.union(ed_state_set)
max_state_set = max_state_set.union(state_set_12)
max_state_set = max_state_set.union(state_set_16)
max_state_set = max_state_set.union(state_set_18)
    
#Limit campuses to those within our common states
campuses = campuses[campuses['STATE'].isin(max_state_set)]
print('Within State Set # of campuses: {}'.format(len(campuses)))
temp_list = []

p = p.to_crs(wkt)
q = q.to_crs(wkt)

assert campuses.crs == p.crs
if 'latitude' in q.columns:
    q = q.rename(columns={"latitude": "Latitude", "longitude": "Longitude"})
q = q[["state", "Latitude","Longitude","geometry"]]
year = '2020'
q = q.rename({"state": f"state_{year}"}, axis="columns")
q = q.rename({"Latitude": f"Latitude_{year}"}, axis="columns")
q = q.rename({"Longitude": f"Longitude_{year}"}, axis="columns")
    
# Get distance to nearest by looping through states, then concat
temp = pd.DataFrame()
for state in max_state_set:
    temp1 = pd.DataFrame()
    temp1 = campuses[campuses['STATE'] == state].sjoin_nearest(q[q[f"state_{year}"] == state], distance_col=f"distances_{year}", how="left")
    #Remove multiple equidistant polling places
    temp1 = temp1.drop_duplicates(subset=['UNIQUEID'], keep='last')
    temp = pd.concat([temp, temp1])

#Set final df
final_df = temp

##############################
#Add Ballot Ready Polling Data
##############################
p = gpd.read_file(
        f"../../20_intermediate_files/10_polling_places/2020_BallotReady_Early.geojson"
    )
p['Longitude'] = p['geometry'].x
p['Latitude'] = p['geometry'].y
p = p.to_crs(wkt)
#Save a copy of polling place geometries
p = p[["state", "Latitude", "Longitude", "geometry"]]
year = '2020_early'
p = p.rename({"state": f"state_{year}"}, axis="columns")
p = p.rename({"Latitude": f"Latitude_{year}"}, axis="columns")
p = p.rename({"Longitude": f"Longitude_{year}"}, axis="columns")
temp = pd.DataFrame()

#Loop through states and merge with final dataframe
for state in max_state_set:
    temp1 = pd.DataFrame()
    temp1 = campuses[campuses['STATE'] == state].sjoin_nearest(p[p[f"state_{year}"] == state], distance_col=f"distances_{year}", how="left")
    #Remove multiple equidistant polling places
    temp1 = temp1.drop_duplicates(subset=['UNIQUEID'], keep='last')
    temp = pd.concat([temp, temp1])
final_df = final_df.merge(temp.iloc[:,[0,-3,-2,-1]],on='UNIQUEID',how='inner')

######################
#Add 2012 Election Day
######################
r = gpd.GeoDataFrame(r,geometry=gpd.points_from_xy(r['Longitude'], r['Latitude']))
r = r.set_crs(epsg=4326)
r = r.to_crs(wkt)
#Save a copy of polling place geometries
r = r[["State", "Latitude", "Longitude", "geometry"]]
year = '2012'
r = r.rename({"State": f"state_{year}"}, axis="columns")
r = r.rename({"Latitude": f"Latitude_{year}"}, axis="columns")
r = r.rename({"Longitude": f"Longitude_{year}"}, axis="columns")
temp = pd.DataFrame()
#Loop through states and merge with final dataframe
for state in max_state_set:
    temp1 = pd.DataFrame()
    temp1 = campuses[campuses['STATE'] == state].sjoin_nearest(r[r[f"state_{year}"] == state], distance_col=f"distances_{year}", how="left")
    #Remove multiple equidistant polling places
    temp1 = temp1.drop_duplicates(subset=['UNIQUEID'], keep='last')
    temp = pd.concat([temp, temp1])
final_df = final_df.merge(temp.iloc[:,[0,-3,-2,-1]],on='UNIQUEID',how='inner')

######################
#Add 2016 Election Day
######################
s = gpd.GeoDataFrame(s,geometry=gpd.points_from_xy(s['Longitude'], s['Latitude']))
s = s.set_crs(epsg=4326)
s = s.to_crs(wkt)
#Save a copy of polling place geometries
s = s[["State", "Latitude", "Longitude", "geometry"]]
year = '2016'
s = s.rename({"State": f"state_{year}"}, axis="columns")
s = s.rename({"Latitude": f"Latitude_{year}"}, axis="columns")
s = s.rename({"Longitude": f"Longitude_{year}"}, axis="columns")
temp = pd.DataFrame()
#Loop through states and merge with final dataframe
for state in max_state_set:
    temp1 = pd.DataFrame()
    temp1 = campuses[campuses['STATE'] == state].sjoin_nearest(s[s[f"state_{year}"] == state], distance_col=f"distances_{year}", how="left")
    #Remove multiple equidistant polling places
    temp1 = temp1.drop_duplicates(subset=['UNIQUEID'], keep='last')
    temp = pd.concat([temp, temp1])
final_df = final_df.merge(temp.iloc[:,[0,-3,-2,-1]],on='UNIQUEID',how='inner')

######################
#Add 2018 Election Day
######################
t = gpd.GeoDataFrame(t,geometry=gpd.points_from_xy(t['Longitude'], t['Latitude']))
t = t.set_crs(epsg=4326)
t = t.to_crs(wkt)
#Save a copy of polling place geometries
t = t[["State", "Latitude", "Longitude", "geometry"]]
year = '2018'
t = t.rename({"State": f"state_{year}"}, axis="columns")
t = t.rename({"Latitude": f"Latitude_{year}"}, axis="columns")
t = t.rename({"Longitude": f"Longitude_{year}"}, axis="columns")
temp = pd.DataFrame()
#Loop through states and merge with final dataframe
for state in max_state_set:
    temp1 = pd.DataFrame()
    temp1 = campuses[campuses['STATE'] == state].sjoin_nearest(t[t[f"state_{year}"] == state], distance_col=f"distances_{year}", how="left")
    #Remove multiple equidistant polling places
    temp1 = temp1.drop_duplicates(subset=['UNIQUEID'], keep='last')
    temp = pd.concat([temp, temp1])
final_df = final_df.merge(temp.iloc[:,[0,-3,-2,-1]],on='UNIQUEID',how='inner')

######################
#Add Nearest Starbucks
######################
s = gpd.read_file(
        f"../../00_source_data/store_locations/Starbucks_USA.csv"
    )
s = gpd.GeoDataFrame(s,geometry=gpd.points_from_xy(s['Longitude'], s['Latitude']))
s = s.set_crs(epsg=4326)
s = s.to_crs(wkt)
#Save a copy of polling place geometries
s = s[["State", "Latitude", "Longitude", "geometry"]]
year = 'starbucks'
s = s.rename({"State": f"state_{year}"}, axis="columns")
s = s.rename({"Latitude": f"Latitude_{year}"}, axis="columns")
s = s.rename({"Longitude": f"Longitude_{year}"}, axis="columns")
temp = pd.DataFrame()
#Loop through states and merge with final dataframe
for state in max_state_set:
    temp1 = pd.DataFrame()
    temp1 = campuses[campuses['STATE'] == state].sjoin_nearest(s[s[f"state_{year}"] == state], distance_col=f"distances_{year}", how="left")
    #Remove multiple equidistant Starbucks
    temp1 = temp1.drop_duplicates(subset=['UNIQUEID'], keep='last')
    temp = pd.concat([temp, temp1])
final_df = final_df.merge(temp.iloc[:,[0,-3,-2,-1]],on='UNIQUEID',how='inner')

######################
#Add Nearest Target
######################
s = gpd.read_file(
        f"../../00_source_data/store_locations/Target_USA.csv"
    )
s = gpd.GeoDataFrame(s,geometry=gpd.points_from_xy(s['Longitude'], s['Latitude']))
s = s.set_crs(epsg=4326)
s = s.to_crs(wkt)
#Save a copy of polling place geometries
s = s[["State", "Latitude", "Longitude", "geometry"]]
year = 'target'
s = s.rename({"State": f"state_{year}"}, axis="columns")
s = s.rename({"Latitude": f"Latitude_{year}"}, axis="columns")
s = s.rename({"Longitude": f"Longitude_{year}"}, axis="columns")
temp = pd.DataFrame()
#Loop through states and merge with final dataframe
for state in max_state_set:
    temp1 = pd.DataFrame()
    temp1 = campuses[campuses['STATE'] == state].sjoin_nearest(s[s[f"state_{year}"] == state], distance_col=f"distances_{year}", how="left")
    #Remove multiple equidistant Targets
    temp1 = temp1.drop_duplicates(subset=['UNIQUEID'], keep='last')
    temp = pd.concat([temp, temp1])
final_df = final_df.merge(temp.iloc[:,[0,-3,-2,-1]],on='UNIQUEID',how='inner')

#Save to file
final_df.to_file(
    "../../20_intermediate_files/30_campuses_w_dist_to_nearest_pp.geojson",
    driver="GeoJSON")
final_df.to_csv(
    "../../20_intermediate_files/30_campuses_w_dist_to_nearest_pp.csv")
