#  ### 2. RFM Segmentation:
#  RFM segmentation technique takes into account the past purchase behaviour and patterns of the customers to divide them into segments. Here 'R', 'F', 'M' denote Recency, Frequency and Monetary analysis respectively.
#  
# * Recency: Number of days since a customer's last purchase
# * Frequency: Number of purchases by the customer
# * Monetary: Total amount of money spent by the customer on his purchases
#   
# We will be sorting the customers into quartiles based on these three metrics, and calculating their RFM score. With the help of this score, we can effectively sort the customers into segments which can be used for targeting particular segments for campaigns, promotions or other personalized experiences.
#  
# For our ease of analysis, we'll be moving forward with the assumption that the date of our RFM analysis is  just the day after the most recent invoice date in the dataset.

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:10.720212Z","iopub.execute_input":"2021-08-29T19:53:10.720539Z","iopub.status.idle":"2021-08-29T19:53:13.199266Z","shell.execute_reply.started":"2021-08-29T19:53:10.720509Z","shell.execute_reply":"2021-08-29T19:53:13.198237Z"}}
#copy data into a new dataframe for analysis
data_all= df.copy()

#calculating total the total amount for each line item (unit price * Quantity)
data_all['amount']= data_all['Quantity']* data_all['UnitPrice']
data_all.head()

#convert column to datetime
data_all['InvoiceDate']=pd.to_datetime(data_all['InvoiceDate'])

#setting date of analysis= 1 day after the most recent invoice
analysis_date = pd.to_datetime(data_all['InvoiceDate'].max())+ dt.timedelta(days=1)
data_all.head()

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:13.200934Z","iopub.execute_input":"2021-08-29T19:53:13.201212Z","iopub.status.idle":"2021-08-29T19:53:13.762427Z","shell.execute_reply.started":"2021-08-29T19:53:13.201185Z","shell.execute_reply":"2021-08-29T19:53:13.761395Z"}}
#calculate the recency, frequency and Monetary values for each customer
grouped = data_all.groupby(['CustomerID'])\
                .agg({'InvoiceDate': lambda x: (analysis_date - x.max()).days,
                      'InvoiceNo': 'count',
                      'amount': 'sum'})\

#rename each column to denote the R,F,M Values
grouped.rename(columns = {'InvoiceDate': 'R_val',
                                   'InvoiceNo': 'F_val',
                                   'amount': 'M_val'}, inplace=True)
grouped.reset_index().head()

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:13.763906Z","iopub.execute_input":"2021-08-29T19:53:13.764254Z","iopub.status.idle":"2021-08-29T19:53:13.793819Z","shell.execute_reply.started":"2021-08-29T19:53:13.764220Z","shell.execute_reply":"2021-08-29T19:53:13.792776Z"}}
#divide recency metric into 4 quartiles
r_quartiles = pd.qcut(grouped['R_val'], 4, labels = range(4, 0, -1))
grouped = grouped.assign(R_quartile = r_quartiles.values.astype('int'))

#divide frequency metric into 4 quartiles
f_quartiles = pd.qcut(grouped['F_val'], 4, labels = range(1, 5, 1))
grouped = grouped.assign(F_quartile = f_quartiles.values.astype('int'))

#divide monetary metric into 4 quartiles
m_quartiles = pd.qcut(grouped['M_val'], 4, labels = range(1, 5, 1))
grouped = grouped.assign(M_quartile = m_quartiles.values.astype('int'))

grouped.head()
grouped.info()

# %% [markdown]
# Now that we have the R,F,M quartiles, we'll move on to calculating the RFM scores as a sum total of all the three quartiles and assigning RFM segments.

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:13.795164Z","iopub.execute_input":"2021-08-29T19:53:13.795485Z","iopub.status.idle":"2021-08-29T19:53:13.839861Z","shell.execute_reply.started":"2021-08-29T19:53:13.795457Z","shell.execute_reply":"2021-08-29T19:53:13.838475Z"}}
#get RFM segment by concatenation of R,F,M values
grouped['RFM_Seg']=grouped['R_quartile'].astype('str') + grouped['F_quartile'].astype('str') + grouped['M_quartile'].astype('str')

#calculate RFM by summing R,F,M values
grouped['RFM_Score']= grouped[['R_quartile','F_quartile','M_quartile']].sum(axis=1)
grouped.head()

# %% [markdown]
# Visualizing the total count of each RFM Segment:

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-08-29T19:53:13.841726Z","iopub.execute_input":"2021-08-29T19:53:13.842077Z","iopub.status.idle":"2021-08-29T19:53:15.615486Z","shell.execute_reply.started":"2021-08-29T19:53:13.842044Z","shell.execute_reply":"2021-08-29T19:53:15.614544Z"}}
#set sns theme
sns.set_theme(style="whitegrid")

#set plot size
fig, ax = plt.subplots(figsize=(20, 5))

#plot count of each RFM segment
sns.countplot(x="RFM_Seg", data=grouped)
plt.xticks(rotation=45)

plt.show()

# %% [markdown]
# We can clearly see that segment '111'(Worst customers) and segment '444'(best customers) have the highest count.
# 
# Now as per the business requirements, we can analyse each segment. 
# 
# First, we group the customers into different tiers based on their total RFM Score. In decreasing order of their RFM scores, they are as follows:
# 1. Platinum
# 2. Gold
# 3. Advanced
# 4. Basic

