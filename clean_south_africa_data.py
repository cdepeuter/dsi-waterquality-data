import pandas as pd
import os
import numpy as np

frames = []
for f in os.listdir("processed_data"):
    if f.endswith("_nobor.csv"):
        this_frame = pd.read_csv("processed_data/"+f, parse_dates=["date_time"], na_values='#n/a')
        print(f, this_frame.shape)
        if this_frame.shape[0] > 1000:
            frames.append(this_frame)

all_data=pd.concat(frames)
print("data collected, shape", all_data.shape)
print("columns available", all_data.columns)
# scraping has latitude without its -, fix this
all_data["lat"] = -1*all_data["lat"]
# calcualte hardness and other params
all_data["hardness"] = all_data["Ca_Diss_Water"].astype(float).multiply( 2.497) + all_data["Mg_Diss_Water"].astype(float).multiply(4.188)
all_data["year"] = all_data.date_time.dt.year
all_data["month"] = all_data.date_time.dt.month

# group data by station, year, and month
station_hardness = all_data.groupby(['Station', 'year', 'month']).agg({'lat':{'lat':'mean'}, 'lon':{'lon':'mean'}, 
                                                        'hardness':{'hardness':'mean', 'hardness_max':'max', 'hardness_min':'min'},
                                                        'pH_Diss_Water':{'ph':'mean', 'ph_max':'max', 'ph_min':'min'},
                                                        'K_Diss_Water':{'k':'mean', 'k_max':'max', 'k_min':'min'},
                                                        #'DMS_Tot_Water':{'dms':'mean', 'dms_max':'max', 'dms_min':'min'},
                                                        'EC_Phys_Water':{'ec':'mean', 'ec_max':'max', 'ec_min':'min'},
                                                        'Cl_Diss_Water':{'cl':'mean', 'cl_max':'max','cl_min':'min'},
                                                        'F_Diss_Water':{'f':'mean', 'f_max':'max', 'f_min':'min'},
                                                        'Na_Diss_Water':{'na':'mean', 'na_max':'max', 'na_min':'min'},
                                                        #'P_Tot_Water':{'p':'mean','p_max':'max', 'p_min':'min'},
                                                        'Si_Diss_Water':{'si':'mean', 'si_max':'max', 'si_min':'min'},
                                                        'TAL_Diss_Water':{'tal':'mean', 'tal_max':'max', 'tal_min':'min'},
                                                        'SO4_Diss_Water':{'so':'mean', 'so_max':'max', 'so_min':'min'},
                                                        'NO3_NO2_N_Diss_Water':{'no':'mean', 'no_max':'max', 'no_min':'min'},
                                                        'NH4_N_Diss_Water':{'amn':'mean', 'amn_max':'max', 'amn_min':'min'}
                                                        })
station_hardness['Station'] = station_hardness.index


station_hardness.columns = station_hardness.columns.droplevel()
station_hardness.reset_index(inplace=True) 
print(station_hardness.isnull().sum())
print("shape before drops", station_hardness.shape)
station_hardness.dropna(axis=0, inplace=True)
print("after drops", station_hardness.shape)
# set max values
station_hardness.si.loc[station_hardness.si>20] = 20
station_hardness.no.loc[station_hardness.no>2] = 2
station_hardness.amn.loc[station_hardness.amn>.3] = .3
station_hardness.so.loc[station_hardness.so>300] = 300
station_hardness.tal.loc[station_hardness.tal>400] = 400
station_hardness.na.loc[station_hardness.na>200] = 200
station_hardness.f.loc[station_hardness.f>2] = 2
station_hardness.cl.loc[station_hardness.cl>150] = 150
station_hardness.ec.loc[station_hardness.ec>100] = 100
station_hardness.hardness[station_hardness.hardness > 150] = 150
#station_hardness.dms.loc[station_hardness.dms>1000] = 1000
station_hardness.k.loc[station_hardness.k>10] = 10
# only save data after 2000
filename = "flask-app/data/south_africa_data.csv"
station_hardness[station_hardness.year > 2000].to_csv(filename, index=False)
print("saved data to ", filename, station_hardness.shape)