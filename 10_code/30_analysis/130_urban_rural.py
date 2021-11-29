import pandas as pd
import geopandas as gpd

#Add Urban/Rural Percentages

#Read In Rural/Urban Pct Data
ur = pd.read_excel("../../00_source_data/Urban_Rural_Data/PctUrbanRural_County.xls")

#Remove occurences of duplicate counties
ur = ur.drop(ur[(ur['COUNTY'] == 189) & (ur['COUNTYNAME'] == 'St. Louis')].index)
ur = ur.drop(ur[(ur['COUNTY'] == 5) & (ur['COUNTYNAME'] == 'Baltimore')].index)
ur = ur.drop(ur[(ur['COUNTY'] == 59) & (ur['COUNTYNAME'] == 'Fairfax')].index)
ur = ur.drop(ur[(ur['COUNTY'] == 67) & (ur['COUNTYNAME'] == 'Franklin')].index)

#Remove unnecessary columns
ur = ur[['STATENAME','COUNTYNAME','POPPCT_URBAN','POPPCT_RURAL']]

#Load existing master data file
data=gpd.read_file("../../20_intermediate_files/30_campuses_w_dist_to_nearest_pp.geojson")

#Convert State Abbreviations
states = {'WA': 'WASHINGTON', 'VA': 'VIRGINIA', 'DE': 'DELAWARE', 'DC': 'DISTRICT OF COLUMBIA', 
          'WI': 'WISCONSIN', 'WV': 'WEST VIRGINIA', 'HI': 'HAWAII', 'FL': 'FLORIDA', 
          'FM': 'FEDERATED STATES OF MICRONESIA', 'WY': 'WYOMING', 'NH': 'NEW HAMPSHIRE', 
          'NJ': 'NEW JERSEY', 'NM': 'NEW MEXICO', 'TX': 'TEXAS', 'LA': 'LOUISIANA', 'NC': 'NORTH CAROLINA', 
          'ND': 'NORTH DAKOTA', 'NE': 'NEBRASKA', 'TN': 'TENNESSEE', 'NY': 'NEW YORK', 'PA': 'PENNSYLVANIA', 
          'CA': 'CALIFORNIA', 'NV': 'NEVADA', 'PW': 'PALAU', 'GU': 'GUAM GU', 'CO': 'COLORADO', 
          'VI': 'VIRGIN ISLANDS', 'AK': 'ALASKA', 'AL': 'ALABAMA', 'AS': 'AMERICAN SAMOA', 'AR': 'ARKANSAS',
          'VT': 'VERMONT', 'IL': 'ILLINOIS', 'GA': 'GEORGIA', 'IN': 'INDIANA', 'IA': 'IOWA', 
          'OK': 'OKLAHOMA', 'AZ': 'ARIZONA', 'ID': 'IDAHO', 'CT': 'CONNECTICUT', 'ME': 'MAINE', 
          'MD': 'MARYLAND', 'MA': 'MASSACHUSETTS', 'OH': 'OHIO', 'UT': 'UTAH', 'MO': 'MISSOURI', 
          'MN': 'MINNESOTA', 'MI': 'MICHIGAN', 'MH': 'MARSHALL ISLANDS', 'RI': 'RHODE ISLAND', 
          'KS': 'KANSAS', 'MT': 'MONTANA', 'MP': 'NORTHERN MARIANA ISLANDS', 'MS': 'MISSISSIPPI', 
          'PR': 'PUERTO RICO', 'SC': 'SOUTH CAROLINA', 'KY': 'KENTUCKY', 'OR': 'OREGON', 'SD': 'SOUTH DAKOTA'}
states = {state:abbrev for state, abbrev in states.items()}
data['state_abbrev'] = data['STATE'].map(states)

#Convert State and County to Titles (First letter capital)
data['state_abbrev'] = data['state_abbrev'].apply(lambda x: x.title())
data['COUNTY'] = data['COUNTY'].apply(lambda x: x.title())

#Merge existing data set with urban/rural percentages
final = data.merge(ur, left_on=['COUNTY','state_abbrev'], right_on=['COUNTYNAME','STATENAME'], how='left')

#Save to file
final.to_file(
    "../../20_intermediate_files/30_campuses_w_dist_to_nearest_pp.geojson", driver="GeoJSON")