import lyricsgenius as lg
import time
from pathlib import Path


# this function reads the contents of a given 
def get_file_contents(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("{} file not found".format(filename))


# this function returns the musicans names in a huge array
def read_musicans_lists(filename):
    with open(filename, 'r', encoding= 'utf-8') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    # removes all empty lines
    lines = [line for line in lines if line != ""]
        
    return lines


def write_to_file(filename, lyrics):
    try:
        with open( "data\\lyrics\\" + filename.replace(" ", "_") + ".txt", 'w', encoding="utf-8") as file:
            file.write("\n \n   <|endoftext|>   \n \n".join(lyrics))
            print("Successfully saved {} lyrics\n".format(filename))
    except Exception as e:
        print(e)
        print("The above error with the {} lyrics has occurred".format(filename))


# this function fetches n songs from a given list of artists
def get_lyrics_of_artist(liste, n):
    for name in liste:
        if Path("data\\lyrics\\" + name.replace(" ", "_") + ".txt").is_file():
            if Path("data\\lyrics\\" + name.replace(" ", "_") + ".txt").stat().st_size == 0:
                songs = (genius.search_artist(name, max_songs=n, sort="popularity")).songs
                lyrics = [song.lyrics for song in songs]
                write_to_file(name, lyrics)
                # experimental timeout
                time.sleep(1)
            print("Skipping {} as its already exists".format(name))
        else:
            songs = (genius.search_artist(name, max_songs=n, sort="popularity")).songs
            lyrics = [song.lyrics for song in songs]
            write_to_file(name, lyrics)
            # experimental timeout
            time.sleep(1)




if __name__ == "__main__":

    # read apikey
    api_key = get_file_contents("apikey")

    #create genius object
    genius = lg.Genius(api_key, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

    # read list
    list_of_artists = read_musicans_lists("data\\hip_hop_musicans.txt")
    
    # get lyrics and save them
    get_lyrics_of_artist(list_of_artists, 1)

