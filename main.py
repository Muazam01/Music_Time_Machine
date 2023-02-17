import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

################################################################################################################
MY_CLIENT_ID="CL_ID.txt"
MY_CLIENT_SECRET="CL_SECRET.txt"

REDIRECT_URL="REDIRECT.txt"
MY_TOKEN="token.txt"   #Once your token is generated here paste it in token.txt file and use that file

################################################################################################################

ask=input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD\n ")
URL=f"https://www.billboard.com/charts/hot-100/{ask}/"
ask_=ask.split("-")
year=ask_[0]
month=ask_[1]
day=ask_[2]
response_=requests.get(URL)
response=response_.text
soup=BeautifulSoup(response,"html.parser")
songs=soup.findAll(name="h3",class_="a-font-primary-bold-s")
artists_=soup.findAll(name="span",class_="a-no-trucate")

list_of_songs=[]
list_of_artists=[]
for song in songs:
    song_list=song.text
    name=song_list.strip()
    list_of_songs.append(name)

for a in artists_:
    artist_text=a.text
    artist=artist_text.strip()
    list_of_artists.append(artist)

list_of_songs.pop(0)
list_of_songs.remove("Additional Awards")

spotify_url="https://developer.spotify.com/dashboard/applications/62b0c82562074890af2e06a5357d1547"
spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=MY_CLIENT_ID,client_secret=MY_CLIENT_SECRET,redirect_uri=REDIRECT_URL,scope="playlist-modify-private",show_dialog=True,
        cache_path=MY_TOKEN))


user_id=spotify.current_user()["id"]


#  Fetching data from other website and parsing it
tracks_ = []
for i in range(0,100):
    dict_ = dict()
    dict_["key"]=f"{list_of_songs[i]}"
    dict_["value"]=f"{list_of_artists[i]}"
    tracks_.append(dict_)

song_url=[]
for i in range(0,100):
   result = spotify.search(q=f"track: {tracks_[i]['key']} year: {year}", type='track')
   if len(result['tracks']['items']) > 0:
       song_url.append(result['tracks']['items'][1]['uri'])


playlist= spotify.user_playlist_create(user=user_id,name=f"{year}-{month}-{day} Billboard 100",public=False,collaborative=False, description="Test")
PLAYLIST_ID = playlist["id"]
spotify.playlist_add_items(playlist_id=PLAYLIST_ID,items=song_url)
