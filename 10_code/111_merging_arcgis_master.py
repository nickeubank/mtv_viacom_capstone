import geopandas as gpd
import pandas as pd


def string_punc(test_str):

    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    try:

        test_str=str(test_str).lower()
        #print(test_str)
        for ele in test_str:
            if ele in punc:
                test_str = test_str.replace(ele, "")
        processed_lst=[]
        for word in test_str.split():
            if word not in ['the','at','in','and','of']:
                processed_lst.append(word)


        test_str=' '.join(processed_lst)
        test_str = test_str.replace(" ", "")
        return test_str.lower()
    except:
        return 'Null'








if __name__=='__main__':
    geo_df = gpd.read_file("../00_source_data/College_Data/Raw_College_Polygon.geojson")
    master_df = pd.read_csv("../00_source_data/College_Data/SLSV Master Campus Sheet - Master Sheet.csv", header=1)
    print("Original Master:",len(master_df))
    master_df['preprocessed_name'] = master_df['School Name'].apply(string_punc)
    geo_df['preprocessed_name'] = geo_df['preprocessed_name'].apply(string_punc)
    master_df=master_df[~master_df['preprocessed_name'].str.contains('policy|law|phd|graduate|grad|health|medicine|medical|music|business|nursing|film|art|arts|design|commerce', regex=True)]



    print("Length of Master Table:",len(master_df))
    final_data=master_df.merge(geo_df, left_on='preprocessed_name', right_on='preprocessed_name',how='inner')

    #print(final_data)

    print("Length of Merged Table:",len(final_data))

    final_data=final_data.drop_duplicates(subset='NAME',keep='first')

    not_merged = set(master_df['preprocessed_name']) - set(final_data['preprocessed_name'])
    # not_merged = not_merged.tolist()
    textfile = open("../20_intermediate_files/not_merged.txt", "w")
    for element in not_merged:
        textfile.write(element + "\n")
    textfile.close()



    print("Length of Merged Table without duplicates:",len(final_data))
    _=final_data.to_csv("../00_source_data/College_Data/Merged_College_Polygon.csv")
