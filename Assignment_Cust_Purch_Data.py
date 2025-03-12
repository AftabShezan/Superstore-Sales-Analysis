#!/usr/bin/env python
# coding: utf-8

# # Ecommerce Purchases Exercise Overview
# 
# Hi Guys,<br>
# After a crash course on pandas for data analysis, its time to do some practice!!!<br>
# Because of privacy issues, I have created a fake dataset here with 30K entries. <br>
# The situation is, customers are providing some personal information while purchasing stuff on-line or in-store. For some reasons, your client wants to know the answer to some of his questions from the dataset, let's try to help him!.<br>
# 
# *Feel free to consult the solutions if needed. Please note, the tasks given in the exercises, can be solved in different ways. Try your best answer and compare with the solutions.* <br>
# &#9758; The dataset is provided in the course downloads. 

# **1. Import Pandas and Read the csv file.**

# In[1]:


import pandas as pd 


# In[2]:


df=pd.read_csv('Cust_Purch_FakeData.csv')


# In[ ]:





# **2. Its good idea to see how the data look like, display first 5 rows of your data-set.**

# In[3]:


# Code here please
df.head()


# In[ ]:





# **3. How many entries your data have? 
# Can you tell the no. of columns in your data?**

# In[4]:


# Code here please
df.info()


# In[ ]:





# **4. What are the max and min ages of your customer? Can you find mean of your customer?**

# In[5]:


# Code here please

print('Max. age of the customer is:',df['age'].max())
print('Min. age of the customer is:',df['age'].min())
print('Avg. age of the customer is:',df['age'].mean().round(2))


# In[ ]:





# **5. What are the three most common customer's names?**<br>
# &#9989; [<code>**value_counts()**</code>](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html) returns object containing counts of unique values. The resulting object will be in descending order so that the first element is the most frequently-occurring element. Excludes NA values by default.

# In[6]:


#combine names and create new column name as 'full_name'

df['full_name'] = df['prefix']+ '' + df['first']+ '' +df ['last']
df.head()


# In[ ]:





# In[7]:


# Code here please

top3_name = df['full_name'].value_counts().head(3)
top3_name 


# In[ ]:





# **6. Two customers have the same phone number, can you find those customers**?

# In[8]:


# Code here please
df['phone'].value_counts().head(2)


# In[9]:


# lets find what phone number is twice!


# In[10]:


# Code here please


# In[11]:


# Now we know the phone number, let's find out the other stuff!


# **7. How many customers have profession "Structural Engineer"?**

# In[12]:


# Code here please
df[df['profession']== "Structural Engineer"].count()


# In[ ]:





# **8. How many male customers are 'Structural Engineer'?**

# In[13]:


# Code here please
male_structural_engineers = df[(df['gender'] == 'Male') & (df['profession'] == 'Structural Engineer')]
male_structural_engineers.head()


# In[ ]:





# **9. Find out the female Structural Engineers from province Alberta (AB)?** 

# In[14]:


# Code here please
female_structural_engineers_ab = df[
    (df['gender'] == 'Female') & 
    (df['profession'] == 'Structural Engineer') & 
    (df['province'] == 'AB')
]
female_structural_engineers_ab


# In[ ]:





# **10. What is the max, min and average spending?**

# In[15]:


# Code here please
print('Max. spending:',df['price(CAD)'].max())
print('min. spending:',df['price(CAD)'].min())
print('Avg. spending:',df['price(CAD)'].mean().round(2))


# In[ ]:





# **11. Who did not spend anything? Company wants to send a deal to encourage the customer to buy stuff!**

# In[16]:


# Code here please
spend_nothing = df[df['price(CAD)'] == 0]
spend_nothing


# In[ ]:





# **12. As a loyalty reward, company wants to send thanks coupon to those who spent 100CAD or more, please find out the customers?**

# In[17]:


# Code here please
who_spent_100CAD = df[df['price(CAD)']>= 100.0]
who_spent_100CAD


# In[ ]:





# **13. How many emails are associated with this credit card number '5020000000000230'?**

# In[18]:


# Code here please

# Filter rows where cc_no is '5020000000000230'
filtered_data = df[df['cc_no'] == '5020000000000230']

# Extract the email column
emails = filtered_data['email']

# Display the emails
print("Emails associated with credit card number '5020000000000230':")
print(emails)


# In[ ]:





# **14. We need to send new cards to the customers well before the expire, how many cards are expiring in 2019?**<br>
# *Use `sum()` and `count()` and see the difference in their use :)*

# In[19]:


# Code here please
# Extract the year from the 'cc_exp' column
df['exp_year'] = df['cc_exp'].apply(lambda x: x.split('/')[1])

# Count the number of cards expiring in 2019 using count()
count_2019 = df[df['exp_year'] == '19'].count()['cc_no']

# Sum the number of cards expiring in 2019 using sum()
sum_2019 = (df['exp_year'] == '19').sum()

print(f"Number of cards expiring in 2019 (using count()): {count_2019}")
print(f"Number of cards expiring in 2019 (using sum()): {sum_2019}")


# In[20]:


#cust[cust['cc_exp'].apply(lambda x: x[5:]) == '19'].count()


# In[21]:


df.head(2)


# **15. How many people use Visa as their Credit Card Provider?**

# In[22]:


# Code here please
df['cc_type'].value_counts()['Visa']


# In[ ]:





# **16. Can you find the customer who spent 100 CAD using Visa?**

# In[23]:


# Code here please
customer_100_cad_visa = df[(df['price(CAD)'] == 100) & (df['cc_type'] == 'Visa')]
customer_100_cad_visa


# In[ ]:





# **17. What are two most common professions?**

# In[24]:


# Code here please
profession_counts = df['profession'].value_counts().head(2)
profession_counts


# In[ ]:





# **18. Can you tell the top 5 most popular email providers? (e.g. gmail.com, yahoo.com, etc...)**

# In[25]:


# Code here please

df['email_provider'] = df['email'].apply(lambda x: x.split('@')[1])

# Get the value counts of the 'email_provider' column
email_provider_counts = df['email_provider'].value_counts()

# Get the top 5 most popular email providers
top_5_email_providers = email_provider_counts.head(5)

print("Top 5 most popular email providers:")
print(top_5_email_providers)


# In[ ]:





# **19. Is there any customer who is using email with "am.edu"?**<br>
# Hint: Use `lambda` expression in `apply()`. split the email address at `@`.  

# In[26]:


# Code here please


# In[ ]:





# In[ ]:





# **20. Which day of the week, the store gets more customers?**

# In[27]:


# Code here please

weekday_counts = df['weekday'].value_counts()
weekday_counts


# In[ ]:





# # Excellent work!
