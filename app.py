from flask import Flask, render_template, request, redirect
import requests
import json

# importing the spotipy library and spotipy credentials
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

app = Flask(__name__)

# setting route
@app.route('/',methods=['GET','POST'])
def index():
  # connect to the spotipy API
  sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="117b49902060434fb6640e9332867736",
                                                             client_secret="27eb9a6630c54fecb484f12876eb6ce6"))
  # access the genre list to pass to the html template
  genre_dictionary = sp.recommendation_genre_seeds()
  genres = genre_dictionary['genres']


  # if a get request
  if request.method == 'GET':
    return render_template('index.html', genres=genres)


  # if a post request (submit button has been pressed)
  if request.method == 'POST': 
    # get user input (note that id is in quotation marks)
    user_genre_input = request.form.get('id')
    # check if the user input exists in genres
    
    if user_genre_input not in genres:
      # render the index.html template along with the needed variables
      return render_template('index.html', genres=genres)
    # if the user has entered a valid genre

    else:
      # connect to the spotipy api to search recommendations based on seed genre
      recommendation_tracks = sp.recommendations(seed_genres=[user_genre_input])
      # create variable to pass to html template
      tracks = []
      # loop over the items in the search result (accessed by recommendation_tracks['tracks'])
      for track in recommendation_tracks['tracks']:
          # append track name to a list
          song = track['name']
          artist = track['artists'][0]['name']
          album = track['album']['name']
          release_date = track['album']['release_date']
          url = track['external_urls']['spotify']
          tracks.append((song,artist,album,release_date,url))
      # render the index.html template along with the needed variables
      return render_template('index.html', genres=genres, tracks=tracks, user_genre_input=user_genre_input)