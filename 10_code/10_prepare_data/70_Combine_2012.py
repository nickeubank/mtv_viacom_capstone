import pandas as pd
import geopandas as gpd
import numpy as np

#Combine 21 states w/ Arkansas, WV in csv for geocodio

csv1_states = ['Alaska','Connecticut','Delaware','Illinois','Iowa','Kentucky','Maryland','Michigan',
              'Mississippi','Nebraska','New_Hampshire','New_Jersey','North_Carolina','North_Dakota','Ohio',
             'Oklahoma','Pennsylvania','Rhode_Island','South_Carolina','Virginia','Wisconsin','Arkansas','West_Virginia']
csv1 = []

for state in csv1_states:
    state_df = pd.read_csv(f"../../20_intermediate_files/10_polling_places/2012_Polling_Clean/{state}_2012_clean.csv")
    if (state == 'North_Dakota'): 
        state_df['state'] = 'ND'
    elif (state == 'Nebraska'):
        state_df['state'] = 'NE'
    df = state_df[['state','name','address','clean_address']]
    csv1.append(df)
    
csv1 = pd.concat(csv1, axis=0, ignore_index=True)
csv1.to_csv(f"../../20_intermediate_files/10_polling_places/2012_Polling_Clean/Tier1_2012_clean_23States.csv")

#Combine Massachusetts, Louisiana, Maine, Montana in csv (no zip codes)

csv2_states = ['Louisiana','Maine','Massachusetts','Montana']
csv2 = []

for state in csv2_states:
    state_df = pd.read_csv(f"../../20_intermediate_files/10_polling_places/2012_Polling_Clean/{state}_2012_clean.csv")
    #if (state == 'North_Dakota'): 
    #    state_df['state'] = 'ND'
    #elif (state == 'Nebraska'):
    #    state_df['state'] = 'NE'
    df = state_df[['state','name','address','clean_address']]
    csv2.append(df)
    
csv2 = pd.concat(csv2, axis=0, ignore_index=True)
csv2.to_csv(f"../../20_intermediate_files/10_polling_places/2012_Polling_Clean/Tier2_2012_clean_4States.csv")