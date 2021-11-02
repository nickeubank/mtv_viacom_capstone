import geopandas as gpd
import pandas as pd
import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))


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
        print(test_str)
        return test_str.lower()
    except:
        return 'Null'






if __name__ == "__main__":

    geo_df=gpd.read_file("../00_source_data/CollegeUniversityCampuses/CollegeUniversityCampuses.shp")

    #preprocessing the college names
    geo_df['preprocessed_name'] = geo_df['NAME'].apply(string_punc)
    #print(df['preprocessed_name'])
    geo_df=geo_df[~geo_df['preprocessed_name'].str.contains('hall|beta|phi|gym|laboratory|center|house|program|theater|apartment', regex=True)]


    #Extracting the centroid from each college polygon
    geo_df['centroid']=geo_df.centroid
    geo_df = geo_df.assign(x_centroid = lambda x: (x['centroid'].x))
    geo_df = geo_df.assign(y_centroid = lambda x: (x['centroid'].y))
    geo_df['centroid_geom'] = geo_df['x_centroid'].map(str) + ', ' + geo_df['y_centroid'].map(str)



    #Cause geo_df should have only 'geometry' and no other column that represents points
    geo_df=geo_df.drop(columns=['centroid'])

    ##print("Pass 7:",len(geo_df))
    ##print(geo_df)


    _=geo_df.to_file("../00_source_data/College_Data/Raw_College_Polygon.geojson", driver='GeoJSON')
    _=geo_df.to_csv("../00_source_data/College_Data/Raw_College_Polygon.csv")

