#this file adds the glassdoor text for each review into a dictionary and
#saves to a json object  
import csv, nltk, re, json, sys
from itertools import islice

csv.field_size_limit(sys.maxsize)

#function that adds year to dictionary
def addYear(year,dic):
    #create year subdictionary if it doesn't exist        
    if year in dic.keys():
        return dic
    else:
        dic[year] = {}
        return dic 

#function that adds orgID to dictionary
def addOrgID(year,orgID,dic):
    #create org subdictionary if it doesn't exist
    if orgID in dic[year].keys():
        return dic
    else:
        dic[year][orgID] = {}
        return dic

#function that removes non-words, lowercase, and tokenizes
def token(txt):
    txt = re.sub("'","",txt)
    txt = re.sub("\W+"," ",txt)
    txt = re.sub('\d+'," ",txt)
    txt = txt.lower()
    txt = nltk.word_tokenize(txt)
    return txt


#the columns I need are 1 (reviewID), 2 (orgID), 3 (timestamp), and 9-10 (pros, cons)
#will only create dictionary entries for orgs I need by checking against
#set and for valid review IDs
gd_dict = {}

with open('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/temp_data/' + 'agg_pro_con.csv', 'r') as csvfile:
    read = csv.reader(csvfile, delimiter = ',')

    next(read)
    
    for row in read:
        year = row[3]
        orgID = row[2]                                      

        #call function to remove non-words, lowercase, and tokenize
        pro = token(row[0])
        con = token(row[1])

        #add year,month,org,reviewid to dictionary
        gd_dict = addYear(year,gd_dict)
        gd_dict = addOrgID(year,orgID,gd_dict)

        #add text to dictionary and count words
        gd_dict[year][orgID]['pro'] = {}
        gd_dict[year][orgID]['pro']['text'] = pro
        gd_dict[year][orgID]['pro']['wordCount'] = len(pro)

        gd_dict[year][orgID]['con'] = {}
        gd_dict[year][orgID]['con']['text'] = con
        gd_dict[year][orgID]['con']['wordCount'] = len(con)

          

#save dictionary as json object
with open('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/data/' + 'gd_dict_06232020_annual', 'w') as gd:
    json.dump(gd_dict, gd)



            
                
            
