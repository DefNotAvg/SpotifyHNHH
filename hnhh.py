import html
import json
import requests
from bs4 import BeautifulSoup
from helpers import load_from_json

class HNHH:
	def __init__(self, api_endpoint, artist_replacements):
		'''Initialize HNHH class with some attributes.

		Attributes:
			api_endpoint: API endpoint to scrape for songs.
			build_id: BuildId to scrape for songs.
			homepage: Homepage of HNHH.
			session: Session used across all HTTP requests.
		'''
		self.api_endpoint = api_endpoint
		self.artist_replacements = load_from_json(artist_replacements)
		self.build_id = None # Set buildId to None initially
		self.homepage = 'https://www.hotnewhiphop.com/'
		self.session = requests.Session()

	def get_songs(self):
		'''Obtains songs from HNHH source code.

		Returns:
			List of dictionaries containing a Spotify query and the main artist behind the song.
		'''
		response = self.session.get(self.homepage + self.api_endpoint)
		soup = BeautifulSoup(response.content, 'html.parser')
		songs = soup.find_all('div', class_='ml-4')
		return [self.song_info(song) for song in songs]

	def song_info(self, song):
		'''Obtains relevant info from a single song's HTML.

		Args:
			song: Song HTML.

		Returns:
			Dictionary containing various information about a given song.
		'''
		song_name = html.unescape(song.find('h2').get_text())
		raw_artists = ''.join([html.unescape(item.get_text()).strip() for item in song.find_all('a', class_='mr-1')]).split(',')
		artists = [(self.artist_replacements[artist] if artist in self.artist_replacements.keys() else artist) for artist in raw_artists]
		query = '{} {}'.format(song_name, ' '.join(artists))
		return {
			'artists': artists,
			'query': query,
			'songName': song_name
		}