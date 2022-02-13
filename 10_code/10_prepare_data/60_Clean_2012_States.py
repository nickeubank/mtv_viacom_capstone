import pandas as pd
import geopandas as gpd
import numpy as np
from geopy.geocoders import Nominatim

#Clean the 29 states for which we have 2012 data
    
#Define Functions
def add_clean(states):
    for state in states:
        #Load state CSV
        state_df = pd.read_csv(f"../../00_source_data/Polling_Data_by_Year_2012/{state}_2012.csv")
        #Add new column
        state_df['clean_address'] = state_df['address']
        #Remove NA's
        state_df = state_df[state_df['address'].notna()]
        #Remove Duplicates
        state_df = state_df.drop_duplicates(subset=['name','address','clean_address'])
        #Save to New Folder
        state_df.to_csv(f"../../20_intermediate_files/10_polling_places/2012_Polling_Clean/{state}_2012_clean.csv")

def add_zip_comma(states):
    for state in states:
        #Load state CSV
        state_df = pd.read_csv(f"../../00_source_data/Polling_Data_by_Year_2012/{state}_2012.csv")
        #Add new column
        state_df['clean_address'] = np.nan
        #Remove NA's
        state_df = state_df[state_df['address'].notna()]
        #Remove Duplicates
        state_df = state_df.drop_duplicates(subset=['name','address','clean_address'])
        for i in range(0,len(state_df)):
            #Add zip code comma
            start_list = state_df.iloc[i]['address'].split()
            draft_str2 = ' '.join([str(start_list[i]) for i in range(0,len(start_list) - 1)])
            new_str = ', '.join([draft_str2, start_list[-1]])
            state_df.loc[i,'clean_address'] = new_str
        state_df.to_csv(f"../../20_intermediate_files/10_polling_places/2012_Polling_Clean/{state}_2012_clean.csv")
        
def add_all_commas(states):
    for state in states:
        #Special Case for Kentucky
        if(state == 'Kentucky'):
            ky = pd.read_csv('../../00_source_data/Polling_Data_by_Year_2012/Kentucky_2012.csv')
            new_ky = ky[ky['address'].str.contains('NO VOTERS')==False]
            new_ky = new_ky[new_ky['name'].str.contains('NO VOTERS')==False]
            state_df = new_ky[new_ky['name'].str.contains('TO BE DETERMINED')==False]
        #Load state CSV
        else:
            state_df = pd.read_csv(f"../../00_source_data/Polling_Data_by_Year_2012/{state}_2012.csv")
        #Add new column
        state_df['clean_address'] = np.nan
        #Remove NA's
        state_df = state_df[state_df['address'].notna()]
        #Remove Duplicates
        state_df = state_df.drop_duplicates(subset=['name','address','clean_address'])
        for i in range(0,len(state_df)):
            #Add street, state, and zip code commas
            start_list = state_df.iloc[i]['address'].split()
            draft_str2 = ' '.join([str(start_list[i]) for i in range(0,len(start_list) - 3)])
            new_str = ', '.join([draft_str2, start_list[-3], start_list[-2], start_list[-1]])
            state_df.loc[i,'clean_address'] = new_str
        state_df.to_csv(f"../../20_intermediate_files/10_polling_places/2012_Polling_Clean/{state}_2012_clean.csv")
        
def add_all_except_street_commas(states):
    for state in states:
        state_df = pd.read_csv(f"../../00_source_data/Polling_Data_by_Year_2012/{state}_2012.csv")
        #Add new column
        state_df['clean_address'] = np.nan
        #Remove NA's
        state_df = state_df[state_df['address'].notna()]
        #Remove Duplicates
        state_df = state_df.drop_duplicates(subset=['name','address','clean_address'])
        for i in range(0,len(state_df)):
            #Add state & zip code comma
            start_list = state_df.iloc[i]['address'].split()
            draft_str2 = ' '.join([str(start_list[i]) for i in range(0,len(start_list) - 2)])
            new_str = ', '.join([draft_str2, start_list[-2], start_list[-1]])
            state_df.loc[i,'clean_address'] = new_str
        state_df.to_csv(f"../../20_intermediate_files/10_polling_places/2012_Polling_Clean/{state}_2012_clean.csv")
        
#Move 5 Clean States to Clean Folder
clean_states = ['Alaska', 'Connecticut', 'Illinois', 'North_Dakota', 'Ohio']
add_clean(clean_states)

#Clean 8 States By Adding Comma Before Zip Code
zip_code_comma_states = ['Delaware', 'Maryland', 'Mississippi', 'Nebraska', 'North_Carolina', 'Rhode_Island', 'South_Carolina', 'Wisconsin']
add_zip_comma(zip_code_comma_states)

#Clean up Kentucky by removing 'NO VOTER' and 'TO BE DETERMINED' addresses
ky = pd.read_csv('../../00_source_data/Polling_Data_by_Year_2012/Kentucky_2012.csv')
new_ky = ky[ky['address'].str.contains('NO VOTERS')==False]
new_ky = new_ky[new_ky['name'].str.contains('NO VOTERS')==False]
new_ky = new_ky[new_ky['name'].str.contains('TO BE DETERMINED')==False]

#Clean 7 States By Adding All Commas
comma_states = ['Kentucky', 'Michigan', 'New_Hampshire', 'New_Jersey', 'Oklahoma', 'Pennsylvania', 'Virginia']
add_all_commas(comma_states)

#Clean 1 State by Adding All but Street Comma
add_all_except_street_commas(['Iowa'])