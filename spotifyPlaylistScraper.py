from __future__ import unicode_literals
import json
import os
import requests
import youtube_dl
from bs4 import BeautifulSoup

url = input('Please paste link to desired Spotify playlist... ')

r = requests.get(url)
print("Status " + str(r.status_code))

soup = BeautifulSoup(r.content, 'html.parser')

script = soup.find_all('script')[7].string.strip()[35:-1]

data = json.loads(script)

song_list = data['tracks']['items']

# Structure of each song obj scraped from playlist
class Song:
    def __init__(self, title):
        self.title = title
        self.artists = [] #creates a new empty list for each song

    def add_artist(self, artist):
        self.artists.append(artist)

    def get_info(self):
        temp = self.title
        for artist in self.artists:
            temp = temp + " " + artist
        return temp

playlist_songs = []

#iterates over list of songs
for aSong in song_list:
    newSong = Song(aSong['track']['name'])

    #iterates artist(s) for each song
    for anArtist in aSong['track']['artists']:
        newSong.add_artist(anArtist['name'])

    playlist_songs.append(newSong)

##-- playlist_songs now populated --##

for song in playlist_songs:
    os.system('youtube-dl --add-metadata --extract-audio --audio-format mp3 ytsearch:\'' + song.get_info() + '\'')
    # edit download preferences above. Audio quality set to HIGH as default
    # see list of download preferences at https://github.com/ytdl-org/youtube-dl
