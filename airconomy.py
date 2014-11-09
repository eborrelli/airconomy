
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


# In[1]:

import numpy as np


# In[2]:

import pandas as pd


# In[4]:

# top ten arrivals in the world in 2013
numLines = 10000011
skipLines = 1 # we skip the header line
numChunks = 64
chunkSize = np.ceil((numLines - skipLines) / (numChunks / 1.0)).astype(int)
chunkSize


# In[ ]:

reader = pd.read_csv(bookings_file, sep='\s*\^', skiprows=skipLines, chunksize=chunkSize, header=None)


# In[ ]:

chunk_results = {}
for chunk in reader:
    try:
        tmp = chunk.ix[:,[12,34]].groupby(['X.13']).sum()
        for key,value in dict(tmp['X.35']).iteritems():
            try:
                chunk_results[key] += value
            except KeyError:
                chunk_results[key] = []
                chunk_results[key].append(value)
    except Exception as e:
        pass


# In[ ]:

reduced_results = []
for key,values in chunk_results.iteritems():
    reduced_results.append((key, sum(values).astype(int)))


# In[ ]:

def tuple_sort (a, b):
    if a[1] < b[1]:
        return 1
    elif a[1] > b[1]:
        return -1
    else:
        return cmp(a[0], b[0])


# In[ ]:

reduced_results.sort(tuple_sort)


# In[ ]:

reduced_results[0:10]

