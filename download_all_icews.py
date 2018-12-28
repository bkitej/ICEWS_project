#!/usr/bin/env python
# coding: utf-8

# In[122]:


import requests      # all-purpose web scraping package
import re            # finding permalink string from requests.response
import zipfile, io   # stream & unzip
import os            # for making output folder
import pandas as pd  # datetime
from pathlib import Path  # to check if files already downloaded


# In[118]:


# select range of dates to check over
first_icews_date = pd.to_datetime(20181004, format='%Y%m%d')
yesterday = pd.Timestamp.today() - pd.Timedelta('1 days')
all_dates = pd.date_range(first_icews_date, yesterday).strftime('%Y%m%d')


# In[112]:


# create output folder in pwd
output_folder = './icews_files'
try:
    os.mkdir(output_folder)
except FileExistsError:
    pass


# In[129]:


for date in all_dates:
    
    # check if file already downloaded
    file_path = Path(output_folder + '/' + date + '-icews-events.tab')
    if file_path.is_file():
        print(date + ' already downloaded.')
        continue
    
    # url search for date needed
    url = 'https://dataverse.harvard.edu/dataverse/icews?q={}&types=files&sort=score&order=desc'.format(date)
    
    # query url
    response = requests.get(url)
    
    # search for events page link in response text
    ext_raw =         re.search(
            pattern = r'/file.xhtml\?(persistentId=doi\:10.7910/DVN/QI2T9A/[\d\w]{6})',
            string = response.text)
    
    # if it doesn't exist, assume it isn't posted
    if not ext_raw:
        print(date + ' not posted.')
        continue

    # collect download url extension string
    ext = ext_raw.groups(1)[0]
    
    # combine download url
    dl_url = 'https://dataverse.harvard.edu/api/access/datafile/:persistentId?' + ext

    # query download url
    download = requests.get(dl_url)

    # unzip
    try:
        zipfile.ZipFile(
            io.BytesIO(
                download.content)) \
        .extractall(path = output_folder)
    except zipfile.BadZipFile:
        print(date + ' is corrupted.')
    
    # succes status message
    print(date + ' downloaded successfully.')


# In[ ]:




