import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pickle
import argparse

parser = argparse.ArgumentParser(description='vectorizer building')
parser.add_argument('--type', default='unigram')

args = parser.parse_args()

type = args.type

question = pd.read_csv('merged.csv', usecols=['question']).dropna()
print('data loaded')

if type == 'unigram':
	vectorizer = CountVectorizer(ngram_range=(1,1))
	vectorizer.fit(question.question.values)
if type == 'unigram_tfidf':
        vectorizer = TfidfVectorizer(ngram_range=(1,1))
        vectorizer.fit(question.question.values)

if type == 'bigram_tfidf':
        vectorizer = TfidfVectorizer(ngram_range=(2,2))
        vectorizer.fit(question.question.values)

if type == 'bigram':
        vectorizer = CountVectorizer(ngram_range=(2,2))
        vectorizer.fit(question.question.values)

if type == 'bigram_unigram':
        vectorizer = CountVectorizer(ngram_range=(1,2))
        vectorizer.fit(question.question.values)

print("model builded")
pickle.dump(vectorizer, open('vectorizers/{}.pkl'.format(type), 'wb'))
