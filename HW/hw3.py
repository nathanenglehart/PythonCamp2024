#!/home/nath/Documents/python_environments/nath/bin/python

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

verbose = False

client_id = ""
client_secret = ""

spotify = spotipy.Spotify(client_credentials_manager=
                          SpotifyClientCredentials(client_id=client_id,
                                                   client_secret=client_secret))

uri = "0mhTJOr2GHvDdPtAwl8TtS"

playlist = spotify.playlist_tracks(uri)
tracks = playlist['items']

track_ids = [track['track']['id'] for track in tracks]
audio_features = spotify.audio_features(track_ids)

songs, artists, danceability, energy = [], [], [], []

for i, feature in enumerate(audio_features): 
    
    song_i = tracks[i]['track']['name']
    artist_i = tracks[i]['track']['artists']
    dance_i = feature['danceability']
    energy_i = feature['energy']

    songs.append(song_i)
    artists.append(artist_i)
    danceability.append(dance_i)
    energy.append(energy_i)
    
    if(verbose):
        print("-----------------------")
        print(f"song: {song_i}")
        print(f"artist: {artist_i[0]}")
        print(f"danceability: {dance_i}")
        print(f"energy: {energy_i}")
        print("-----------------------")

df = pd.DataFrame({'song': songs,
                   'artist': artists,
                   'danceability': danceability,
                   'energy': energy})

# What song has the most energy? Danceability?

max_dance_row = df.loc[df['danceability'].idxmax()]
max_energy_row = df.loc[df['energy'].idxmax()]

print("-----------------------")
print(max_dance_row['song'], "has the greatest danceability!")
print(max_energy_row['song'], "has the greatest energy!")
print("-----------------------")

# Of the artists in the playlist, who has the song with the greatest energy? Danceability?

print("-----------------------")
print(max_dance_row['artist'][0]['name'], "has the greatest danceability!")
print(max_energy_row['artist'][0]['name'], "has the greatest energy!")
print("-----------------------")

# Print the top 30 results for the Missouri Federal House and Senate candidates sorted by candidate_id as follows:
# name-party-district

import requests
import re

url = "https://api.open.fec.gov/v1/candidates"
api_key = ""
state = "MO"
office = "H"
per_page = 30
sort = "candidate_id"

parameters = {
    "api_key": api_key,
    "state": state,
    "office": office,
    "per_page": per_page,
    "sort": sort
}

out = requests.get(url, params=parameters)

districts, parties, names, candidate_ids = [], [], [], []

if(out.status_code == 200):
    data = out.json()
    for result in data['results']:
        district = result['district']
        party = result['party']
        name = result['name']
        candidate_id = result['candidate_id']

        districts.append(district)
        parties.append(party)
        names.append(name)
        candidate_ids.append(candidate_id)
else:
    print("failed:", out.status_code)

df = pd.DataFrame({'name': names,
                   'party': parties,
                   'district': districts,
                   'candidate_id': candidate_ids})

df = df.sort_values(by='candidate_id', ascending=True)

print("-----------------------")
for idx, row in df.iterrows():
    print(row['name'] + " - " + row['party'] + " - " + row['district'])
print("-----------------------")

# Print the top 5 states which contributed to the democratic party in 2020 as follows:
# state-amount
# Amount must have a dollar sign in front of it, along with appropriate thousands separators. You may use the re library to achieve this
# (my best attempt given I am not super familiar with the FEC)

url = "https://api.open.fec.gov/v1/schedules/schedule_f"
api_key = "IOQOtZ2mDPMEzHcdVOpKnpMtqnmSLr4kesI5KDF0"
per_page = 25
min_date = '2020-01-01'
max_date = '2020-12-31'
sort = '-expenditure_amount'

parameters = {
    "api_key": api_key,
    "per_page": per_page,
    "min_date": min_date,
    "max_date": max_date,
    "sort": sort,
}

out = requests.get(url, params=parameters)

states, amounts, parties = [], [], []

if(out.status_code == 200):
    data = out.json()
    for result in data['results']:
        state = result['committee']['state']
        party = result['committee']['party']
        amount = result['expenditure_amount']
        states.append(state)
        amounts.append(amount)
        parties.append(party)
else:
    print("failed:", out.status_code)

df = pd.DataFrame({'state': state,
                   'amount': amounts,
                   'party': parties})

df = df[df['party'] == "DEM"]
df = df.head()

print("-----------------------")
for idx, row in df.iterrows():
    amt = str(row['amount'])
    amt = re.sub(r'(?<=\d)(?=(\d{3})+$)', ',', amt) 
    print(row['state'] + " - " + amt)
print("-----------------------")
