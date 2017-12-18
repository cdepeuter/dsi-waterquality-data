import json
import pandas as pd
import os
import re
import numpy as np

def ordinal_to_numerical(d):
    ord_map = {'I':1, 'II':2, 'III':3, 'IV':4, 'V':5}
    if d in ord_map:
        return ord_map[d]
    return np.nan

def week_to_month(w):
    w = int(w / 4) + 1
    if w > 12:
        w = 12
    return w

def update_columns(cols, data_type):
    final_cols = []
    for c in cols:
        if c == "0":
            final_cols.append("Station")
        else:
            final_cols.append(data_type+"_week_"+c)
    return final_cols

gem = pd.read_csv("china_data/china_gem_data/china_gem_data.csv")
gem.columns = ['Station', 'lon', 'lat', 'Basin']

data_root = "china_data/china_param_data/2016/"
data_2016_files = [f for f in os.listdir(data_root)]


this_frame = None
for f in data_2016_files:
    print(f)
#f = data_2016_files[0]
    data_type = f.replace(".csv","").lower()
    if this_frame is None:
        this_frame = pd.read_csv(data_root + f, encoding='utf-8')
        this_frame = pd.melt(this_frame, id_vars=['0'])
        this_frame.columns = ['Station', 'week', data_type]
        #this_frame.columns = update_columns(this_frame.columns, data_type)
    else:
        new_frame = pd.read_csv(data_root + f, encoding='iso-8859-1')
        new_frame = pd.melt(new_frame, id_vars=['0'])
        new_frame.columns = ['Station', 'week', data_type]
        this_frame = this_frame.merge(new_frame, on=['Station', 'week'])
        
this_frame["year"] = 2016
this_frame_2016 = this_frame
print("2016 shape", this_frame.shape)

data_root = "china_data/china_param_data/2017/"
data_2017_files = [f for f in os.listdir(data_root)]

this_frame = None
for f in data_2017_files:
    print(f)
#f = data_2016_files[0]
    data_type = f.replace(".csv","").lower()
    if this_frame is None:
        this_frame = pd.read_csv(data_root + f, encoding='utf-8')
        this_frame = pd.melt(this_frame, id_vars=['0'])
        this_frame.columns = ['Station', 'week', data_type]
        #this_frame.columns = update_columns(this_frame.columns, data_type)
    else:
        new_frame = pd.read_csv(data_root + f, encoding='iso-8859-1')
        new_frame = pd.melt(new_frame, id_vars=['0'])
        new_frame.columns = ['Station', 'week', data_type]
        this_frame = this_frame.merge(new_frame, on=['Station', 'week'])


this_frame["year"] = 2017

this_frame = pd.concat([this_frame_2016, this_frame])
this_frame.week_eval = this_frame.week_eval.map(ordinal_to_numerical)

this_frame["month"] = this_frame.week.astype(int).map(week_to_month)
this_frame = this_frame.merge(gem, on='Station')

this_frame["nh3"] = pd.to_numeric(this_frame.nh3, errors='coerce')
this_frame["cod"] = pd.to_numeric(this_frame.cod, errors='coerce')
this_frame["do"] = pd.to_numeric(this_frame.do, errors='coerce')
this_frame["ph"] = pd.to_numeric(this_frame.ph, errors='coerce')

this_frame.dropna(subset=['ph','cod', 'do', 'nh3','week_eval', 'lat', 'lon'], inplace=True)


this_frame.rename(columns={'week_eval':'quality'}, inplace=True)
this_frame.rename(columns={'nh3':'nh'}, inplace=True)

# group by station/year/month, aggregate to get mean min and max
china_data = this_frame.groupby(['Station', 'year', 'month']).agg({'lat':{'lat':'mean'}, 'lon':{'lon':'mean'}, 
                                                            'quality':{'quality':'mean', 'quality_max':'max', 'quality_min':'min'},
                                                        'ph':{'ph':'mean', 'ph_max':'max', 'ph_min':'min'},
                                                            'cod':{'cod':'mean', 'cod_max':'max', 'cod_min':'min'},
                                                                  'do':{'do':'mean', 'do_max':'max', 'do_min':'min'},
                                                                  'nh':{'nh':'mean', 'nh_max':'max', 'nh_min':'min'}})
china_data['Station'] = china_data.index

# set maximum values
china_data.columns = china_data.columns.droplevel()
china_data.reset_index(inplace=True) 
china_data.do[china_data.do > 15] = 15
china_data.cod[china_data.cod > 10] = 10
china_data.nh[china_data.nh > 3] = 3
print("china columns", china_data.columns)
china_data.to_csv("flask-app/data/merged_china_data.csv")
print("done with china data", china_data.shape)