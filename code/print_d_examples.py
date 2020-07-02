#this file prints glassdoor phrases that are high in dynamic to a csv file
import csv, json

def extract(filename):

    #open output text file
    f = open('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/output/' + filename + '.txt', 'w')    

    #loop through each reviewid and extract from dictionary
    with open('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/output/' + filename + '.csv', 'r') as csvfile:

        #load dictionary
        with open('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/data/phrase_dict_all_02012020', 'r') as gd:
            data = json.load(gd)

            read = csv.reader(csvfile, delimiter = ',')

            next(read)

            for row in read:
                phraseID = row[0]

                #loop through dictionary to find reviewid
                for orgID in data.keys():
                    for reviewID in data[orgID].keys():
                        if phraseID in data[orgID][reviewID]['all'].keys():
                            text = data[orgID][reviewID]['all'][phraseID]['text']
                            f.write(str(text) + '\n')                             

    csvfile.close()
    f.close()

extract('d95_reviewids')
extract('d75_reviewids')





