import geopandas as gpd
import pandas as pd

# Little helper function for later



############
# Import pre-cleaned HIFLD polygons
############

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

#import the geo_df and master_df
geo_df = gpd.read_file("../20_intermediate_files/10_HIFLD_campus_polygons.geojson")
master_df = pd.read_csv(
    "./Users/pranavmanjunath/Desktop/Duke/Capstone Project/mtv_viacom_capstone/00_source_data/PlusOne_College_Demographic_Data/SLSV Master Campus Sheet - Master Sheet.csv",
    header=1,
)
print("Original Master:", len(master_df))

#applying the string punctuations
master_df["preprocessed_name"] = master_df["School Name"].apply(string_punc)
geo_df["preprocessed_name"] = geo_df["preprocessed_name"].apply(string_punc)
master_df=master_df.drop_duplicates()
master_df = master_df[
    ~master_df["preprocessed_name"].str.contains(
        "policy|law|phd|graduate|grad|health|medicine|medical"
        "|music|business|nursing|film|art|arts|design|commerce",
        regex=True,
    )
]

#Helping to remove the Many to Many Match
master_df=master_df[master_df['IPED ID']!='Hawaii Community College']
master_df=master_df[master_df['IPED ID']!='485263.00']
master_df=master_df[master_df['IPED ID']!='101949.00']
master_df = master_df[master_df['IPED ID'] != '155636.00']

geo_df = geo_df.loc[~geo_df.duplicated(['preprocessed_name', "STATE"])]

geo_df=geo_df[geo_df['UNIQUEID']!='459082']
geo_df=geo_df[geo_df['UNIQUEID']!='241128']

print("Updated Master:", len(master_df))


print("Length of Master Table:", len(master_df))
merged_data = geo_df.merge(
    master_df,
    left_on = ['preprocessed_name', 'STATE'],
    right_on = ['preprocessed_name', 'State'],
    how="inner",
    indicator=True,
    validate='1:1'
)

# Drop do inner -- do outer, check
# results so you can see what happened,
# then drop
merged_data._merge.value_counts()

final_data = merged_data[merged_data._merge == "both"]

print("Length of Merged Table:", len(final_data))

final_data = final_data.drop_duplicates(subset="NAME", keep="first")

# This you now get as a full dataset (without this run time)
# from your `merged_data._merge == "left"` or `merged_data._merge == "right"`
# results
# not_merged = set(master_df["preprocessed_name"]) - set(final_data["preprocessed_name"])
# not_merged = not_merged.tolist()

not_merged = merged_data[merged_data._merge != "both"]
not_merged = pd.DataFrame(not_merged)
not_merged.to_csv("../20_intermediate_files/15_polygons_not_merged_w_demographics.csv")

print("Length of Merged Table without duplicates:", len(final_data))

final_data = final_data.drop("_merge", axis="columns")
final_data.to_file("../20_intermediate_files/20_campus_polygons_w_demographics.geojson")