# %% [code] {"execution":{"iopub.status.busy":"2021-08-29T19:53:15.616602Z","iopub.execute_input":"2021-08-29T19:53:15.616894Z","iopub.status.idle":"2021-08-29T19:53:15.638798Z","shell.execute_reply.started":"2021-08-29T19:53:15.616851Z","shell.execute_reply":"2021-08-29T19:53:15.637683Z"}}
def get_tier(a):
    if a >9:
        return 'Platinum'
    elif (a>6) & (a<=9):
        return 'Gold'
    elif (a>3) & (a<=6):
        return 'Advanced'
    elif (a>0) & (a<=3):
        return 'Basic' 

#assign a tier to each customer based on the get_tier function logic
grouped['Tier']=grouped['RFM_Score'].apply(get_tier)
grouped.head()

# %% [markdown]
# Next, let us compute the mean of the R-F-M values of each tier and also their counts.

# %% [code] {"execution":{"iopub.status.busy":"2021-08-29T19:53:15.640398Z","iopub.execute_input":"2021-08-29T19:53:15.640856Z","iopub.status.idle":"2021-08-29T19:53:15.669038Z","shell.execute_reply.started":"2021-08-29T19:53:15.640820Z","shell.execute_reply":"2021-08-29T19:53:15.667987Z"}}
df_reset= grouped.reset_index()
tier_analysis=df_reset.groupby(['Tier'])\
        .agg({'R_val': 'mean',
                      'F_val': 'mean',
                      'M_val': 'mean'}).round(2)
print(tier_analysis,'\n')
print(grouped['Tier'].value_counts())

# %% [markdown]
# We can see that the tiers have very distinctive properties, and they can be further analysed as per business needs.
# 
# A few takeaways:
# 
# 1. Tiers with higher Recency values: These are the inactive customers. Surveys should be undertaken to understand their experience and pain-points with the store/app and appropriate measures should be taken in an effort to re-engage them
# 
# 2. Tiers with lower Frequeny Values: These customers should be targeted with additional offers and campaigns from time to time to increase their frequency of purchase
# 
# 3. Tiers with lower Monetary Values: For these customers, marketing and pricing strategies need to be formulated to increase their basket value. This can be achieved by offering discounts on a minimum cart price or bulk purchase discounts

# %% [markdown]
# Now, let's do an analysis of the tiers country-wise. This will help us understand which are the best and worst performing regions.
# 
# We will find out the top 5 countries with the largest percentage of the customers in the Basic Tier and the top 5 countries with the largest percentage of customers in the Platinum Tier.

# %% [code] {"execution":{"iopub.status.busy":"2021-08-29T19:53:15.672596Z","iopub.execute_input":"2021-08-29T19:53:15.672988Z","iopub.status.idle":"2021-08-29T19:53:16.048545Z","shell.execute_reply.started":"2021-08-29T19:53:15.672951Z","shell.execute_reply":"2021-08-29T19:53:16.047396Z"}}
#find total customers in each country
country_count=data_all.groupby(['Country']).size().to_frame('Total_Customers_in_country').reset_index()
country_count.head()

#merge with original df to add the 'Country' column
df_with_country = df_reset.merge(data_all[['CustomerID','Country']], how='inner', on='CustomerID')
result= df_with_country.groupby(['Tier','Country']).size().to_frame('Customer_count').reset_index()
country_data= result.merge(country_count, how='inner', on='Country')

#get filtered dataset for Basic Tier
basic_tier= country_data[country_data['Tier'].isin(['Basic'])]

#calculate percentage of Basic Tier customers in each country
basic_tier['Basic_Tier_Percentage']= ((basic_tier['Customer_count']/basic_tier['Total_Customers_in_country'])*100)\
                                           .round(3)
#display top 5 countries with the largest percentage of Basic Tier Customers
basic_tier[['Country', 'Basic_Tier_Percentage']].sort_values('Basic_Tier_Percentage', ascending=False).head()

# %% [code] {"execution":{"iopub.status.busy":"2021-08-29T19:53:16.049805Z","iopub.execute_input":"2021-08-29T19:53:16.050147Z","iopub.status.idle":"2021-08-29T19:53:16.067039Z","shell.execute_reply.started":"2021-08-29T19:53:16.050116Z","shell.execute_reply":"2021-08-29T19:53:16.065734Z"}}
#get filtered dataset for Platinum Tier
platinum_tier= country_data[country_data['Tier'].isin(['Platinum'])]

#calculate percentage of Platinum Tier customers in each country
platinum_tier['Platinum_Tier_Percentage']= ((platinum_tier['Customer_count']/platinum_tier['Total_Customers_in_country'])*100)\
                                            .round(3)
#display top 5 countries with the largest percentage of Platinum Tier Customers
platinum_tier[['Country','Platinum_Tier_Percentage']].sort_values('Platinum_Tier_Percentage', ascending=False).head()

# %% [markdown]
# From the above analysis, we can Singapore and Iceland have the most active and profitable customer base with 100% of them belonging to the Platinum Tier.
# 
# While, Saudi Arabia does not have any customer outside the Basic Tier.

# %% [markdown]
