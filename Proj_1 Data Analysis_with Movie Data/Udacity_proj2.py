#!/usr/bin/env python
# coding: utf-8

# In[20]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.

# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns       
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# Investigating the shape of Data.

# In[21]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df = pd.read_csv('tmdb-movies.csv')
df.head


# In[22]:


df.info()


# In[23]:


# to check the number of rows and coloumn
df.tail()


# In[24]:


# statistic values for this data 
df.describe()


# In[25]:


# check the rows and columns of this dataset
df.shape


# In[26]:


# check each columns number of unique values 
df.nunique()


# In[27]:


df.isnull().sum()


# Data cleaning process by filling null values with mean and also drop duplicate data

# In[28]:


# drop unuseful columns 
df.drop(['id','imdb_id', 'homepage','overview'],axis=1,inplace=True)  # do not forget inplace 

df.fillna(df.mean(), inplace = True)
df.info()


# In[29]:


# calculate sum of null value for each coloumn
df.isnull().sum()


# In[30]:


# Drop null values for each coloumn containing null values
df.dropna(inplace = True)
df.info()


# In[31]:


# to replace all the zero value in coloumn with mean value.
df['popularity']=df['popularity'].replace(0,df['popularity'].mean())
df['revenue']=df['revenue'].replace(0,df['revenue'].mean())
df['runtime']=df['runtime'].replace(0,df['runtime'].mean())
df['budget_adj']=df['budget_adj'].replace(0,df['budget_adj'].mean())
df['revenue_adj']=df['revenue_adj'].replace(0,df['revenue_adj'].mean())


# In[32]:


df.describe()


# In[33]:


# calculate sum of all duplicated value
df.duplicated().sum()


# In[34]:


# Drop duplicate value
df.drop_duplicates(inplace=True)


# In[35]:


# calculate sum of all duplicated value
df.duplicated().sum()


# In[36]:


# visulize each variables 
df.hist(figsize=(18,18));


# Exploration with Visuals and Conclusions
# 
# The questions about this dataset:
# 
# 1) Does higher budget mean higher popularity ?
# 
# 2) Do the runtime affect the vote count and popularity?
# 
# 3) Is Higher popularity means higher profits ?
# 
# 4) What are the Features Associate with Top 10 Revenue Movies ?

# _______________________________________________________________________________________________
# EVALUATING QUESTION 1
# 
# 1) Does higher budget mean higher popularity ?

# In[37]:


# plot the relation between budget and popularity 
x = df['budget']
y = df['popularity'] 

plt.scatter(x,y)
plt.title('Average Popularity by Different budget',fontsize=20)
plt.xlabel('budgete',fontsize=20)
plt.ylabel('popularity',fontsize=20)


# As per the above scatter plot its very difficult to observe strong relationship between popularity and budget. So we use other 
# method to observe the relationship between them. In this method we divide data set in to two group on the basis of median.

# In[38]:


# divide the budget into two groups : lesser_cost and more_cost.
med = df['budget'].median()
lesser_cost =  df.query('budget < {}'.format(med))
more_cost =  df.query('budget >= {}'.format(med))


# In[39]:


# check lesser cost and more cost  mean values 
mean_low_budget = lesser_cost['popularity'].mean()
mean_high_budget = more_cost['popularity'].mean()


# In[40]:


# create a bar chart with the values we get above 
locations = [1,2]
heights = [mean_low_budget , mean_high_budget]
labels=['low','high']
plt.bar(locations, heights, tick_label = labels)
plt.title('Mean Popularity by all Budget')
plt.xlabel('Budgets')
plt.ylabel('Mean Popularity')


# In[41]:


increase_percentage = (mean_high_budget - mean_low_budget) / mean_high_budget * 100
increase_percentage


# Answer for question 1
# 
# From the above bar plot we conclude that higher budget movie gains higher popularity. Higher budget movie have Mean popularity more than twice than the Mean popularity of lower budget movie.

# EVALUATING QUESTION 2
# 
# 2) Do the runtime affect the vote count and popularity?
# 
# 

# In[42]:


# There 3 groups with query().  <60 min: lowest   , 60 min <=  <= - 120 min: medium ,  >120 min: highest
lowest =  df.query('runtime < {}'.format(100))
med =  df.query('runtime < {}'.format(200))
highest = df.query('runtime > {}'.format(200))


# In[43]:


# check mean popularity of different movie lengths 
mean_of_lowest = lowest['popularity'].mean()
mean_of_med = med['popularity'].mean()
mean_of_highest = highest['popularity'].mean()


# In[44]:


locations = [1,2,3]
heights = [mean_of_lowest, mean_of_med, mean_of_highest]
labels=['low','medium','high']
plt.bar(locations, heights, tick_label = labels)
plt.title('Average Popularity by Different Runtime')
plt.xlabel('Runtime')
plt.ylabel('Average Popularity')


# In[45]:


# scatter plot between runtime and popularity 
x = df['runtime']
y = df['popularity'] 

plt.scatter(x,y)

plt.title('Average Popularity by Different Runtime',fontsize=20)
plt.xlabel('runtime',fontsize=20)
plt.ylabel('popularity',fontsize=20)


# ANSWER FOR QUESTION 2
# 
# From the above two plots, we can simply say that 
# If the movies are within 200 minutes,it will be more popular. 
# Once the movies run over 200 minutes, it's hard for them to gain high popularity

# EVALUATING QUESTION 3
# 
# 3) Is Higher popularity means higher profits ?
# 
# 

# In[49]:


# calculation for the mean of popularity 
mean = df['popularity'].median()
lowest_popularity =  df.query('popularity < {}'.format(mean))
more_popularity =  df.query('popularity >= {}'.format(mean))


# In[50]:


# create a new column called profit.
df['profit'] = df['revenue'] - df['budget']


# In[51]:


# average net profit for low_popularity and high_popularity
mean_profit_of_low = lowest_popularity['profit'].mean()
mean_profit_of_high = more_popularity['profit'].mean()
df.head()


# In[52]:


# create a bar chart with the values we get above 
locations = [1,2]
heights = [mean_profit_of_low, mean_profit_of_high]
labels=['low','high']
plt.bar(locations, heights, tick_label = labels)
plt.title('Average profit by Different Popularity')
plt.xlabel('Popularity')
plt.ylabel('Average Profit')


# ANSWER FOR QUESTION 3
# 
# From the above graph we observe that higher popularity leads to more Average profit.

# EVALUATING QUESTION 4
# 
# 4) What are the Features Associate with Top 10 Revenue Movies ?
# 
# 

# In[53]:


top10_revenue = df.nlargest(10,'revenue')
top10_revenue.hist(figsize=(20,20))


# ANSWER FOR QUESTION 4
# 
# From the above plot we conclude that Runtime ranges from 100 mins to 200 mins. The released year are between 1995 to 2015 leads to top 10 revenue movies.

# # CONCLUSION
# 
# 1) Higher budget movie gains higher popularity. Higher budget movie have Mean popularity more than twice than the Mean          popularity of lower budget movie.
# 
# 2) If the movies are within 200 minutes,it will be more popular. Once the movies run over 200 minutes, it's hard for them to gain high popularity.
# 
# 3) Higher popularity leads to more Average profit.
# 
# 4) Runtime ranges from 100 mins to 200 mins. The released year are between 1995 to 2015 leads to top 10 revenue movies.

# # LIMITATIONS
# 
# 1) There are plenty of missing data and many zeros which effect the data analysis process.
# 
# 2) Its very difficult to know how the measurement should be done for coloumn like vote_counts and popularity.
# 
# 3) For movies outside the country currency is not indicated. So its also effect the data analysis process.

# # REFERENCE
# 
# 1) I mainly watch instructor video to know the data analysis process after watching video i follow the same steps.
# 
# 2) I have also paid account of Data Camp. So i also refer some steps from there.
# 
# 

# In[ ]:




