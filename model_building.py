import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import argparse

parser = argparse.ArgumentParser(description='model building')
parser.add_argument('--type', default='unigram')
parser.add_argument('--model', default='lr')

args = parser.parse_args()
type = args.type
model = args.model

question = pd.read_csv('merged.csv', usecols=['question', 'category_urlname']).dropna()
print("data loaded")
vectorizer = pickle.load(open('vectorizers/{}.pkl'.format(type), 'rb'))

print("vectorizer loaded")

from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

food_categories = ['sweets_baking', 'drinks', 'food_devices', 'main_courses',
       'food_other', 'celebration', 'food_howto', 'food_buy', 'salads',
       'food_preserving', 'soups', 'food_kid']


y = question.category_urlname.apply(lambda x: 1 if x in food_categories else 0)
X = vectorizer.transform(question.question.values)
print("preprocessing done!")

import numpy as np
n = y.value_counts()[1]
mask = np.hstack([np.random.choice(np.where(y == l)[0], n, replace=False)
                      for l in np.unique(y)])

X_balanced, y_balanced = X[mask], y[mask]

from sklearn.cross_validation import train_test_split


X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.3)

a = list(map(lambda x : 1 if x else 0, y_train))
b = list(map(lambda x : 1 if x else 0, y_test))

clf = LogisticRegression()
if model == 'bayes':
	clf =  BernoulliNB()
if model == 'lr':
	clf = LogisticRegression()
if model == 'rf':
	clf = RandomForestClassifier()

clf.fit(X_train, a)

from sklearn.metrics import roc_auc_score



from sklearn.metrics import classification_report
s = classification_report(b,  clf.predict(X_test))


s += "\nroc_auc: " + str(roc_auc_score(b, clf.predict_proba(X_test)[:, 1]))

f = open('metrics/{}_{}.txt'.format(type, model), 'w')
f.write(s)
f.close()

import pickle
pickle.dump(clf, open('models/{}_{}.pkl'.format(type, model), 'wb'))
