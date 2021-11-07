import geopandas as gpd
import pandas as pd

# Little helper function for later


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


############
# Import pre-cleaned HIFLD polygons
############

geo_df = gpd.read_file("../20_intermediate_files/10_HIFLD_campus_polygons.geojson")
master_df = pd.read_csv(
    "../00_source_data/College_Data/SLSV Master Campus Sheet - Master Sheet.csv",
    header=1,
)
print("Original Master:", len(master_df))

master_df["preprocessed_name"] = master_df["School Name"].apply(string_punc)
geo_df["preprocessed_name"] = geo_df["preprocessed_name"].apply(string_punc)

master_df = master_df[
    ~master_df["preprocessed_name"].str.contains(
        "policy|law|phd|graduate|grad|health|medicine|medical"
        "|music|business|nursing|film|art|arts|design|commerce",
        regex=True,
    )
]

#
#
# THIS IS A MANY-TO-MANY MERGE! THOSE ARE TROUBLE!
# Use the `validate` keyword to check your merge assumptions
#
# Also if you use the geopandas dataframe up front,
# geospatial data is preserved.
#

print("Length of Master Table:", len(master_df))
merged_data = geo_df.merge(
    master_df,
    on="preprocessed_name",
    how="outer",
    indicator=True,
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
