import html
import json
import requests
from bs4 import BeautifulSoup

class HNHH:
	def __init__(self, api_endpoint):
		'''Initialize HNHH class with some attributes.

		Attributes:
			api_endpoint: API endpoint to scrape for songs.
			build_id: BuildId to scrape for songs.
			homepage: Homepage of HNHH.
			session: Session used across all HTTP requests.
		'''
		self.api_endpoint = api_endpoint
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
			Dictionary containing a Spotify query and the main artist behind the song.
		'''
		song_name = html.unescape(song.find('h2').get_text())
		artists = ''.join([html.unescape(item.get_text()).strip() for item in song.find_all('a', class_='mr-1')]).split(',')
		main_artist = artists[0]
		query = '{} {}'.format(song_name, ' '.join(artists))
		return {
			'query': query,
			'mainArtist': main_artist
		}