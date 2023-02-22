import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Spotify:
	def __init__(self, username, scope):
		'''Initialize Spotify class with some attributes.

		Attributes:
			spotify: Authorized Spotipy instance.
		'''
		token = spotipy.util.prompt_for_user_token(username, scope)
		self.spotify = spotipy.Spotify(auth=token)

	def get_track_id(self, query, main_artist):
		'''Obtains relevant info from a single song's next data.

		Args:
			query: Spotify query.
			main_artist: Main artist behind the song.

		Returns:
			URI string of the track.
		'''
		results = self.spotify.search('track:' + query, limit=10, offset=0, type='track', market=None)['tracks']['items']
		if results:
			filtered_results = [song for song in results if any(item.strip() == song['artists'][0]['name'].lower() for item in main_artist.lower().split(','))]
			if filtered_results:
				if any(item['explicit'] for item in filtered_results):
					return [item for item in filtered_results if item['explicit']][0]['uri'].split(':')[2]
				else:
					return filtered_results[0]['uri'].split(':')[2]
		return None