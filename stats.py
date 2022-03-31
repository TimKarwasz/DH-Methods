# this srcipt built the dataset, preprocessed it, cleanded it, builds graphs and does sentiment anaylsis

import os
import pickle
import matplotlib.pyplot as plt
import re
import fasttext
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob



model = fasttext.load_model("lid.176.bin")

font = {'size'   : 24}

plt.rc('font', **font)

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('spacytextblob')

genres = ["rock", "pop", "hiphop", "country", "metal", "RandB"]
pretty_genres = ["Rock", "Pop", "Hiphop", "Country", "Metal", "R&B"]

print("#" * 50)
genre_dict = {"Rock" : {}, "Pop" : {}, "Hiphop" : {}, "Country" : {}, "Metal" : {}, "R&B" : {}}

# this for loop does data_cleaning as well as extracts the statistics of the dataset
for (genre, pretty_genre) in zip(genres,pretty_genres):
    artist_counter = 0
    english_songs = []
    sentiments_per_genre = []
    for filename in os.listdir("data\\lyrics_" + genre + "\\"):
        with open("data\\lyrics_" + genre+ "\\" + filename, "r", encoding="utf8") as f:
            songs_per_artist = []
            contents = f.read()
            songs = re.split("endoftext", contents)
            
            for song in songs:
                predictions = model.predict(song.replace("\n", ""))

                if str(predictions[0]) == "('__label__en',)":
                    songtext = song.replace("|", "")
                    songtext = songtext.replace(">", "")
                    songtext = songtext.replace("<", "")
                    songtext = songtext.replace("[", "")
                    songtext = songtext.replace("]", "")
                    songtext = songtext.replace(")", "")
                    songtext = songtext.replace("(", "")
                    songtext = songtext.replace("/", "")
                    songtext = songtext.replace("Lyrics", "")
                    songtext = songtext.replace("Embed", "")
                    songtext = songtext.replace("embed", "")

                    english_songs.append(songtext)
                    songs_per_artist.append(songtext)

                    ## sentiment analysis
                    doc = nlp(songtext)

                    sentiment_per_song = (doc._.blob.polarity, doc._.blob.subjectivity, doc._.blob.sentiment_assessments.assessments)
                    sentiments_per_genre.append(sentiment_per_song)

            # checks if the artist had an english song
            if len(songs_per_artist) != 0:
                artist_counter += 1

    # save sentiments to file
    with open("data\\sentiments\\" + genre + ".pkl", "wb") as f:
        pickle.dump(sentiments_per_genre, f)

    print("Amount of {} songs: {}".format(genre, len(english_songs)))
    genre_dict[pretty_genre]["song_amount"] = len(english_songs)

    print("Amount of {} artists: {}".format(genre, artist_counter))
    genre_dict[pretty_genre]["amount_artists"] = artist_counter

    ## Average song length
    len_list = []
    for song in english_songs:
        len_list.append(len(song))

    avg_song_length = round(sum(len_list) / len(len_list))
    print("Average song length of {} songs: {}".format(genre, avg_song_length))
    genre_dict[pretty_genre]["avg_song_length"] = avg_song_length

    ## Total word count
    print("Combined word count of all {} songs: {}".format(genre, sum(len_list)))
    genre_dict[pretty_genre]["combined_word_count"] = sum(len_list) 

    print("#" * 50)


    # used for generating the dataset
    with open("data\\whole_corpora_new\\" + genre + ".txt", "w", encoding="utf8") as f:
        f.write(" ".join(english_songs))

y_values_list = ["song_amount", "amount_artists", "avg_song_length"]
y_label_list = ['Amount of songs', 'Amount of artists', 'Average song length (in words)']


## automated bar graphs
for num in range(3):
    y_values = []
    for genre in genre_dict.keys():
        y_values.append(genre_dict[genre][y_values_list[num]])

    plt.figure(figsize=(14,8))
    plt.bar(list(genre_dict.keys()),y_values)
    plt.xticks(rotation=70)  
    plt.xlabel('Genre')  
    plt.ylabel(y_label_list[num]) 
    plt.show()


