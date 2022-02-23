import requests
from bs4 import BeautifulSoup



def save_list_to_file(filename, liste):
    with open("data//" + filename, 'w', encoding="utf-8") as f:
            for element in liste:
                    f.write(element + "\n")




# Get list of R&B musicans
soup = BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_R%26B_musicians").text, "lxml")

res = soup.findAll("a")

list_RandB = []

for elem in res:
    list_RandB.append(elem.text)

# remove any lines which do not contain bands
list_RandB = list_RandB[49:1072]
list_RandB = [line for line in list_RandB if line[0] != "[" and line != "edit" ]

#for elem in list_RandB:
    #print(elem)

save_list_to_file("RandB_musicans.txt", list_RandB)


# Get list of rock musicans A-M
soup = BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_hard_rock_musicians_(A%E2%80%93M)").text, "lxml")

#res = soup.select('li a')
res = soup.findAll("a")

list_rock_part1 = []

for elem in res:
    list_rock_part1.append(elem.text)

# remove any lines which do not contain bands
list_rock_part1 = list_rock_part1[25:463]
list_rock_part1 = [line for line in list_rock_part1 if line[0] != "[" and line != "edit" ]

#for elem in list_rock_part1:
    #print(elem)

#save_list_to_file("hip_hop_musicans.txt", list_hip_hop)


# Get list of rock musicans N-Z
soup = BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_hard_rock_musicians_(N%E2%80%93Z)").text, "lxml")

res = soup.findAll("a")

list_rock_part2 = []

for elem in res:
    list_rock_part2.append(elem.text)

# remove any lines which do not contain bands
list_rock_part2 = list_rock_part2[20:272]
list_rock_part2 = [line for line in list_rock_part2 if line[0] != "[" and line != "edit" ]

#for elem in list_rock_part2:
    #print(elem)

# join both lists
complete_rock_list = list_rock_part1 + list_rock_part2
save_list_to_file("rock_musicans.txt", complete_rock_list)


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
