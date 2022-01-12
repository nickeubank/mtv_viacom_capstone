
import pandas as pd


#HD2020 Table
college_name=pd.read_csv("../../00_source_data/college_enrollment_data/college_name.csv")

#EF2020B Table
'''
Data Dictionary:
EFPAGE01: Full time men
EFAGE02: Full time women
EFAGE03: Part time men
EFAGE04: Part time women
EFAGE05: Full time total
EFAGE06: Part time total
EFAGE07: Total men
EFAGE08: Total women
EFAGE09: Grand total
'''
enrollment_data=pd.read_csv("../../00_source_data/college_enrollment_data/enrollment_data.csv")

'''
In the enrollment_data, there are multiple rows for each college and hence when LINE=412, 
the total enrollment is correct. Verified with manually searching total student population of colleges on college websites and the values present in the column EFAGE09.

'''
enrollment_data=enrollment_data[enrollment_data['LINE']==412]


#Merged the Data on the UNITID Column
data=college_name.merge(enrollment_data, on='UNITID')

#Saving it into the 20_intermediate_files folder
_=data.to_csv("../../20_intermediate_files/college_enrollment_data_merge.csv")