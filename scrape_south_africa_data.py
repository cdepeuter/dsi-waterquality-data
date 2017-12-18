import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
import zipfile
import os
import re

def get_info_from_row(r):
    """ 
        For a table row, scrape data
    """
    cells = r.select("td")   
    # we want this data point if theres a zip, save all the info
    # including lat, long, type, 
    if len(cells) > 10 and cells[2].select("a"):
        id_ =  re.sub("[^\w\. ]", "",cells[0].text)
        data_anchor = cells[2].select("a")[0]
        href = data_anchor["href"]
        desc = cells[3].text
        type_ = cells[4].text
        med_ec = cells[8].text
        flow = re.sub("[^\w\.]", "",cells[9].text)
        lat = re.sub("[^\w\.]", "",cells[10].text)
        lon = re.sub("[^\w\.]", "",cells[11].text)
        
        return {"id":id_, "desc":desc, "type":type_, "med_ec":med_ec, "flow":flow, "lat":lat, "lon":lon, "href":href}



def fetch_save_data_for_region(reg_url):
    """
        For a given region, collect metatdata, download all files
        With the downloaded files, unzip them and combine with their metadata
    """
    # get region page
    region_page = requests.get(reg_url)
    region_name = reg_url.split("/")[-1].split(".")[0]
    region_dir = "data/" + region_name
    # store the data files
    if not os.path.exists(region_dir):
        os.makedirs(region_dir)
                    
    print("starting process for", reg_url)
            
    soup = BeautifulSoup(region_page.text, "html.parser")
    # create metadata array
    rows = soup.select("table#hor-minimalist-b tr")
    metadata_array = [get_info_from_row(rows[i]) for i in range(1, len(rows))]
    metadata_array = [m for m in metadata_array if m is not None]
    metadata_lookup = {m["id"]:m for m in metadata_array if m is not None}
    
    data_urls = [m["href"] for m in metadata_array]
    for d in data_urls:
        download_file(d, region_dir+"/")
    print("len data urls:", len(data_urls))

    # unzip all the files
    unzip_dir = os.getcwd() + "/" + region_dir
    for item in os.listdir(unzip_dir): # loop through items in dir
        if item.endswith(".zip"): # check for ".zip" extension
            file_name = unzip_dir + "/" + item # get full path of files
            #print(file_name)
            try:
                zip_ref = zipfile.ZipFile(file_name) # create zipfile object
                zip_ref.extractall(unzip_dir) # extract file to dir
            except:
                print("unzip, error with file", file_name)
            zip_ref.close() # close file
    
    
    # load dataframes individually, concat, save
    data_files = [f for f in os.listdir(region_dir) if f.endswith(".csv")]
    print("len data files", len(data_files))

    data_frames = []
    for d in data_files:
        try:
            new_frame = pd.read_csv(region_dir + "/" + d) 
            id_ = d.replace(".csv", " ").replace("_", " ").strip()
            metadata = metadata_lookup[id_]
            new_frame["desc"] = metadata["desc"]
            new_frame["type"] = metadata["type"]
            new_frame["med_ec"] = metadata["med_ec"]
            new_frame["flow"] = metadata["flow"]
            new_frame["lat"] = metadata["lat"]
            new_frame["lon"] = metadata["lon"]
            
            data_frames.append(new_frame)     
        except:
            print("load csv, error with file", d)
    data = pd.concat(data_frames)
    print("data shape", data.shape)
    data.to_csv("processed_data/" + region_name +".csv", index=False)

def download_file(url, path):
    """
        Download and save a zip file from the inputted URL
    """
    file_name = path + url.split("/")[-1]
    req = requests.get(url)
    zipped_info = req.content
    print(file_name)
    if not os.path.isfile(file_name):
        print("file doesnt exist, writing", file_name)
        with open(file_name, 'wb') as f:
            f.write(zipped_info)
    else:
        print("file exists", file_name)




region_page = requests.get("http://www.dwa.gov.za/iwqs/wms/data/A_reg_WMS_nobor.htm")
soup = BeautifulSoup(region_page.text, "html.parser")
rows = soup.select("table#hor-minimalist-b tr")
metadata_array = [get_info_from_row(rows[i]) for i in range(1, len(rows))]
metadata_lookup = {m["id"]:m for m in metadata_array if m is not None}

# get all region links
sa_page = requests.get("http://www.dwa.gov.za/iwqs/wms/data/WMS_pri_txt.asp")
soup = BeautifulSoup(sa_page.text, "html.parser")
all_links = soup.find_all('a', href=True)


domain = "http://www.dwa.gov.za/iwqs/wms/data/"
region_links = [domain + a["href"] for a in all_links if a["href"].endswith("_nobor.htm")]

# for each region scrape and save data
for r in region_links:
    fetch_save_data_for_region(r)

print("done scraping south africa data")
