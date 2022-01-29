import requests
from bs4 import BeautifulSoup



def save_list_to_file(filename, liste):
    with open("data//" + filename, 'w', encoding="utf-8") as f:
            for element in liste:
                    f.write(element + "\n")




# Get list of hip hop musicans
soup = BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_hip_hop_musicians").text, "lxml")

res = soup.select('.div-col')

list_hip_hop = []

for elem in res:
    list_hip_hop.append(elem.text)

save_list_to_file("hip_hop_musicans.txt", list_hip_hop)



# List of country music performers
soup = BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_country_music_performers").text, "lxml")

res = soup.findAll("a")

list_of_country_music_artists = []

for elem in res:
    list_of_country_music_artists.append(elem.text)

# remove any lines which do not contain bands
list_of_country_music_artists = list_of_country_music_artists[48:2195]

list_of_country_music_artists_cleaned = []

#remove any invalid lines
for elem in list_of_country_music_artists:
    if elem != "" and elem[0] != "[" and elem != "edit":
        list_of_country_music_artists_cleaned.append(elem)

save_list_to_file("country_music_musicans.txt", list_of_country_music_artists_cleaned)



# List of heavy metal performers
soup = BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_heavy_metal_bands").text, "lxml")

list_of_heavy_metal_bands = []

res = soup.select("a")
for elem in res:
    list_of_heavy_metal_bands.append(elem.text)

# remove any lines which do not contain bands
list_of_heavy_metal_bands = list_of_heavy_metal_bands[30:413]

list_of_heavy_metal_bands_cleaned = []

#remove any invalid lines
for elem in list_of_heavy_metal_bands:
    if elem != "" and elem[0] != "[" and elem != "edit":
        list_of_heavy_metal_bands_cleaned.append(elem)

save_list_to_file("heavy_metal_musicans.txt", list_of_heavy_metal_bands_cleaned)