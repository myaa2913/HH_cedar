#this file extracts a random sample of phrases that score highly on the dynamism culture measure
import csv, json
import pandas as pd
import numpy as np
 
#import pandas data frame from csv
df = pd.read_pickle('~/projects/def-mcorrito/mcorrito/HH/data/lda_phrase_final_4000_25_annual.pkl')

#remove ids
df = df.drop(df.columns[[0,1,3]],axis=1)

df.columns = range(df.shape[1])

#create column for the culture categories
df['dynamic'] = df[24]
df['reviewid'] = df[0]

#keep the culture topics
df = df[['reviewid','dynamic']]

#randomly sample reviewid from high dynamic topics
#calculate percentiles from the dynamic variables
h95 = df.dynamic.quantile(0.95) # 95th percentile
h75 = df.dynamic.quantile(0.75) # 75th percentile

df_h95 = df[df.dynamic>=h95]
df_h95 = df_h95[['reviewid']]
df_h95 = df_h95.sample(n=100)
df_h95.to_csv('~/projects/def-mcorrito/mcorrito/HH/output/d95_reviewids.csv',index=False)

df_h75 = df[df.dynamic>=h75]
df_h75 = df_h75[['reviewid']]
df_h75 = df_h75.sample(n=100)
df_h75.to_csv('~/projects/def-mcorrito/mcorrito/HH/output/d75_reviewids.csv',index=False)

