#!/usr/bin/env python
# coding: utf-8

# ## Analyze A/B Test Results
# 
# You may either submit your notebook through the workspace here, or you may work from your local machine and submit through the next page.  Either way assure that your code passes the project [RUBRIC](https://review.udacity.com/#!/projects/37e27304-ad47-4eb0-a1ab-8c12f60e43d0/rubric).  **Please save regularly.**
# 
# This project will assure you have mastered the subjects covered in the statistics lessons.  The hope is to have this project be as comprehensive of these topics as possible.  Good luck!
# 
# ## Table of Contents
# - [Introduction](#intro)
# - [Part I - Probability](#probability)
# - [Part II - A/B Test](#ab_test)
# - [Part III - Regression](#regression)
# 
# 
# <a id='intro'></a>
# ### Introduction
# 
# A/B tests are very commonly performed by data analysts and data scientists.  It is important that you get some practice working with the difficulties of these 
# 
# For this project, you will be working to understand the results of an A/B test run by an e-commerce website.  Your goal is to work through this notebook to help the company understand if they should implement the new page, keep the old page, or perhaps run the experiment longer to make their decision.
# 
# **As you work through this notebook, follow along in the classroom and answer the corresponding quiz questions associated with each question.** The labels for each classroom concept are provided for each question.  This will assure you are on the right track as you work through the project, and you can feel more confident in your final submission meeting the criteria.  As a final check, assure you meet all the criteria on the [RUBRIC](https://review.udacity.com/#!/projects/37e27304-ad47-4eb0-a1ab-8c12f60e43d0/rubric).
# 
# <a id='probability'></a>
# #### Part I - Probability
# 
# To get started, let's import our libraries.

# In[2]:


import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
#We are setting the seed to assure you get the same answers on quizzes as we set up
random.seed(42)


# `1.` Now, read in the `ab_data.csv` data. Store it in `df`.  **Use your dataframe to answer the questions in Quiz 1 of the classroom.**
# 
# a. Read in the dataset and take a look at the top few rows here:

# In[3]:


df = pd.read_csv("ab_data.csv")
df.head()


# b. Use the cell below to find the number of rows in the dataset.

# In[4]:


df.shape


# c. The number of unique users in the dataset.

# In[5]:


df['user_id'].nunique()


# d. The proportion of users converted.

# In[6]:


df.converted.mean()


# e. The number of times the `new_page` and `treatment` don't match.

# In[7]:


line_1 = df.query('group == "treatment" and landing_page == "old_page"').count()


# In[8]:


line_2 = df.query('group == "control" and landing_page == "new_page"').count()


# In[9]:


line_1 + line_2


# f. Do any of the rows have missing values?

# In[10]:


df.isnull().sum()


# `2.` For the rows where **treatment** does not match with **new_page** or **control** does not match with **old_page**, we cannot be sure if this row truly received the new or old page.  Use **Quiz 2** in the classroom to figure out how we should handle these rows.  
# 
# a. Now use the answer to the quiz to create a new dataset that meets the specifications from the quiz.  Store your new dataframe in **df2**.

# In[11]:


df2 = df[((df['group'] == 'treatment') == (df['landing_page'] == 'new_page')) == True]
df2.head()


# In[12]:


# Double Check all of the correct rows were removed - this should be 0
df2[((df2['group'] == 'treatment') == (df2['landing_page'] == 'new_page')) == False].shape[0]


# In[13]:


df2['converted'].value_counts()


# `3.` Use **df2** and the cells below to answer questions for **Quiz3** in the classroom.

# a. How many unique **user_id**s are in **df2**?

# In[14]:


df2['user_id'].nunique()


# b. There is one **user_id** repeated in **df2**.  What is it?

# In[15]:


df2[df2.duplicated('user_id')]


# c. What is the row information for the repeat **user_id**? 

# In[16]:


df2[df2.duplicated(['user_id'], keep = False)]


# d. Remove **one** of the rows with a duplicate **user_id**, but keep your dataframe as **df2**.

# In[17]:


# drop duplicates 
df2.drop_duplicates(keep='first')
df2.duplicated().sum()


# `4.` Use **df2** in the cells below to answer the quiz questions related to **Quiz 4** in the classroom.
# 
# a. What is the probability of an individual converting regardless of the page they receive?

# In[18]:


df2['converted'].mean()


# b. Given that an individual was in the `control` group, what is the probability they converted?

# In[19]:


df.groupby('group').mean()


# c. Given that an individual was in the `treatment` group, what is the probability they converted?

# probability they converted for given that an individual was in the treatment is 0.118920

# d. What is the probability that an individual received the new page?

# In[20]:


df2.landing_page.value_counts()[0]/len(df2)


# e. Consider your results from parts (a) through (d) above, and explain below whether you think there is sufficient evidence to conclude that the new treatment page leads to more conversions.

# **Your answer goes here.**
# About 12% control group converted and 11.89% treatment group converted. So there is not sufficient evidence to conclude that the new page leads to more conversions.
# 

# <a id='ab_test'></a>
# ### Part II - A/B Test
# 
# Notice that because of the time stamp associated with each event, you could technically run a hypothesis test continuously as each observation was observed.  
# 
# However, then the hard question is do you stop as soon as one page is considered significantly better than another or does it need to happen consistently for a certain amount of time?  How long do you run to render a decision that neither page is better than another?  
# 
# These questions are the difficult parts associated with A/B tests in general.  
# 
# 
# `1.` For now, consider you need to make the decision just based on all the data provided.  If you want to assume that the old page is better unless the new page proves to be definitely better at a Type I error rate of 5%, what should your null and alternative hypotheses be?  You can state your hypothesis in terms of words or in terms of **$p_{old}$** and **$p_{new}$**, which are the converted rates for the old and new pages.

# **Put your answer here.**
# 
# H0: Pnew - Pold <= 0 (Old page have higher population rate)
# 
# H1: Pnew - Pold > 0 (new page have higher population rate)
# 
# 

# `2.` Assume under the null hypothesis, $p_{new}$ and $p_{old}$ both have "true" success rates equal to the **converted** success rate regardless of page - that is $p_{new}$ and $p_{old}$ are equal. Furthermore, assume they are equal to the **converted** rate in **ab_data.csv** regardless of the page. <br><br>
# 
# Use a sample size for each page equal to the ones in **ab_data.csv**.  <br><br>
# 
# Perform the sampling distribution for the difference in **converted** between the two pages over 10,000 iterations of calculating an estimate from the null.  <br><br>
# 
# Use the cells below to provide the necessary parts of this simulation.  If this doesn't make complete sense right now, don't worry - you are going to work through the problems below to complete this problem.  You can use **Quiz 5** in the classroom to make sure you are on the right track.<br><br>

# a. What is the **conversion rate** for $p_{new}$ under the null? 

# In[42]:


p_new = df2[df2['landing_page'] == 'new_page'].converted.mean()
print(p_new)


# b. What is the **conversion rate** for $p_{old}$ under the null? <br><br>

# In[43]:


p_old = df2[df2['landing_page']== 'old_page'].converted.mean()
print(p_old)


# In[44]:


p_avg = (p_new + p_old)/2
print(p_avg)


# In[45]:


n_new = df2['landing_page'].value_counts()
print(n_new)


# c. What is $n_{new}$, the number of individuals in the treatment group?

# In[46]:


n_new, n_old = df2['landing_page'].value_counts()
print(n_new)


# d. What is $n_{old}$, the number of individuals in the control group?

# In[47]:


n_new,n_old = df2['landing_page'].value_counts()
print(n_old)


# e. Simulate $n_{new}$ transactions with a conversion rate of $p_{new}$ under the null.  Store these $n_{new}$ 1's and 0's in **new_page_converted**.

# In[54]:


new_page_converted = np.random.choice([0,1], size = n_new, p=(p_avg, 1-p_avg))
print(new_page_converted)
new_page_converted.mean()


# f. Simulate $n_{old}$ transactions with a conversion rate of $p_{old}$ under the null.  Store these $n_{old}$ 1's and 0's in **old_page_converted**.

# In[55]:


old_page_converted = np.random.choice([0,1], size = n_old, p = (p_avg, 1-p_avg))
print(old_page_converted)
old_page_converted.mean()


# g. Find $p_{new}$ - $p_{old}$ for your simulated values from part (e) and (f).

# In[62]:


actual_diff = new_page_converted.mean() - old_page_converted.mean()
print(actual_diff)


# h. Create 10,000 $p_{new}$ - $p_{old}$ values using the same simulation process you used in parts (a) through (g) above. Store all 10,000 values in a NumPy array called **p_diffs**.

# In[63]:


