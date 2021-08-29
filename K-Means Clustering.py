# ### 3. K-Means Clustering:
# 
# Now, we will be approaching the segmentation using K-Means Clustering, a popular unsupervised learning algorithm. But before we start, we need to process the data to adhere to the following assumptions of K-Means Clustering with the techiques mentioned below:
# 
# 1. K-Means assumes that the variables are not skewed. We will test our R,F,M values. If they are skewed, we will use logarithmic transformation to eliminate the skewness
# 
# 2. K-Means assumes that all the variables have a similar mean and variance. Therefore, we will check the range and mean of each of the variables and if they are dissimilar, we will be using the Standard Scalar to normalize them

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:16.068949Z","iopub.execute_input":"2021-08-29T19:53:16.069429Z","iopub.status.idle":"2021-08-29T19:53:16.410783Z","shell.execute_reply.started":"2021-08-29T19:53:16.069381Z","shell.execute_reply":"2021-08-29T19:53:16.409716Z"}}
#plot the skewness of recency metric
sns.distplot(grouped['R_val'])

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:16.412543Z","iopub.execute_input":"2021-08-29T19:53:16.412990Z","iopub.status.idle":"2021-08-29T19:53:16.793030Z","shell.execute_reply.started":"2021-08-29T19:53:16.412944Z","shell.execute_reply":"2021-08-29T19:53:16.791841Z"}}
#plot the skewness of frequency metric
sns.distplot(grouped['F_val'])

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:16.794303Z","iopub.execute_input":"2021-08-29T19:53:16.794639Z","iopub.status.idle":"2021-08-29T19:53:17.258853Z","shell.execute_reply.started":"2021-08-29T19:53:16.794606Z","shell.execute_reply":"2021-08-29T19:53:17.258017Z"}}
#plot the skewness of monetary metric
fig, ax = plt.subplots(figsize=(13, 7))
sns.distplot(grouped['M_val'])

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:17.260162Z","iopub.execute_input":"2021-08-29T19:53:17.260450Z","iopub.status.idle":"2021-08-29T19:53:17.577709Z","shell.execute_reply.started":"2021-08-29T19:53:17.260413Z","shell.execute_reply":"2021-08-29T19:53:17.576684Z"}}
#log transformation of recency metric
recency_log= np.log(grouped['R_val'])

#plot the transformed variable
sns.distplot(recency_log)
plt.show()

# %% [code] {"execution":{"iopub.status.busy":"2021-08-29T19:53:17.579313Z","iopub.execute_input":"2021-08-29T19:53:17.579722Z","iopub.status.idle":"2021-08-29T19:53:17.619112Z","shell.execute_reply.started":"2021-08-29T19:53:17.579680Z","shell.execute_reply":"2021-08-29T19:53:17.618044Z"}}
#check for variance and mean of the variables
grouped.describe()

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:17.620959Z","iopub.execute_input":"2021-08-29T19:53:17.621390Z","iopub.status.idle":"2021-08-29T19:53:17.649288Z","shell.execute_reply.started":"2021-08-29T19:53:17.621336Z","shell.execute_reply":"2021-08-29T19:53:17.648123Z"}}
rfm = grouped[['R_val','F_val','M_val']]

#making all values in M_val positive
rfm['M_val']=rfm['M_val']+1

#applying logarithmic transformation
for c in ['R_val', 'F_val']:
    rfm[c]= np.log(rfm[c])
    

#Normalization of variables
from sklearn.preprocessing import StandardScaler

ecomm_standardized= StandardScaler().fit_transform(rfm)
rfm[['R_val','F_val','M_val']]=ecomm_standardized.round(2)

rfm.head()

# %% [markdown]
# The above step concludes the pre-processig of the data. Now, we use the elbow criterion method to find the optinum number of clusters.

# %% [code] {"execution":{"iopub.status.busy":"2021-08-29T19:53:17.652603Z","iopub.execute_input":"2021-08-29T19:53:17.652972Z","iopub.status.idle":"2021-08-29T19:53:32.509359Z","shell.execute_reply.started":"2021-08-29T19:53:17.652935Z","shell.execute_reply":"2021-08-29T19:53:32.508519Z"}}
#start k-means clusterig
from sklearn.cluster import KMeans

sse = {}

#find the optimum number of clusters from 1 to 10
for k in range(1, 11):    
    kmeans = KMeans(n_clusters=k, random_state=1)    
    kmeans.fit(rfm)    
    sse[k] = kmeans.inertia_ 
    
# Plot SSE for each value of k    
plt.title('The Elbow Method')
plt.xlabel('k'); 
plt.ylabel('SSE')
sns.pointplot(x=list(sse.keys()), y=list(sse.values()))
plt.show()

# %% [code] {"execution":{"iopub.status.busy":"2021-08-29T19:53:32.510590Z","iopub.execute_input":"2021-08-29T19:53:32.511071Z","iopub.status.idle":"2021-08-29T19:53:33.851325Z","shell.execute_reply.started":"2021-08-29T19:53:32.511024Z","shell.execute_reply":"2021-08-29T19:53:33.850261Z"}}
#fit k-means with 3 clusters
kmeans = KMeans(n_clusters=3, random_state=1)    
kmeans.fit(rfm)

#adding column with cluster labels to a new df
cluster_table = grouped.assign(Cluster=kmeans.labels_)

#group by cluster
clustered_data = cluster_table.groupby(['Cluster'])

#average RFM values for each cluster
clustered_data.agg({
    'R_val': 'mean',
    'F_val': 'mean',
    'M_val': 'mean'
  }).round(2)
