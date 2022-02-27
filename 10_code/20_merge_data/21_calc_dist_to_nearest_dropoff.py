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

#Get sets of states common to all polling place data

p = gpd.read_file(
        f"../../20_intermediate_files/10_polling_places/2020_BallotReady_Dropoff_Early.geojson"
    )
state_set_20 = set(p['state'].unique())
q = gpd.read_file(
        f"../../20_intermediate_files/10_polling_places/2018_BallotReady_Dropoff_Early.geojson"
    )
#Fill in Missing States for 2018 Dropoff
for i in range(0,len(q)):
    if not q.loc[i,'state']:
        temp = q.loc[i,'election_name'].split(' ')
        q.loc[i,'state'] = temp[0]
q['state'] = q['state'].replace(['Washington','Colorado','Nebraska'], ['WA','CO','NE'])
state_set_18 = set(q['state'].unique())
max_state_set = state_set_20.union(state_set_18)

#Limit campuses to those within our common states
campuses = campuses[campuses['STATE'].isin(max_state_set)]
print('Within State Set # of campuses: {}'.format(len(campuses)))
temp_list = []

#Add Lat/Long and Set CRS
p['Longitude'] = p['geometry'].x
p['Latitude'] = p['geometry'].y
p = p.to_crs(wkt)
q['Longitude'] = q['geometry'].x
q['Latitude'] = q['geometry'].y
q = q.to_crs(wkt)

# Rename, reformat, calculate nearest
def reformat(p,year,max_state_set,campuses):
    p = p[["state", "Latitude", "Longitude", "geometry"]]
    p = p.rename({"state": f"state_{year}"}, axis="columns")
    p = p.rename({"Latitude": f"Latitude_{year}"}, axis="columns")
    p = p.rename({"Longitude": f"Longitude_{year}"}, axis="columns")
    temp = pd.DataFrame()
    for state in max_state_set:
        temp1 = pd.DataFrame()
        temp1 = campuses[campuses['STATE'] == state].sjoin_nearest(p[p[f"state_{year}"] == state], distance_col=f"distances_{year}", how="left")
        #Remove multiple equidistant polling places
        temp1 = temp1.drop_duplicates(subset=['UNIQUEID'], keep='last')
        temp = pd.concat([temp, temp1])
    return temp
p = reformat(p,'Dropoff_2020',max_state_set,campuses)
q = reformat(q,'Dropoff_2018',max_state_set,campuses)

#Set final_df
final_df = p
final_df = final_df.merge(q.iloc[:,[0,-3,-2,-1]],on='UNIQUEID',how='inner')

#Save to file
final_df.to_file(
    "../../20_intermediate_files/31_campuses_w_dist_to_nearest_dropoff.geojson",
    driver="GeoJSON")
final_df.to_csv(
    "../../20_intermediate_files/31_campuses_w_dist_to_nearest_dropoff.csv")