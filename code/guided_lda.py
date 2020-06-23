from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import re
from sklearn.decomposition import LatentDirichletAllocation as LDA
import nltk, csv, scipy, pickle
import guidedlda

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
number_topics = 500
number_words = 50        

gd = pd.read_csv('~/projects/def-mcorrito/mcorrito/HH/temp_data/agg_pro.csv')
# print("csv load done")

ids = gd[['employerid','year']]

# # Remove punctuation
gd['pro_text'] = gd['pro_text'].map(lambda x: re.sub('\W+', ' ', x))
gd['pro_text'] = gd['pro_text'].map(lambda x: re.sub('\d+', ' ', x))

# gd.to_pickle("~/projects/def-mcorrito/mcorrito/HH/temp_data/pro_text_processed.pkl")

#gd = pd.read_pickle('~/projects/def-mcorrito/mcorrito/HH/temp_data/pro_text_processed.pkl')

# Initialise the count vectorizer with the English stop words
count_vectorizer = CountVectorizer(lowercase=True,
                                   stop_words=tokenized_stop_words,
                                   tokenizer=Tokenizer(),
                                   max_features=5000)

# Fit and transform the processed titles
count_data = count_vectorizer.fit_transform(gd['pro_text'])
vocab = count_vectorizer.get_feature_names()
word2id = dict((v, idx) for idx, v in enumerate(vocab))
#pickle.dump(vocab,open('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/temp_data/vocab.pkl','w'))

#pickle.dump(word2id,open('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/temp_data/word2id.pkl','w'))



#scipy.sparse.save_npz('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/temp_data/count_data.npz', count_data)

#count_data = scipy.sparse.load_npz('/home/mcorrito/projects/def-mcorrito/mcorrito/HH/temp_data/count_data.npz')




#count_data = count_data.toarray()


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

# # Guided LDA with seed topics.
# seed_topic_list = [['innov','experi','experiment','dynam','fast','creativ']]

# seed_topics = {}
# for t_id, st in enumerate(seed_topic_list):
#     for word in st:
#         seed_topics[word2id[word]] = t_id

# # Normal LDA without seeding
# model = guidedlda.GuidedLDA(n_topics=20, n_iter=100, random_state=182, refresh=20)
# print(model.fit(count_data,seed_topics=seed_topics,seed_confidence=0.15))

# topic_word = model.topic_word_
# n_top_words = 20
# for i, topic_dist in enumerate(topic_word):
#     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
#     print('Topic {}: {}'.format(i, ' '.join(topic_words)))
