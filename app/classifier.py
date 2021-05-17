import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import svm
from joblib import load
from app.preprocessor import preprocess_text, lemm


class Classifier:
    # Выбор классификаторов (векторайзеров?)
    log_reg = load('app/models/logreg.joblib')
    vectorizer = load('app/models/vectorizer.joblib')
    svm = load('app/models/svm.joblib')
    nb = load('app/models/nb.joblib')

    def classify(self, path, method):
        if method == 'logreg':
            cls = self.log_reg
        elif method == 'svm':
            cls = self.svm
        elif method == 'nb':
            cls = self.nb
        data = pd.read_excel(f"{path}/otz.xlsx")
        texts = data['text']
        texts_p = [preprocess_text(t) for t in texts]
        texts_l = lemm(texts_p)
        vectors = self.vectorizer.transform(texts_l)
        result = cls.predict(vectors)
        data['sentiment'] = result
        proba = cls.predict_proba(vectors)
        probs = pd.DataFrame(data=proba, columns=['neg', 'pos'])
        neg_index = probs[probs['neg'] == probs['neg'].max()].index[0]
        pos_index = probs[probs['pos'] == probs['pos'].max()].index[0]
        data['most'] = -1
        data.iloc[neg_index, -1] = 0
        data.iloc[pos_index, -1] = 1
        data.to_excel(f"{path}/otz.xlsx", index=False)

    # def get_most(self, data):
    #     texts = data['text']
    #     texts_p = [preprocess_text(t) for t in texts]
    #     texts_l = lemm(texts_p)
    #     vectors = self.vectorizer.transform(texts_l)
    #     proba = self.log_reg.predict_proba(vectors)
    #     probs = pd.DataFrame(data=proba, columns=['neg', 'pos'])
    #     neg_index = probs[probs['neg'] == probs['neg'].max()].index[0]
    #     pos_index = probs[probs['pos'] == probs['pos'].max()].index[0]
    #     return neg_index, pos_index