p_diffs = []
new = np.random.binomial(n_new, p_avg, 10000)/n_new
old = np.random.binomial(n_old, p_avg, 10000)/n_old
p_diffs = new - old


# i. Plot a histogram of the **p_diffs**.  Does this plot look like what you expected?  Use the matching problem in the classroom to assure you fully understand what was computed here.

# In[64]:


p_diffs = np.array(p_diffs)
plt.hist(p_diffs)


# In[ ]:





# j. What proportion of the **p_diffs** are greater than the actual difference observed in **ab_data.csv**?

# In[66]:


#compute actual conversion rate
# number of landing new page and converted  / number of landing new page
converted_new = df2.query('converted == 1 and landing_page== "new_page"')['user_id'].nunique()
actual_new = float(converted_new) / float(n_new)

# number of landing old page and converted  / number of landing old page
converted_old = df2.query('converted == 1 and landing_page== "old_page"')['user_id'].nunique()
actual_old = float(converted_old) / float(n_old)

#observed difference in converted rate
obs_diff = actual_diff = actual_new - actual_old
obs_diff


# In[67]:


# create distribution under the null hypothesis
null_vals = np.random.normal(0, p_diffs.std(), p_diffs.size)


# In[69]:


#Plot Null distribution
plt.hist(null_vals)
#Plot vertical line for observed statistic
plt.axvline(x=obs_diff,color ='black')


# k. Please explain using the vocabulary you've learned in this course what you just computed in part **j.**  What is this value called in scientific studies?  What does this value mean in terms of whether or not there is a difference between the new and old pages?

# **Put your answer here.**

# l. We could also use a built-in to achieve similar results.  Though using the built-in might be easier to code, the above portions are a walkthrough of the ideas that are critical to correctly thinking about statistical significance. Fill in the below to calculate the number of conversions for each page, as well as the number of individuals who received each page. Let `n_old` and `n_new` refer the the number of rows associated with the old page and new pages, respectively.

# In[71]:


import statsmodels.api as sm

convert_old = df2.query('converted == 1 and landing_page== "old_page"').user_id.nunique()
convert_new = converted_old = df2.query('converted == 1 and landing_page== "new_page"').user_id.nunique()
n_old = df2.query('landing_page == "old_page"')['user_id'].nunique()
n_new = df2.query('landing_page == "new_page"')['user_id'].nunique()

convert_old,convert_new , n_old , n_new


# m. Now use `stats.proportions_ztest` to compute your test statistic and p-value.  [Here](http://knowledgetack.com/python/statsmodels/proportions_ztest/) is a helpful link on using the built in.

# In[72]:


# compute the sm.stats.proportions_ztest using the alternative
z_score, p_value = sm.stats.proportions_ztest(np.array([convert_new,convert_old]),np.array([n_new,n_old]), alternative = 'larger')
z_score, p_value


# n. What do the z-score and p-value you computed in the previous question mean for the conversion rates of the old and new pages?  Do they agree with the findings in parts **j.** and **k.**?

# **Put your answer here.**
# 
# 1) Since the z-score of 1.3109241984234394 does not exceed the critical value of 1.959963984540054, we fail to reject the null hypothesis. Therefore, the converted rate for new page and old page have no difference. This result is the same as parts J. and K. result.
# 
# 2) The z-score is greater than the value of -0.1645 (one-tail test) and hence it suggests that we can't reject the null.
# 
# 3) And the p-value determines the significance of our resuls. The values are different from parts j and k but it still suggests that there is no statistically significant difference betweem the new and the old page.

# <a id='regression'></a>
# ### Part III - A regression approach
# 
# `1.` In this final part, you will see that the result you achieved in the A/B test in Part II above can also be achieved by performing regression.<br><br> 
# 
# a. Since each row is either a conversion or no conversion, what type of regression should you be performing in this case?

# **Put your answer here.**
# 
# In my opinion Logistic regression is the best option because value is categorical.

# b. The goal is to use **statsmodels** to fit the regression model you specified in part **a.** to see if there is a significant difference in conversion based on which page a customer receives. However, you first need to create in df2 a column for the intercept, and create a dummy variable column for which page each user received.  Add an **intercept** column, as well as an **ab_page** column, which is 1 when an individual receives the **treatment** and 0 if **control**.

# In[76]:


df2['intercept']=1 #define intercept as 1
df2[['control', 'treatment']] = pd.get_dummies(df2['group'])


# In[77]:


df2.tail()


