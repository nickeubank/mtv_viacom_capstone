import pandas as pd
import geopandas as gpd
import numpy as np

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
        state_df = state_df.drop_duplicates(subset=['name','address','clean_address'], ignore_index=True)
        #Clean Certain Illinois Counties
        if(state == 'Illinois'):
            county_list = ['Alexander','Clay','Ford','Jasper','Jersey','JoDaviess','LaSalle','McDonough','McLean','Ogle','Rock Island']
            special_county = 'Jackson'
            for i in range(0,len(state_df)):
                if state_df.loc[i,'county_name'] in county_list:
                    start_list = state_df.loc[i,'address'].split(sep=",")
                    draft_str2 = ' '.join([str(start_list[i]) for i in range(1,len(start_list) - 3)])
                    new_str = ', '.join([draft_str2, start_list[-3], start_list[-2], start_list[-1]])
                    if (new_str[0] == ','):
                        new_str = new_str[3:]
                    state_df.loc[i,'clean_address'] = new_str
                elif state_df.loc[i,'county_name'] == special_county:
                    start_list = state_df.loc[i,'address'].split(sep=",")
                    draft_str2 = ' '.join([str(start_list[i]) for i in range(2,len(start_list) - 3)])
                    new_str = ', '.join([draft_str2, start_list[-3], start_list[-2], start_list[-1]])
                    state_df.loc[i,'clean_address'] = new_str
                else:
                    state_df.loc[i,'clean_address'] = state_df.loc[i,'address']
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
        state_df = state_df.drop_duplicates(subset=['name','address','clean_address'], ignore_index=True)
        for i in range(0,len(state_df)):
            #Add zip code comma
            start_list = state_df.loc[i,'address'].split()
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
        state_df = state_df.drop_duplicates(subset=['name','address','clean_address'], ignore_index=True)
        for i in range(0,len(state_df)):
            #Add street, state, and zip code commas
            start_list = state_df.loc[i,'address'].split()
            #Catch Arkansas addresses that are short
            if (len(start_list) > 3):
                draft_str2 = ' '.join([str(start_list[i]) for i in range(0,len(start_list) - 3)])
                new_str = ', '.join([draft_str2, start_list[-3], start_list[-2], start_list[-1]])
            else:
                new_str = ', '.join(start_list)
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
        state_df = state_df.drop_duplicates(subset=['name','address','clean_address'], ignore_index=True)
        for i in range(0,len(state_df)):
            #Add state & zip code comma
            start_list = state_df.loc[i,'address'].split()
            draft_str2 = ' '.join([str(start_list[i]) for i in range(0,len(start_list) - 2)])
            new_str = ', '.join([draft_str2, start_list[-2], start_list[-1]])
            state_df.loc[i,'clean_address'] = new_str
        state_df.to_csv(f"../../20_intermediate_files/10_polling_places/2012_Polling_Clean/{state}_2012_clean.csv")
        
def clean_MA():
    #Load state CSV
    state_df = pd.read_csv(f"../../00_source_data/Polling_Data_by_Year_2012/Massachusetts_2012.csv")
    #Add new column
    state_df['clean_address'] = np.nan
    #Remove NA's
    state_df = state_df[state_df['address'].notna()]
    #Remove Duplicates
    state_df = state_df.drop_duplicates(subset=['name','address','clean_address'], ignore_index=True)
    for i in range(0,len(state_df)):
        #Add city and state 
        state_df.loc[i,'clean_address'] = state_df.loc[i,'address'] + ', ' + state_df.loc[i,'jurisdiction'] + ', MA'
    state_df.to_csv(f"../../20_intermediate_files/10_polling_places/2012_Polling_Clean/Massachusetts_2012_clean.csv")

def add_state(state,short_state):
    #Load state CSV
    state_df = pd.read_csv(f"../../00_source_data/Polling_Data_by_Year_2012/{state}_2012.csv")
    #Add new column
    state_df['clean_address'] = np.nan
    #Remove NA's
    state_df = state_df[state_df['address'].notna()]
    #Remove Duplicates
    state_df = state_df.drop_duplicates(subset=['name','address','clean_address'], ignore_index=True)
    for i in range(0,len(state_df)):
        #Add state
        state_df.loc[i,'clean_address'] = state_df.loc[i,'address'] + ', ' + short_state
    state_df.to_csv(f"../../20_intermediate_files/10_polling_places/2012_Polling_Clean/{state}_2012_clean.csv")

#Move 6 Clean States to Clean Folder
clean_states = ['Alaska', 'Connecticut', 'Illinois', 'North_Dakota', 'Ohio', 'Montana']
add_clean(clean_states)

#Clean 9 States By Adding Comma Before Zip Code
zip_code_comma_states = ['Delaware', 'Maryland', 'Mississippi', 'Nebraska', 'North_Carolina', 'Rhode_Island', 'South_Carolina', 'Wisconsin', 'West_Virginia']
add_zip_comma(zip_code_comma_states)

#Clean up Kentucky by removing 'NO VOTER' and 'TO BE DETERMINED' addresses
ky = pd.read_csv('../../00_source_data/Polling_Data_by_Year_2012/Kentucky_2012.csv')
new_ky = ky[ky['address'].str.contains('NO VOTERS')==False]
new_ky = new_ky[new_ky['name'].str.contains('NO VOTERS')==False]
new_ky = new_ky[new_ky['name'].str.contains('TO BE DETERMINED')==False]

#Clean 8 States By Adding All Commas
comma_states = ['Kentucky', 'Michigan', 'New_Hampshire', 'New_Jersey', 'Oklahoma', 'Pennsylvania', 'Virginia', 'Arkansas']
add_all_commas(comma_states)

#Clean 1 State by Adding All but Street Comma
add_all_except_street_commas(['Iowa'])

#Clean 1 State (Massachusetts), by adding city and state
clean_MA()

#Clean 2 States By Adding State
add_state('Louisiana', 'LA')
add_state('Maine', 'ME')

#South Dakota and Vermont are not included here because their polling places did not include addresses