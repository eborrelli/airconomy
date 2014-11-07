
# coding: utf-8

# In[1]:

import bz2


# In[2]:

bookings_file = bz2.BZ2File("/home/elvio/workspace_airconomy/data/bookings.csv.bz2", 'r')


# In[3]:

for i, l in enumerate(bookings_file):
    pass


# In[4]:

bookings_file_num_lines = i+1


# In[5]:

print('Num lines of bookings file: ' + str(bookings_file_num_lines))


# In[6]:

searches_file = bz2.BZ2File("/home/elvio/workspace_airconomy/data/searches.csv.bz2", 'r')


# In[7]:

for i, l in enumerate(searches_file):
    pass


# In[8]:

searches_file_num_lines = i+1


# In[9]:

print('Num lines of searches file: ' + str(searches_file_num_lines))


# In[ ]:



