# %% [code] {"execution":{"iopub.status.busy":"2021-08-06T17:10:55.537728Z","iopub.execute_input":"2021-08-06T17:10:55.538127Z","iopub.status.idle":"2021-08-06T17:10:55.554420Z","shell.execute_reply.started":"2021-08-06T17:10:55.538090Z","shell.execute_reply":"2021-08-06T17:10:55.553375Z"}}
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import datetime as dt

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# %% [code] {"execution":{"iopub.status.busy":"2021-08-06T17:10:55.556080Z","iopub.execute_input":"2021-08-06T17:10:55.556483Z","iopub.status.idle":"2021-08-06T17:10:56.955531Z","shell.execute_reply.started":"2021-08-06T17:10:55.556441Z","shell.execute_reply":"2021-08-06T17:10:56.954355Z"}}
data= pd.read_csv('../input/ecommerce-data/data.csv')

data.head()

# %% [markdown]
# ### Cohort Analysis:
# 
# We first divide the entire data into different cohorts to understand high-level trends. We use time cohort for our analysis here:

# %% [code] {"execution":{"iopub.status.busy":"2021-08-06T17:12:39.078193Z","iopub.execute_input":"2021-08-06T17:12:39.078559Z","iopub.status.idle":"2021-08-06T17:12:41.532083Z","shell.execute_reply.started":"2021-08-06T17:12:39.078528Z","shell.execute_reply":"2021-08-06T17:12:41.531231Z"}}
def get_month(x):
    return dt.datetime(x.year, x.month, 1)

data['InvoiceMonth'] = pd.to_datetime(data['InvoiceDate']).to_numpy().astype('datetime64[M]')

data['CohortMonth'] = data.groupby('CustomerID')['InvoiceMonth'].transform('min')
data.head()

# %% [code]
def get_date_int(df, column):    
    year = df[column].dt.year    
    month = df[column].dt.month    
    day = df[column].dt.day
    return year, month, day
