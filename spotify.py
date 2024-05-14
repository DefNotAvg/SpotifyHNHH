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

	def get_track_id(self, song):
		'''Obtains relevant info from a single song's next data.

		Args:
			song: Dictionairy containing various information about a given song.

		Returns:
			URI string of the track.
		'''
		results = self.spotify.search('track:' + song['query'], limit=10, offset=0, type='track', market=None)['tracks']['items']
		if results:
			sorted_results = sorted(results, key=lambda item: len(set([artist.lower() for artist in song['artists']])&set([artist['name'].lower() for artist in item['artists']])), reverse=True) # Sort results by number of matched artists
			filtered_results = [item for item in sorted_results if len(set([artist.lower() for artist in song['artists']])&set([artist['name'].lower() for artist in item['artists']])) > 0] # Remove tracks with no matched artists
			if filtered_results:
				if any(item['explicit'] for item in filtered_results):
					return [item for item in filtered_results if item['explicit']][0]['uri'].split(':')[2]
				else:
					return filtered_results[0]['uri'].split(':')[2]
		return None