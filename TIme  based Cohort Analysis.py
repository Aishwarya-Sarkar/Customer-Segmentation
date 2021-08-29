import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:05.287766Z","iopub.execute_input":"2021-08-29T19:53:05.288163Z","iopub.status.idle":"2021-08-29T19:53:06.082780Z","shell.execute_reply.started":"2021-08-29T19:53:05.288129Z","shell.execute_reply":"2021-08-29T19:53:06.081735Z"}}
df= pd.read_csv('../input/ecommerce-data/data.csv')

#copy data into new df for analysis
data=df.copy()

data.head()

# %% [code] {"execution":{"iopub.status.busy":"2021-08-29T19:53:06.084437Z","iopub.execute_input":"2021-08-29T19:53:06.084786Z","iopub.status.idle":"2021-08-29T19:53:06.364777Z","shell.execute_reply.started":"2021-08-29T19:53:06.084751Z","shell.execute_reply":"2021-08-29T19:53:06.363723Z"}}
data.info()

# %% [markdown]
# ### 1. Cohort Analysis:
# 
# We first divide the entire data into different cohorts to understand high-level trends. We use time cohort for our analysis here:

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:06.366696Z","iopub.execute_input":"2021-08-29T19:53:06.367033Z","iopub.status.idle":"2021-08-29T19:53:09.173283Z","shell.execute_reply.started":"2021-08-29T19:53:06.367003Z","shell.execute_reply":"2021-08-29T19:53:09.172041Z"}}
#generate invoice month for each line purchase equal to the first day of the month when the purchase was made
data['InvoiceMonth'] = pd.to_datetime(data['InvoiceDate']).to_numpy().astype('datetime64[M]')

#first invoice month for every customer
data['CohortMonth'] = data.groupby('CustomerID')['InvoiceMonth'].transform('min')

#drop null values
data.dropna(inplace=True)

data.head()

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:09.175416Z","iopub.execute_input":"2021-08-29T19:53:09.175931Z","iopub.status.idle":"2021-08-29T19:53:09.603317Z","shell.execute_reply.started":"2021-08-29T19:53:09.175863Z","shell.execute_reply":"2021-08-29T19:53:09.602242Z"}}
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

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:09.605025Z","iopub.execute_input":"2021-08-29T19:53:09.605468Z","iopub.status.idle":"2021-08-29T19:53:09.718958Z","shell.execute_reply.started":"2021-08-29T19:53:09.605422Z","shell.execute_reply":"2021-08-29T19:53:09.717968Z"}}
#group by cohort month and index and find number of unique customers for each grouping
grouped = data.groupby(['CohortMonth', 'CohortIndex'])['CustomerID'].apply(pd.Series.nunique)\
                                                                    .reset_index()
#pivot the data with cohort month as rows and Cohort Index as columns
grouped = grouped.pivot(index='CohortMonth', columns='CohortIndex',  values='CustomerID')
grouped

# %% [markdown]
# In the table above, the first column values represents the size of every individual cohort, and the subsequent columns represent the number of active customers for that cohort in the subsequent months.

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:09.720225Z","iopub.execute_input":"2021-08-29T19:53:09.720545Z","iopub.status.idle":"2021-08-29T19:53:09.766002Z","shell.execute_reply.started":"2021-08-29T19:53:09.720514Z","shell.execute_reply":"2021-08-29T19:53:09.764530Z"}}
#divide each column by value of the first(cohort size) to find retention rate
size = grouped.iloc[:,0]
retention_table = grouped.divide(size, axis=0)

#compute the percentage
retention_table.round(3) * 100

# %% [markdown]
# Let's now visualize the retention rates on a heatmap:

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:09.769513Z","iopub.execute_input":"2021-08-29T19:53:09.769842Z","iopub.status.idle":"2021-08-29T19:53:10.717836Z","shell.execute_reply.started":"2021-08-29T19:53:09.769811Z","shell.execute_reply":"2021-08-29T19:53:10.716747Z"}}
plt.figure(figsize=(10, 8))

sns.heatmap(data = retention_table,
            annot = True,        
            fmt = '.0%',         
            vmin = 0.0,          
            vmax = 0.5,           
            cmap = 'BuPu')
plt.show()

# %% [markdown]
