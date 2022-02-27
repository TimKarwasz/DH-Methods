import re
import os
import time
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from langdetect import detect
import argparse



parser = argparse.ArgumentParser(description='A script for analysing songs of different music genres')

parser.add_argument("--genre", help="Choose the genre, which u want to analyze", default="hiphop")

args = parser.parse_args()

def read_dir_create_corpus(path):
    # these words will get removed
    forbiddenWords = ['<|', '|>', 'Embed', "embed"]
    regex = re.compile('|'.join(map(re.escape, forbiddenWords)))
    corpus = []
    song_counter = 0
    for filename in os.listdir(path):
        with open(path + filename, "r", encoding="utf8") as f:
            contents = f.read()
            splitted_in_songs = re.split("endoftext", contents)
            
            english_songs_same_artist = []
            for song in splitted_in_songs:
                
                try:
                    which_language = detect(song)
                except Exception as e:
                    print(e)
                    pass

                #if the language is not english, the lyric does not get added
                if which_language == "en":
                    cleaned_song = regex.sub("", song)
                    english_songs_same_artist.append(cleaned_song)

            song_counter += len(english_songs_same_artist)
            corpus.append(english_songs_same_artist)



    print("Amount of unique artists: {}".format(len(corpus)))
    print("Amount of unique songs: {}".format(song_counter))
    # returns a list, where each item contains all songs from one artist
    return corpus


def write_corpus_to_one_file(corpus, filename):
    # writes all songs in one file
    with open("data\\whole_corpora\\" + filename + ".txt", "w", encoding="utf-8") as file:
        for document in corpus:
            for song in document:
                file.write(song)


def check_word_count(filename):
    # this funnction is just for checking purposes
    with open("data\\whole_corpora\\" + filename + ".txt", "r", encoding="utf-8") as file:
        contents = file.readlines()

    word_count = 0
    for line in contents:
        word_count += len(line)

    print("Checking of word count : {}".format(word_count))

def create_wordcloud(corpus):
    """
    word_count = 0
    for document in corpus:
        for song in document:
            word_count += len(song)
    print("Amount of total words: {}".format(word_count))
    """
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
 
    #plt.show()  


if __name__ == "__main__":
    t = time.process_time()

    if "rock" in args.genre:
        data_folder = "lyrics_rock"
    elif "randb" in args.genre:
        data_folder = "lyrics_RandB"
    elif "hiphop" in args.genre:
        data_folder = "lyrics"


    corpus = read_dir_create_corpus("data\\" + data_folder + "\\")
    

    #write_corpus_to_one_file(corpus, args.genre)
    #check_word_count(args.genre)
    #create_wordcloud(corpus)

    elapsed_time = time.process_time() - t
    print("The script took {} seconds".format(elapsed_time))
    exit()