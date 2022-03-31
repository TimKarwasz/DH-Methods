# this script creates the sentiment plot

import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

font = {'size'   : 24}

plt.rc('font', **font)


genres = ["rock", "pop", "hiphop", "country", "metal", "RandB"]
genre_dict = {"rock" : ([],[]), "pop" : ([],[]), "hiphop" : ([],[]), "country" : ([],[]), "metal" : ([],[]), "RandB" : ([],[])}
pretty_genres = {"rock" : "Rock", "pop" : "Pop", "hiphop" : "Hiphop", "country" : "Country", "metal" : "Metal", "RandB" : "R&B"}


word_dict = {"rock" : [], "pop" : [], "hiphop" :[], "country" : [], "metal" : [], "RandB" : []}

# this for loop extracts the sentiment analysis data 
for genre in genres:
    with open("data\\sentiments\\" + genre + ".pkl", "rb") as f:
            sentiments_per_genre = pickle.load(f)


    sentiment_assessments_list = []       
    polarity_list = []
    subjectivity_list = []
    for elem in sentiments_per_genre:
        polarity_list.append(elem[0])
        subjectivity_list.append(elem[1])
        sentiment_assessments_list.append(elem[2])


    genre_dict[genre] = (polarity_list, subjectivity_list)
    word_dict[genre] = sentiment_assessments_list

sentiments_list = []
genre_list = []

# this for loop prepares the data for the plot
for genre in genres:
    neutral_counter = 0
    positive_counter = 0
    negative_counter = 0

    for elem in genre_dict[genre][0]:
        if elem == 0:
            neutral_counter += 1
            sentiments_list.append("neutral")
            genre_list.append(pretty_genres[genre])
        elif elem > 0:
            positive_counter += 1
            sentiments_list.append("positive")
            genre_list.append(pretty_genres[genre])
        elif elem < 0:
            negative_counter += 1
            sentiments_list.append("negative")
            genre_list.append(pretty_genres[genre])
        


# this generates the sentiment plot
df = pd.DataFrame(list(zip(genre_list, sentiments_list)), columns= ["Genre", "Sentiment"])


sns.set(rc = {'figure.figsize':(14,8)})
catplot = sns.catplot(x="Genre", hue="Sentiment", 
                data=df, kind="count", 
                palette={"negative": "#FE2020", 
                         "positive": "#BADD07", 
                         "neutral": "#68BFF5"})

plt.ylabel("Amount of songs")

plt.show()

