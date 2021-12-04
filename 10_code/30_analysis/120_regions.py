import pandas as pd
import geopandas as gpd

#State - Region

states = {
    'AK': 'O',
    'AL': 'S',
    'AR': 'S',
    'AS': 'O',
    'AZ': 'W',
    'CA': 'W',
    'CO': 'W',
    'CT': 'N',
    'DC': 'N',
    'DE': 'N',
    'FL': 'S',
    'GA': 'S',
    'GU': 'O',
    'HI': 'O',
    'IA': 'M',
    'ID': 'W',
    'IL': 'M',
    'IN': 'M',
    'KS': 'M',
    'KY': 'S',
    'LA': 'S',
    'MA': 'N',
    'MD': 'N',
    'ME': 'N',
    'MI': 'W',
    'MN': 'M',
    'MO': 'M',
    'MP': 'O',
    'MS': 'S',
    'MT': 'W',
    'NA': 'O',
    'NC': 'S',
    'ND': 'M',
    'NE': 'W',
    'NH': 'N',
    'NJ': 'N',
    'NM': 'W',
    'NV': 'W',
    'NY': 'N',
    'OH': 'M',
    'OK': 'S',
    'OR': 'W',
    'PA': 'N',
    'PR': 'O',
    'RI': 'N',
    'SC': 'S',
    'SD': 'M',
    'TN': 'S',
    'TX': 'S',
    'UT': 'W',
    'VA': 'S',
    'VI': 'O',
    'VT': 'N',
    'WA': 'W',
    'WI': 'M',
    'WV': 'S',
    'WY': 'W',
    'FM': 'O',
    'PW': 'O'
}

regions={
    'N':'North East',
    'W':'West',
    'M': 'Mid West',
    'S': 'South',
    'O': 'Other'
}


data=gpd.read_file("../../20_intermediate_files/30_campuses_w_dist_to_nearest_pp.geojson")

data.loc[(data.STATE == 'NJ '),'STATE']='NJ'
data.loc[(data.STATE == 'OH '),'STATE']='OH'


data['Region'] = data['STATE'].apply(lambda x: states[x])

data['Region'] = data['Region'].apply(lambda x: regions[x])

data = data[data['Region'] != 'Other']
data.to_file(
    "../../20_intermediate_files/30_campuses_w_dist_to_nearest_pp.geojson", driver="GeoJSON"
)