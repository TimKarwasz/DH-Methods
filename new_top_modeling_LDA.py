import pandas as pd
import os
import gensim
import gensim.corpora as corpora
from gensim.models import TfidfModel
import spacy

#vis
import pyLDAvis
import pyLDAvis.gensim_models

#data cleaning
import nltk.corpus
from nltk.corpus import wordnet as wn
nltk.download('wordnet')
nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

from nltk.corpus import stopwords

from nltk.stem.wordnet import WordNetLemmatizer


stopwords = stopwords.words("english")


def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma


def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

def prepare_text_for_lda(tokens):
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens


def get_data_from_csv(path):
    dict = {}
    for filename in os.listdir(path):
        with open(path + filename, "r", encoding="utf8") as f:
            df = pd.read_csv(path + filename, header=None)
            tokens = []

        for lyric in df[1]:

                # typecast to string
                lyric = str(lyric)
                lyrics = lyric.split()

                for elem in lyrics:
                    if elem != "Embed" and elem != "Lyrics":
                        if elem.isalpha():
                            new = elem.lower()
                            tokens.append(new)
                            #print(elem)

        dict[filename] = tokens

    return dict

def tfidf(corpus, dict):
    tfidf = TfidfModel(corpus, id2word=dict)

    # Filter low value words and also words missing in tfidf models.

    low_value = 0.002

    for i in range(0, len(corpus)):
        bow = corpus[i]
        low_value_words = []  # reinitialize to be safe. You can skip this.
        tfidf_ids = [id for id, value in tfidf[bow]]
        bow_ids = [id for id, value in bow]
        low_value_words = [id for id, value in tfidf[bow] if value < low_value]
        words_missing_in_tfidf = [id for id in bow_ids if
                                  id not in tfidf_ids]  # The words with tf-idf socre 0 will be missing

        new_bow = [b for b in bow if b[0] not in low_value_words and b[0] not in words_missing_in_tfidf]
        # reassign
        corpus[i] = new_bow

    return corpus

def execute_lda(dict):

    tokens = []
    counter = 0
    for key in dict.keys():

            value = dict[key]
            tokens_new = prepare_text_for_lda(value)
            #print(tokens_new)
            tokens.append(tokens_new)
            #print(key)

    #test = [print(elem[0:20]) for elem in tokens]

    dictionary = corpora.Dictionary(tokens)

    corpus = []
    for text in tokens:

        new = dictionary.doc2bow(text)
        corpus.append(new)

    corpus_new = tfidf(corpus, dictionary)
    #print(corpus_new)

    num_topics = 4
    ldamodel = gensim.models.ldamodel.LdaModel(corpus=corpus_new,
                                               num_topics=num_topics,
                                               id2word=dictionary,
                                               passes=10,
                                               iterations=25,
                                               random_state=100,
                                               update_every=1,
                                               chunksize=2,
                                               alpha="auto")

    topics = ldamodel.print_topics(num_words=10)
    print(topics)

    vis = pyLDAvis.gensim_models.prepare(ldamodel, corpus_new, dictionary, mds="mmds", R=10)
    pyLDAvis.save_html(vis, 'lda.html')



if __name__ == "__main__":

    tokens = get_data_from_csv('data/lyrics_csv_2/')
    corpus = execute_lda(tokens)






