
# coding: utf-8

# In[2]:

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




# In[5]:

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




# In[ ]:




# In[ ]:

# monthly number of searches for flights arriving at Malaga, Madrid or Barcelona


# In[3]:

searches_file_num_lines = 20390199
skipLines = 1 # we skip the header line
numChunks = 64
searches_chunkSize = np.ceil((searches_file_num_lines - skipLines) / (numChunks / 1.0)).astype(int)
searches_chunkSize


# In[4]:

airports = { 'AGP': 'Malaga', 'MAD': 'Madrid', 'BCN': 'Barcelona'}


# In[6]:

searches_header_line = searches_file.readline()


# In[8]:

# for getting the headers, we remove the trailing white spaces from the first line of the file and split on ^ .
searches_headers = searches_header_line.strip().split('^')


# In[9]:

# read the file chunk by chunk and filter each chunk before the concat
searches_file.seek(0)
searches_file.readline() # skip the first line
chunk_reader = pd.read_csv(searches_file, sep='\^', skiprows=0, names=searches_headers, chunksize=searches_chunkSize)
# ignore the index during the concatenation
df = pd.concat([chunk[chunk['Destination'].isin(airports.keys())].ix[:, ['Date', 'Destination']] for chunk in chunk_reader], ignore_index=True)
df


# In[10]:

# define a new column that will contain only the date year and month
year_month = []
for i in range(len(df['Date'])):
    year_month.append(df.get_value(i, 'Date')[:-3])
df['year_month'] = year_month


# In[11]:

df.ix[:, ['Date', 'Destination', 'year_month']][0:10]


# In[12]:

# groupby
df_groupedby = df.groupby(['Destination', 'year_month']).count()


# In[13]:

# rename column that stores the num of searches
df_num_searches = df_groupedby.ix[:, ['Date']]
df_num_searches.columns = ['num_searches']


# In[14]:

df_num_searches


# In[15]:

# build the x axis
x = range(len(df_num_searches.ix['AGP'].index.values))
x


# In[16]:

# define the ticks for the x axis
xticks = df_num_searches.ix['AGP'].index.tolist()
xticks


# In[17]:

# values of the index of level 0
df_num_searches.index.levels[0]


# In[19]:

# loop on the index of level 0 (i.e. the airport) and plot
# at the same time we build the legend
labels = []
ax = df_num_searches.ix[df_num_searches.index.levels[0][0]].plot(kind='line', use_index=False)
labels.append(airports[df_num_searches.index.levels[0][0]])
for label in df_num_searches.index.levels[0][1:]:
    df_num_searches.ix[label].plot(kind='line', use_index=False, ax=ax)
    labels.append(airports[label])
    plt.xticks(x, xticks)
plt.legend(labels, title='Destination airports')
plt.xlabel('months')
plt.ylabel('num searches')
plt.title('Num searches per month')
plt.show()
plt.clf()
plt.cla()
plt.close()


# In[20]:

searches_file.close()


# In[ ]:



