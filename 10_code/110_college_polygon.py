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


def in_us(college_data,us_state):
    ##count=0
    
    for i, r in college_data.iterrows():
        for i1,r1 in us_state.iterrows():
            try:
                if college_data.loc[i,'geometry'].centroid.within(us_state.loc[i1,'geometry']):
                    ##count +=1
                    college_data.loc[i,'State']=us_state.loc[i1,'name']
                    break
            except:
                continue
    
    
    ##print("Count:",count)
    ##print("Pass 5: ",len(college_data))
    
    college_data=college_data.dropna(subset=['State'])
    
    ##print("Pass 6: ",len(college_data))
    return college_data

if __name__ == "__main__":
    
    #merging all the export shape files from overpass turbo
    df=pd.DataFrame(columns=['amenity','name','geometry'])
    for i in range(2,23):
        url= "../00_source_data/College_Polygon-OverPassTurbo/export-"+str(i)+".geojson"
        df1 = gpd.read_file(url)
        df1=pd.DataFrame(df1[['amenity','name','geometry']])
        df=pd.concat([df,df1])

    df=df.drop_duplicates()
    df=df.dropna(subset=['name'])
    ##print("Pass 1:",len(df))
    
    #preprocessing the college names
    df['preprocessed_name'] = df['name'].apply(string_punc)
    df=df[~df['preprocessed_name'].str.contains('hall|beta|phi|gym|laboratory|center|house|program|theater|apartment', regex=True)]
    
    ##print("Pass 2:",len(df))
    
    #Converting into a GeoPandas DataFrame and re-reading the file
    geo_df=gpd.GeoDataFrame(df, geometry=df.geometry)
    _=geo_df.to_file("../00_source_data/College_Data/College_Polygon.geojson", driver='GeoJSON')
    geo_df = gpd.read_file("../00_source_data/College_Data/College_Polygon.geojson")
    
    #Extracting the centroid from each college polygon
    geo_df['centroid']=geo_df.centroid
    geo_df = geo_df.assign(x_centroid = lambda x: (x['centroid'].x))
    geo_df = geo_df.assign(y_centroid = lambda x: (x['centroid'].y))
    geo_df['centroid_geom'] = geo_df['x_centroid'].map(str) + ', ' + geo_df['y_centroid'].map(str)
    
    #Checking if the college exists inside the US
    us_state = gpd.read_file("../00_source_data/College_Polygon-OverPassTurbo/us-state-boundaries.geojson")    

    geo_df=in_us(geo_df,us_state)
    
          
    #Cause geo_df should have only 'geometry' and no other column that represents points
    geo_df=geo_df.drop(columns=['centroid'])
    
    ##print("Pass 7:",len(geo_df))                   
    ##print(geo_df)        
                           
                    
    _=geo_df.to_file("../00_source_data/College_Data/Raw_College_Polygon.geojson", driver='GeoJSON')
    _=geo_df.to_csv("../00_source_data/College_Data/Raw_College_Polygon.csv")