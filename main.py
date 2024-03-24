import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import pprint

BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"
birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'

# Getting Hot 100 songs from bilboard.com for given date in the past
date_to_travel = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
content = requests.get(BILLBOARD_URL+date_to_travel).content
soup = BeautifulSoup(content, "html.parser")
song_names = [song.text.strip() for song in soup.select(selector="li h3#title-of-a-story")]
author_names = [author.text.strip() for author in soup.select(selector="li span.c-label.a-font-primary-s")]

# Spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.environ["SPOTIPY_CLIENT_ID"],
        client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
        show_dialog=True,
        cache_path="token.txt",
        username="darklord-54", 
    )
)
user_id = sp.current_user()["id"]
year = date_to_travel.split("-")[0]
track_uris = []
for song_name in song_names:
    try:
        track = sp.search(q=f"track: {song_name} year: {year}", type='track')["tracks"]["items"][0]
        track_uris.append(track["uri"])
    except IndexError:
        print(f"{song_name} doesn't exists. Skipped.")

playlist_id = sp.user_playlist_create(user_id, f"{date_to_travel} Billboard 100", False)["id"]
esult = sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)