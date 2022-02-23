import re
import os
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from langdetect import detect


def read_dir_create_corpus(path):
    corpus = []
    for filename in os.listdir(path):
        with open(path + filename, "r", encoding="utf8") as f:
            #contents = f.read()
            contents = f.readlines()
            contents = [line for line in contents if "endoftext" not in line]
            contents = "".join(contents)

            try:
                which_language = detect(contents)
            except Exception as e:
                pass

            #if the language is not english, the lyric does not get added
            if which_language == "en":

                corpus.append(contents)


    return corpus


if __name__ == "__main__":

    corpus = read_dir_create_corpus("C:\\Users\\Tim\\Desktop\\DH_methods\\data\\lyrics\\")
    print(len(corpus))
    df = pd.DataFrame(corpus)
    

    comment_words = ''
    stopwords = set(STOPWORDS)
 
    # iterate through the csv file
    for lyric in df[0]:
     
        # typecaste to string
        lyric = str(lyric)
 
        # split the value
        tokens = lyric.split()
     
        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
     
        comment_words += " ".join(tokens)+" "
 
    wordcloud = WordCloud(width = 800, height = 800,
                background_color ='black',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)
 
    # plot the WordCloud image                      
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
 
    plt.show()  