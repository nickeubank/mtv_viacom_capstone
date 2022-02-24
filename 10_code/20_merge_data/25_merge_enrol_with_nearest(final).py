

import pandas as pd
import geopandas as gpd

def string_punc(test_str):

    punc = """!()-[]{};:'"\,<>./?@#$%^&*_~"""

    try:

        test_str = str(test_str).lower()
        # print(test_str)
        for ele in test_str:
            if ele in punc:
                test_str = test_str.replace(ele, "")
        processed_lst = []
        for word in test_str.split():
            if word not in ["the", "at", "in", "and", "of"]:
                processed_lst.append(word)

        test_str = " ".join(processed_lst)
        test_str = test_str.replace(" ", "")
        return test_str.lower()
    except:
        return "Null"

        
#nearest_data=pd.read_csv("../../20_intermediate_files/30_campuses_w_dist_to_nearest_pp.csv")


data=pd.read_csv("../../20_intermediate_files/30_campuses_w_dist_to_nearest_pp.csv")
try:
    data=data.drop(columns=['Unnamed: 0','Unnamed: 0.1'])
except:
    data=data

coll_enrol=pd.read_csv("../../20_intermediate_files/17_college_enrollment_data_merge.csv", index_col=None)

coll_enrol['preprocessed_name']=coll_enrol['INSTNM'].apply(string_punc)


merged_data = data.merge(
    coll_enrol,
    left_on = ['preprocessed_name', 'STATE'],
    right_on = ['preprocessed_name', 'STABBR'],
    how="outer",
    indicator=True
)

#If merge was successful, then use the enrollment data from IPEDS, else use the TOT_ENROLL Column
for i,r in merged_data.iterrows():
    if merged_data.loc[i,'_merge']=='both':
        merged_data.loc[i,'Total_Enrollment']=merged_data.loc[i,'EFAGE09']
    else:
        merged_data.loc[i,'Total_Enrollment']=merged_data.loc[i,'TOT_ENROLL']

#Dropping na in UniqueID ()
merged_data=merged_data.dropna(subset=['UNIQUEID'])
merged_data=merged_data.drop(columns=['_merge'])


_=merged_data.to_csv("../../20_intermediate_files/30_campuses_w_dist_to_nearest_pp.csv")