import requests
from secrets import spotify_user_id, discover_weekly_id
from datetime import date
import json
from refresh import Refresh


class SaveSongs:
    def __init__(self):
        self.spotify_user_id = spotify_user_id
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ''
        self.new_playlist_id = ''
        self.spotify_token = ''

    # Finding our discover weekly's playlist
    def find_songs(self):
        query = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(discover_weekly_id)

        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }

        # sending the query
        response = requests.get(query, headers=header)

        response_json = response.json()
        # print(response)

        # loop through playlist tracks and add them to a list
        for i in response_json['items']:
            self.tracks += (i['track']['uri'] + ',')
        self.tracks = self.tracks[:-1]

        self.add_to_new_playlist()

    def create_playlist(self):
        today = date.today()
        today_formatted = today.strftime("%m/%d/%Y")

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)

        request_body = json.dumps({
            "name": today_formatted + " Discover Weekly",
            "description": "Discover weekly saved before it gets refreshed.",
            "public": True
        })

        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }

        # sending the query
        response = requests.post(query, data=request_body, headers=header)
        response_json = response.json()

        return response_json['id']

    def add_to_new_playlist(self):
        self.new_playlist_id = self.create_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks)

        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }

        response = requests.post(query, headers=header)

        return response.json

    def call_refresh(self):
        print("Refreshing token")

        refresh_caller = Refresh()

        self.spotify_token = refresh_caller.refresh()

        self.find_songs()


s = SaveSongs()
print(s.call_refresh())