# c. Use **statsmodels** to instantiate your regression model on the two columns you created in part b., then fit the model using the two columns you created in part **b.** to predict whether or not an individual converts. 

# In[78]:


logit = sm.Logit(df3['converted'],df3[['intercept','treatment']])


# d. Provide the summary of your model below, and use it as necessary to answer the following questions.

# In[79]:


results = logit.fit()
results.summary()


# e. What is the p-value associated with **ab_page**? Why does it differ from the value you found in **Part II**?<br><br>  **Hint**: What are the null and alternative hypotheses associated with your regression model, and how do they compare to the null and alternative hypotheses in **Part II**?

# **Put your answer here.**
# 
# The p-value of the treatment (ab_page) is 0.190.
# 
# There is significant difference is observe between part2 and part3, because we have compared the conversion rate of new and old page in part2 and tried to look at if there is a significant difference between them. But, in logistic regression, we are trying to answer if treatment (ab_page) statistically significant attribute to explain the difference in the conversion rate.

# f. Now, you are considering other things that might influence whether or not an individual converts.  Discuss why it is a good idea to consider other factors to add into your regression model.  Are there any disadvantages to adding additional terms into your regression model?

# **Put your answer here.**
# 
# We may add some other factors that affects the people's choice. However adding too much factors lead us bad results, even if we have all the p-values of attiributes significant, the performance of the regression model might not be better. The main idea is to find minimum number of attributes that tell us the maximum information we need.

# g. Now along with testing if the conversion rate changes for different pages, also add an effect based on which country a user lives in. You will need to read in the **countries.csv** dataset and merge together your datasets on the appropriate rows.  [Here](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.join.html) are the docs for joining tables. 
# 
# Does it appear that country had an impact on conversion?  Don't forget to create dummy variables for these country columns - **Hint: You will need two columns for the three dummy variables.** Provide the statistical output as well as a written response to answer this question.

# In[80]:


df_country = pd.read_csv('countries.csv')
df_country.head()


# In[81]:


df3 = df2.join(df_country.set_index('user_id'),on='user_id')
df3.head()


# In[83]:


df3['country'].value_counts()


# In[88]:


# create dummy variables for country
dummy_df = pd.get_dummies(data=df_country, columns=['country'])
df3 = dummy_df.merge(df3, on='user_id')
df3.head()


# In[92]:


logit = sm.Logit(df3['converted'], df3[['UK', 'US', 'intercept']])
result = logit.fit()


# In[93]:


result.summary()


# h. Though you have now looked at the individual factors of country and page on conversion, we would now like to look at an interaction between page and country to see if there significant effects on conversion.  Create the necessary additional columns, and fit the new model.  
# 
# Provide the summary results, and your conclusions based on the results.

# In[96]:


logit_2 = sm.Logit(df3['converted'], df3[['treatment', 'UK', 'US', 'intercept']])
result_2 = logit_2.fit()


# In[97]:


result_2.summary()


# # CONCLUSION:
# 
# 
# 1) All the p-values are greater than 0.05 except intercept. As per we obtaioned in the last regression, we fail to reject H0.
# 
# 2) The old page performs better than new one. 
# 
# 3) There is no enough evidence that we confidently reject the null hypothesis.

# <a id='conclusions'></a>
# ## Finishing Up
# 
# > Congratulations!  You have reached the end of the A/B Test Results project!  You should be very proud of all you have accomplished!
# 
# > **Tip**: Once you are satisfied with your work here, check over your report to make sure that it is satisfies all the areas of the rubric (found on the project submission page at the end of the lesson). You should also probably remove all of the "Tips" like this one so that the presentation is as polished as possible.
# 
# 
# ## Directions to Submit
# 
# > Before you submit your project, you need to create a .html or .pdf version of this notebook in the workspace here. To do that, run the code cell below. If it worked correctly, you should get a return code of 0, and you should see the generated .html file in the workspace directory (click on the orange Jupyter icon in the upper left).
# 
# > Alternatively, you can download this report as .html via the **File** > **Download as** submenu, and then manually upload it into the workspace directory by clicking on the orange Jupyter icon in the upper left, then using the Upload button.
# 
# > Once you've done this, you can submit your project by clicking on the "Submit Project" button in the lower right here. This will create and submit a zip file with this .ipynb doc and the .html or .pdf version you created. Congratulations!

# In[ ]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Analyze_ab_test_results_notebook.ipynb'])

