#this file creates an org/review document term matrix
import csv, json, nltk, re, urllib2

#define function that creates doc-term matrix for top x number of words
def docTerm(dict,numWords):
     
    #import stemmer
    porter = nltk.stem.PorterStemmer()
    
    #prepare stop words list
    stopWords = urllib2.urlopen("https://web.stanford.edu/~mcorrito/stop_words.txt").readlines()
    
    stopWords = {x.strip("\n") for x in stopWords}
    stopWords = {porter.stem(w) for w in stopWords}
    
    #load dictionary
    with open('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/data/' + dict, 'r') as gd:
        data = json.load(gd)

    #initialize dictionary to record popularity of unigrams (unigrams that
    #appear in a high propostion of the total words across an organization)    
    unigrams = {}

    #identify total word count across reviews within org/quarter
    for yr in data.keys():
        for orgID in data[yr].keys():

            txt = {}                    

            for field in data[yr][orgID].keys():
                txt[field] = []

                if data[yr][orgID][field]['wordCount'] > 0:

                    txt[field] = data[yr][orgID][field]['text']

            allTxt = txt['pro'] + txt['con'] 

            #remove stop words, custom stop words, and stem
            tokens = [porter.stem(w) for w in allTxt]
            tokens = [x for x in tokens if x not in stopWords]

            #track frequencies of unigrams in each review
            data[yr][orgID]['all'] = {}
            data[yr][orgID]['all']['wordCount'] = len(tokens)

            data[yr][orgID]['all']['uniCount'] = {}

            for i in set(tokens):

                count = tokens.count(i)

                #for each unigram, act count to dict
                data[yr][orgID]['all']['uniCount'][i] = count

                #add to unigrams dictionary
                if i in unigrams:
                    unigrams[i] += count
                else:
                    unigrams[i] = count

                            
    #get words from the culture model
    cultWords = open('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/data/' + 'top_unigrams_phrase_' + str(numWords) + '_ref_pruned.csv','r')
    read = csv.reader(cultWords,delimiter=",")
    topUnigrams = None
    for row in read:
        topUnigrams = row

    #write org/review doc term matrix to csv
    headerUni = ["orgid"] + ["year"] + topUnigrams 

    with open('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/data/' + "top_unigrams_" + str(numWords) + "_annual.csv","w") as csvfile:
        writer = csv.writer(csvfile,delimiter=",",lineterminator='\n')
        writer.writerow(headerUni)

        for yr in data.keys():
            for orgID in data[yr].keys():

                if data[yr][orgID]['all']['wordCount'] > 0:
                    toWrite = [orgID,yr]

                    for i in topUnigrams:
                        if i in data[yr][orgID]['all']['uniCount']:
                            toWrite.append(str(data[yr][orgID]['all']['uniCount'][i]))
                        else:
                            toWrite.append(str(0)) 

                    writer.writerow(toWrite)
                            
    csvfile.close()    





            
docTerm('gd_dict_06232020_annual',4000)


                 

