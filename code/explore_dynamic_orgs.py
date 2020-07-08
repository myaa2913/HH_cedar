#this file prints text for orgs high in dynamism
import csv, json
import pandas as pd
import numpy as np


def extract(var):

    #open output text file
    f = open('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/output/' + var + '.txt', 'w')

    #loop through each reviewid and extract from dictionary
    with open('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/data/dynamic_vars.csv', 'r') as csvfile:

        #load dictionary
        with open('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/data/gd_dict_06232020_annual', 'r') as gd:
            data = json.load(gd)

            read = csv.reader(csvfile, delimiter = ',')

            next(read)

            for row in read:
                orgID = row[0]
                year = row[1]
                dynamic = row[3]
                p95 = row[4]
                d75 = row[5]
                d50 = row[6]
                d_thresh = row[7]

                if var==1 and gd_dict[year][orgID]['pro']['text']:
                    text = gd_dict[year][orgID]['pro']['text'] + gd_dict[year][orgID]['con']['text']
                    f.write(str(text) + '\n')
                    
    csvfile.close()
    f.close()





#import pandas data frame from csv
df = pd.read_pickle('~/projects/def-mcorrito/mcorrito/HH/data/lda_final_4000_25_annual.pkl')

df.columns = range(df.shape[1])

#create column for the culture categories
df['orgid'] = df[0]
df['year'] = df[1]
df['word_count'] = df[2]
df['dynamic'] = df[26]

df = df[['orgid','year','word_count','dynamic']]

#randomly sample reviewid from high dynamic topics
#calculate percentiles from the dynamic variables
df['p95'] = (df.dynamic>=df.dynamic.quantile(0.95)).astype(int)
df['d75'] = (df.dynamic>=df.dynamic.quantile(0.75)).astype(int)
df['d50'] = (df.dynamic>=df.dynamic.quantile(0.50)).astype(int)
df['d_thresh'] = (df['dynamic'] >= 0.04).astype(int)

df.to_csv('~/projects/def-mcorrito/mcorrito/HH/data/dynamic_vars.csv',index=False)



extract('p95')
extract('d75')
extract('d50')
extract('d_thresh')
