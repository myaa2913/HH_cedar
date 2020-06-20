from corenlp import StanfordCoreNLP
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import re
from sklearn.decomposition import LatentDirichletAllocation as LDA
import nltk, csv

nlp = StanfordCoreNLP(r'G:\JavaLibraries\stanford-corenlp-full-2018-02-27')

nltk.download('stopwords', quiet=True, raise_on_error=True)
stop_words = set(nltk.corpus.stopwords.words('english'))
tokenized_stop_words = nltk.word_tokenize(' '.join(nltk.corpus.stopwords.words('english')))

class Tokenizer(object):
    def __init__(self):
        nltk.download('punkt', quiet=True, raise_on_error=True)
        self.stemmer = nltk.stem.PorterStemmer()
        
    def _stem(self, token):
        if (token in stop_words):
            return token  # Solves error "UserWarning: Your stop_words may be inconsistent with your preprocessing."
        return self.stemmer.stem(token)
        
    def __call__(self, line):
        tokens = nltk.word_tokenize(line)
        tokens = (self._stem(token) for token in tokens)  # Stemming
        return list(tokens)

# Helper function
def print_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()

    with open('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/output/top_words','w') as csvfile:
        writer = csv.writer(csvfile,delimiter=',',lineterminator='\n')

        for topic_idx, topic in enumerate(model.components_):
            writer.writerow(["\nTopic #%d:" % topic_idx])
            writer.writerow([" ".join([words[i]
                                       for i in topic.argsort()[:-n_top_words - 1:-1]])])
    csvfile.close()
                        
# Tweak the two parameters below
number_topics = 100
number_words = 20        

gd = pd.read_csv('~/projects/def-mcorrito/mcorrito/HH/temp_data/agg_pro.csv',nrows=1000)

ids = gd[['employerid','year']]

# Remove punctuation
gd['pro_text'] = gd['pro_text'].map(lambda x: re.sub('\W+', ' ', x))
gd['pro_text'] = gd['pro_text'].map(lambda x: re.sub('\d+', ' ', x))

# Initialise the count vectorizer with the English stop words
count_vectorizer = CountVectorizer(lowercase=True,
                                   stop_words=tokenized_stop_words,
                                   tokenizer=Tokenizer(),
                                   max_features=5000)

# Fit and transform the processed titles
count_data = count_vectorizer.fit_transform(gd['pro_text'])

# Create and fit the LDA model
lda = LDA(n_components=number_topics,
          n_jobs=-1,
          random_state=182,
          learning_method='online')
fit = lda.fit(count_data)
topic_weights = lda.transform(count_data)
weights = pd.DataFrame(topic_weights)
final = pd.concat([ids,weights],axis=1,ignore_index=True)
final.to_csv('~/projects/def-mcorrito/mcorrito/HH/data/lda_weights.csv',index=False,header=False)

# Print the topics found by the LDA model
print_topics(lda, count_vectorizer, number_words)
