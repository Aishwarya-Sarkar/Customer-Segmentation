#plot the skewness of recency metric
sns.distplot(grouped['R_val'])

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-22T20:59:58.705587Z","iopub.execute_input":"2021-08-22T20:59:58.706139Z","iopub.status.idle":"2021-08-22T20:59:59.011546Z","shell.execute_reply.started":"2021-08-22T20:59:58.706097Z","shell.execute_reply":"2021-08-22T20:59:59.010329Z"}}
#plot the skewness of frequency metric
sns.distplot(grouped['F_val'])

# %% [code] {"execution":{"iopub.status.busy":"2021-08-22T20:59:59.012789Z","iopub.execute_input":"2021-08-22T20:59:59.013091Z","iopub.status.idle":"2021-08-22T20:59:59.338236Z","shell.execute_reply.started":"2021-08-22T20:59:59.013059Z","shell.execute_reply":"2021-08-22T20:59:59.337240Z"}}
#plot the skewness of monetary metric
sns.distplot(grouped['M_val'])

# %% [code] {"execution":{"iopub.status.busy":"2021-08-22T20:59:59.339408Z","iopub.execute_input":"2021-08-22T20:59:59.339669Z","iopub.status.idle":"2021-08-22T20:59:59.591476Z","shell.execute_reply.started":"2021-08-22T20:59:59.339643Z","shell.execute_reply":"2021-08-22T20:59:59.590558Z"}}
recency_log= np.log(grouped['R_val'])
sns.distplot(recency_log)
plt.show()

# %% [code] {"execution":{"iopub.status.busy":"2021-08-22T21:39:13.265863Z","iopub.execute_input":"2021-08-22T21:39:13.266361Z","iopub.status.idle":"2021-08-22T21:39:13.289395Z","shell.execute_reply.started":"2021-08-22T21:39:13.266329Z","shell.execute_reply":"2021-08-22T21:39:13.288467Z"}}
import numpy as np
rfm = grouped[['R_val','F_val','M_val']]
rfm['M_val']=rfm['M_val']+1
rfm_log=np.log(rfm[['R_val','F_val','M_val']])

# Normalize the variables
from sklearn.preprocessing import StandardScaler

ecomm_preprocessed= StandardScaler().fit_transform(rfm_log)
rfm_log[['R_val','F_val','M_val']]=ecomm_preprocessed.round(2)
rfm_log.head()
