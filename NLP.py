import nltk
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import cross_val_predict
from nltk.corpus import stopwords
from string import punctuation
from sklearn.feature_extraction.text import TfidfTransformer

class NLP():
    def __init__(self):
        pass
    
    def cleanText(self, tweet):
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", tweet).split())
        tweet = ' '.join(re.sub("(\w+:\/\/\S+)", " ", tweet).split())
        tweet = ' '.join(re.sub("[\_\|\.\,\"\'\!\?\:\;\-\=]", " ", tweet).split())
        tweet = tweet.lower()

        return tweet

    def train(self):
        df = pd.read_csv('data/Tweets_Mg.csv', encoding='utf-8')

        l = []
        for i,j in zip(df['Text'], df['Classificacao']):
            t = self.cleanText(i)
            l.append([t, j])

        x_train = []
        y_train = []

        sw = set(stopwords.words('portuguese') + list(punctuation))

        palavras_sem_stopwords = [palavra for palavra in l ]

        for i in l:
            lTemp = i[0].split(" ")
            lPost = []
            
            for j in lTemp:        
                if j not in sw:
                    lPost.append(j)
            
            lFinal = " ".join(lPost)
            x_train.append(lFinal)
            y_train.append(i[1])

    
        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(x_train)

        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


        clf = MultinomialNB().fit(X_train_tfidf, y_train)

        return clf, count_vect, tfidf_transformer
    
    def predict(self, clf, count_vect, tfidf_transformer, lText):
        
        X_new_counts = count_vect.transform(lText)
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)

        predicted = clf.predict(X_new_tfidf)

        return str(predicted)















    
# import spacy


# class NLP():
#     def __init__(self):
#         self.nlp = spacy.load('pt')
#         self.spacy_stopwords = spacy.lang.pt.stop_words.STOP_WORDS

#         self.spacy_stopwords.add('a')
#         self.spacy_stopwords.add('o')
#         self.spacy_stopwords.add('e')
#         self.spacy_stopwords.add('"')


#     def process(self, raw):
#         raw = (raw)
#         pRaw = self.nlp(raw)
#         sentences = list(pRaw.sents)

#         l= []

#         for tokens in sentences:
#             for token in tokens:
#                 if not token.is_stop and not token.is_punct:            
#                     if token.text not in self.spacy_stopwords:
#                         l.append(token)

#         return l