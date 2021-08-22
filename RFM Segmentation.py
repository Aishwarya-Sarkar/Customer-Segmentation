#  ### RFM Segmentation:
#  Here 'R', 'F', 'M' denote Recency, Frequency and Monetary analysis respectively.We will be sorting the customers into quartiles based on these three metrics, and calculating their RFM score. With the help of this score, we can effectively sort the customers into segments.
#  
# For our ease of analysis, we'll be moving forward assuming that the date of our RFM analysis is  just the day after the most recent invoice date in the dataset.

# %% [code] {"execution":{"iopub.status.busy":"2021-08-22T07:55:16.769944Z","iopub.execute_input":"2021-08-22T07:55:16.770245Z","iopub.status.idle":"2021-08-22T07:55:19.251583Z","shell.execute_reply.started":"2021-08-22T07:55:16.770215Z","shell.execute_reply":"2021-08-22T07:55:19.250754Z"}}
data_all= df.copy()

#calculating total the total amount for each line item (unit price * Quantity)
data_all['amount']= data_all['Quantity']* data_all['UnitPrice']
data_all.head()

#convert column to datetime
data_all['InvoiceDate']=pd.to_datetime(data_all['InvoiceDate'])

#setting date of analysis= 1 day after the most recent invoice
analysis_date = pd.to_datetime(data_all['InvoiceDate'].max())+ dt.timedelta(days=1)
data_all.head()

# %% [code] {"execution":{"iopub.status.busy":"2021-08-22T07:55:19.253377Z","iopub.execute_input":"2021-08-22T07:55:19.253659Z","iopub.status.idle":"2021-08-22T07:55:19.825463Z","shell.execute_reply.started":"2021-08-22T07:55:19.253633Z","shell.execute_reply":"2021-08-22T07:55:19.824618Z"}}
#grouped = data_all.groupby(['CustomerID'])['InvoiceDate'].apply(lambda x: (analysis_date - x.max()).days).reset_index()
grouped = data_all.groupby(['CustomerID'])\
                .agg({'InvoiceDate': lambda x: (analysis_date - x.max()).days,
                      'InvoiceNo': 'count',
                      'amount': 'sum'})\
                
grouped.rename(columns = {'InvoiceDate': 'R_val',
                                   'InvoiceNo': 'F_val',
                                   'amount': 'M_val'}, inplace=True)
grouped.head()

# %% [code] {"execution":{"iopub.status.busy":"2021-08-22T07:55:19.826746Z","iopub.execute_input":"2021-08-22T07:55:19.827034Z","iopub.status.idle":"2021-08-22T07:55:19.854320Z","shell.execute_reply.started":"2021-08-22T07:55:19.827007Z","shell.execute_reply":"2021-08-22T07:55:19.853372Z"}}
r_quartiles = pd.qcut(grouped['R_val'], 4, labels = range(4, 0, -1))
grouped = grouped.assign(R_quartile = r_quartiles.values)


f_quartiles = pd.qcut(grouped['F_val'], 4, labels = range(1, 5, 1))
grouped = grouped.assign(F_quartile = f_quartiles.values)

m_quartiles = pd.qcut(grouped['M_val'], 4, labels = range(1, 5, 1))
grouped = grouped.assign(M_quartile = m_quartiles.values)

grouped.head()

# %% [code] {"execution":{"iopub.status.busy":"2021-08-22T07:55:26.001148Z","iopub.execute_input":"2021-08-22T07:55:26.001549Z","iopub.status.idle":"2021-08-22T07:55:26.130174Z","shell.execute_reply.started":"2021-08-22T07:55:26.001508Z","shell.execute_reply":"2021-08-22T07:55:26.129132Z"}}
def get_rfm_score(x):
    return str(x['R_quartile']) + str(x['F_quartile']) + str(x['M_quartile'])
grouped['RFM_Seg']= grouped.apply(get_rfm_score, axis=1)

grouped['RFM_Score']= grouped[['R_quartile','F_quartile','M_quartile']].sum(axis=1)
grouped.head()

# %% [code] {"execution":{"iopub.status.busy":"2021-08-22T07:57:06.440945Z","iopub.execute_input":"2021-08-22T07:57:06.441587Z","iopub.status.idle":"2021-08-22T07:57:08.189393Z","shell.execute_reply.started":"2021-08-22T07:57:06.441546Z","shell.execute_reply":"2021-08-22T07:57:08.188289Z"}}
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(20, 5))
sns.countplot(x="RFM_Seg", data=grouped)
plt.xticks(rotation=45)
plt.show()
