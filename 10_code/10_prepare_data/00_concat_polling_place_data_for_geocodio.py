import pandas as pd
import glob
import re

# folder that contains polling place data for each year
path = r'/Users/dapoadegbile/Documents/Capstone /Polling Data by Year 2018' # use your path
all_files = glob.glob(path + "/*.csv")

li = []
# add official state name to each filename
# Get street address and state for geocoding
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    state_full = str.split(filename, '/')[-1][:-9]
    df['state_full'] = state_full.replace('_', ' ')
    df = df[['address', 'state_full']]
    li.append(df)

frame2018 = pd.concat(li, axis=0, ignore_index=True)

# convert to CSV and Excel Sheet
pp_df2018 = frame2018.to_csv(r'/Users/dapoadegbile/Documents/Capstone /pp_df2018', index=False)
frame2018.to_excel("pp_df2018.xlsx", index = False)


# Same Exact same process for 2016
path = r'/Users/dapoadegbile/Documents/Capstone /Polling Data by Year 2016' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    state_full = str.split(filename, '/')[-1][:-9]
    df['state_full'] = state_full.replace('_', ' ')
    df = df[['address', 'state_full']]
    li.append(df)

frame2016 = pd.concat(li, axis=0, ignore_index=True)

pp_df2016 = frame2016.to_csv('pp_df2016', index=False)
frame2016.to_excel("pp_df2016.xlsx", index = False)



path = r'/Users/dapoadegbile/Documents/Capstone /Polling Data by Year 2012' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    state_full = str.split(filename, '/')[-1][:-9]
    df['state_full'] = state_full.replace('_', ' ')
    df = df[['address', 'state_full']]
    li.append(df)

frame2012 = pd.concat(li, axis=0, ignore_index=True)

pp_df2012 = frame2012.to_csv('pp_df2012', index=False)
frame2012.to_excel("pp_df2012.xlsx", index = False)
