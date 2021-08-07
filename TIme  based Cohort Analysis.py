# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-07T20:53:03.304143Z","iopub.execute_input":"2021-08-07T20:53:03.304519Z","iopub.status.idle":"2021-08-07T20:53:04.102745Z","shell.execute_reply.started":"2021-08-07T20:53:03.304437Z","shell.execute_reply":"2021-08-07T20:53:04.101167Z"}}
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-07T20:53:04.104317Z","iopub.execute_input":"2021-08-07T20:53:04.104678Z","iopub.status.idle":"2021-08-07T20:53:05.382009Z","shell.execute_reply.started":"2021-08-07T20:53:04.104639Z","shell.execute_reply":"2021-08-07T20:53:05.381035Z"}}
data= pd.read_csv('../input/ecommerce-data/data.csv')

data.head()
data.info()

# %% [markdown]
# ### Cohort Analysis:
# 
# We first divide the entire data into different cohorts to understand high-level trends. We use time cohort for our analysis here:

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-07T20:53:05.384186Z","iopub.execute_input":"2021-08-07T20:53:05.384562Z","iopub.status.idle":"2021-08-07T20:53:07.664831Z","shell.execute_reply.started":"2021-08-07T20:53:05.384523Z","shell.execute_reply":"2021-08-07T20:53:07.663659Z"}}
data['InvoiceMonth'] = pd.to_datetime(data['InvoiceDate']).to_numpy().astype('datetime64[M]')

data['CohortMonth'] = data.groupby('CustomerID')['InvoiceMonth'].transform('min')
data.head()

data.dropna(inplace=True)
data.info()

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-07T20:53:07.666433Z","iopub.execute_input":"2021-08-07T20:53:07.666692Z","iopub.status.idle":"2021-08-07T20:53:07.992428Z","shell.execute_reply.started":"2021-08-07T20:53:07.666665Z","shell.execute_reply":"2021-08-07T20:53:07.991451Z"}}
'''def get_date_int(df, column):    
    year = df[column].dt.year    
    month = df[column].dt.month    
    day = df[column].dt.day
    return year, month, day'''
#drop NaN values
data.dropna()

#compute year and month from Invoice Date
invoice_year= data['InvoiceMonth'].dt.year.astype('int')
invoice_mon= data['InvoiceMonth'].dt.month.astype('int')

#compute year and month from Cohort Date
cohort_year= data['CohortMonth'].dt.year.astype('int')
cohort_mon= data['CohortMonth'].dt.month.astype('int')

#find the differences
diff_year = invoice_year - cohort_year
diff_mon = invoice_mon - cohort_mon

#calculate the cohort index for each invoice
data['CohortIndex'] = diff_year * 12 + diff_mon + 1
data.head()

# %% [code] {"execution":{"iopub.status.busy":"2021-08-07T20:56:07.552573Z","iopub.execute_input":"2021-08-07T20:56:07.552971Z","iopub.status.idle":"2021-08-07T20:56:07.644636Z","shell.execute_reply.started":"2021-08-07T20:56:07.552937Z","shell.execute_reply":"2021-08-07T20:56:07.643719Z"}}
#group by cohort month and index and find number of unique customers for each grouping
grouped = data.groupby(['CohortMonth', 'CohortIndex'])['CustomerID'].apply(pd.Series.nunique)\
                                                                    .reset_index()
#pivot the data with cohort month as rows and Cohort Index as columns
grouped = grouped.pivot(index='CohortMonth', columns='CohortIndex',  values='CustomerID')
grouped

# %% [markdown]
# In the table above, the first column values represents the size of every individual cohort, and the subsequent columns represent the number of active customers for that cohort in the subsequent months.

# %% [code] {"execution":{"iopub.status.busy":"2021-08-07T21:21:12.863358Z","iopub.execute_input":"2021-08-07T21:21:12.863821Z","iopub.status.idle":"2021-08-07T21:21:12.894022Z","shell.execute_reply.started":"2021-08-07T21:21:12.863792Z","shell.execute_reply":"2021-08-07T21:21:12.893393Z"}}
#divide each column by value of the first(cohort size) to find retention rate
size = grouped.iloc[:,0]
retention_table = grouped.divide(size, axis=0)

#compute the percentage
retention_table.round(3) * 100

# %% [markdown]
# Let's now visualize the retention rates on a heatmap:

# %% [code] {"execution":{"iopub.status.busy":"2021-08-07T21:34:37.088903Z","iopub.execute_input":"2021-08-07T21:34:37.089364Z","iopub.status.idle":"2021-08-07T21:34:37.802999Z","shell.execute_reply.started":"2021-08-07T21:34:37.089317Z","shell.execute_reply":"2021-08-07T21:34:37.802043Z"}}
plt.figure(figsize=(10, 8))

sns.heatmap(data = retention_table,
            annot = True,        
            fmt = '.0%',         
            vmin = 0.0,          
            vmax = 0.5,           
            cmap = 'BuPu')
plt.show()
