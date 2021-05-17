import re
import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem

russian_stopwords = stopwords.words("russian")
mystem = Mystem()

def preprocess_text(text):
    text = text.lower().replace("ё", "е")
    text = re.sub('[^а-яА-Я]+', ' ', text)
    tokens = text.split(' ')
    tokens = [token for token in tokens if token not in russian_stopwords]
    text = " ".join(tokens)
    return text


def lemm(texts):
    lol = lambda lst, sz: [lst[i:i + sz] for i in range(0, len(lst), sz)]
    txtpart = lol(texts, 1000)
    res = []
    for txtp in txtpart:
        alltexts = ' '.join([txt + ' br ' for txt in txtp])

        words = mystem.lemmatize(alltexts)
        doc = []
        for txt in words:
            if txt != '\n' and txt.strip() != '':
                if txt == 'br':
                    doc = ' '.join(doc)
                    res.append(doc)
                    doc = []
                else:
                    doc.append(txt)

    return res