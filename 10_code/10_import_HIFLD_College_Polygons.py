import geopandas as gpd
import pandas as pd

# For cleaning down stream
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
# Load and clean data from HIFLD
############

geo_df = gpd.read_file(
    "../00_source_data/CollegeUniversityCampuses/CollegeUniversityCampuses.shp"
)

# preprocessing the college names
geo_df["preprocessed_name"] = geo_df["NAME"].apply(string_punc)
# print(df['preprocessed_name'])

# Removing things that don't seem to be
# campus itself
geo_df = geo_df[
    ~geo_df["preprocessed_name"].str.contains(
        "hall|beta|phi|gym|laboratory|center|house|program|theater|apartment",
        regex=True,
    )
].copy()  # This would have giving SettingWithCopyWarnings downstream without

#################
# Re-project before spatial manipulations
#################


wkt = """PROJCS["USA_Contiguous_Equidistant_Conic",
        GEOGCS["GCS_North_American_1983",
            DATUM["North_American_Datum_1983",
                SPHEROID["GRS_1980",6378137,298.257222101]],
            PRIMEM["Greenwich",0],
            UNIT["Degree",0.017453292519943295]],
        PROJECTION["Equidistant_Conic"],
        PARAMETER["False_Easting",0],
        PARAMETER["False_Northing",0],
        PARAMETER["Longitude_Of_Center",-96],
        PARAMETER["Standard_Parallel_1",33],
        PARAMETER["Standard_Parallel_2",45],
        PARAMETER["Latitude_Of_Center",39],
        UNIT["Meter",1],
        AUTHORITY["EPSG","102005"]]"""


geo_df = geo_df.to_crs(wkt)

# Extracting the centroid from each college polygon
geo_df["centroid"] = geo_df.centroid

# Save coordinates in floats
geo_df["centroid_x_epsg_102005"] = geo_df["centroid"].x
geo_df["centroid_y_epsg_102005"] = geo_df["centroid"].y

############
# Get centroid in lat-long for Google Maps travel times.
# (Needed projected coordinates to get accurate centroid
# first)
############

# Change which column is active geometry
geo_df = geo_df.set_geometry("centroid")

# Reproject
geo_df = geo_df.to_crs(epsg=4326)

# Extract lat-long
geo_df["centroid_long"] = geo_df["centroid"].x
geo_df["centroid_lat"] = geo_df["centroid"].y

# Back to projected
geo_df = geo_df.to_crs(wkt)

# Back to focus on campus polygons
geo_df = geo_df.set_geometry("geometry")


# Cause geo_df should have only 'geometry' and no other column that represents points
geo_df = geo_df.drop(columns=["centroid"])


geo_df.to_file(
    "../20_intermediate_files/10_HIFLD_campus_polygons.geojson", driver="GeoJSON"
)
geo_df.to_csv("../20_intermediate_files/10_HIFLD_campus_polygons.csv")
