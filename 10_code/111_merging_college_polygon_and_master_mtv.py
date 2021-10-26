import geopandas as gpd
import pandas as pd


def string_punc(test_str):
    
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    try:
        test_str=str(test_str)
        for ele in test_str:
            if ele in punc:
                test_str = test_str.replace(ele, "")

        return test_str.lower()
    except:
        return 'Null'





if __name__=='__main__':
    geo_df = gpd.read_file("../00_source_data/College_Data/College_Polygon.geojson")
    master_df = pd.read_csv("../00_source_data/College_Data/SLSV Master Campus Sheet - Master Sheet.csv", header=1)

    master_df['preprocessed_name'] = master_df['School Name'].apply(string_punc)
    
    
    final_data=master_df.merge(geo_df, left_on='preprocessed_name', right_on='preprocessed_name',how='inner')
    
    print(final_data)
    
    final_data=final_data.drop_duplicates(subset='name',keep='first')
    _=final_data.to_csv("../00_source_data/College_Data/Merged_College_Polygon.csv")