
# coding: utf-8

# In[13]:

# imports
import pandas as pd
import numpy as np
import bz2
import matplotlib.pyplot as plt
import re


# In[ ]:




# In[ ]:

# count the number of lines in files


# In[2]:

bookings_file = bz2.BZ2File("/home/elvio/workspace_airconomy/data/bookings.csv.bz2", 'r')


# In[3]:

for i, l in enumerate(bookings_file):
    pass


# In[4]:

bookings_file_num_lines = i+1


# In[5]:

print('Num lines in bookings file: ' + str(bookings_file_num_lines))


# In[ ]:




# In[6]:

searches_file = bz2.BZ2File("/home/elvio/workspace_airconomy/data/searches.csv.bz2", 'r')


# In[7]:

for i, l in enumerate(searches_file):
    pass


# In[8]:

searches_file_num_lines = i+1


# In[9]:

print('Num lines in searches file: ' + str(searches_file_num_lines))


# In[ ]:




# In[ ]:




# In[ ]:

# top ten arrivals in 2013


# In[10]:

skipLines = 1 # we skip the header line
numChunks = 64
bookings_chunkSize = np.ceil((bookings_file_num_lines - skipLines) / (numChunks / 1.0)).astype(int)
bookings_chunkSize


# In[14]:

# retrieve the headers
bookings_file.seek(0)
bookings_headers_line = bookings_file.readline()
# for getting the headers, we remove the trailing white spaces from the first line of the file and split on ^ .
pattern = re.compile('\s*\^')
bookings_headers = re.split(pattern, bookings_headers_line.strip())


# In[15]:

# we don't bookings_file.seek(0) so we skip the first line (i.e. the headers)
bookings_reader = pd.read_csv(bookings_file, sep='\s*\^', skiprows=0, chunksize=bookings_chunkSize, names=bookings_headers)


# In[16]:

arr_port_pax = {}
for chunk in bookings_reader:
    tmp = chunk[chunk['year'] == 2013].ix[:,['arr_port','pax']].groupby(['arr_port']).sum()
    for key,value in dict(tmp['pax']).iteritems():
        try:
            arr_port_pax[key] += value
        except KeyError:
            arr_port_pax[key] = []
            arr_port_pax[key].append(value)


# In[17]:

# the reduce part should be useless
arr_port_pax_reduced = []
for key,values in arr_port_pax.iteritems():
    arr_port_pax_reduced.append((key, sum(values).astype(int)))


# In[18]:

# comparator for tuples
def tuple_sort (a, b):
    if a[1] < b[1]:
        return 1
    elif a[1] > b[1]:
        return -1
    else:
        return cmp(a[0], b[0])


# In[19]:

arr_port_pax_reduced.sort(tuple_sort)


# In[20]:

arr_port_pax_reduced[0:10] # top ten arrival airports 2013


# In[ ]:



