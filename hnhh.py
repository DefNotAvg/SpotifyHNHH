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
		self.build_id = self.get_build_id() # Get buildId after session has been initiated
		self.next_data = '{}_next/data/{}/{}.json'.format(self.homepage, self.build_id, self.api_endpoint) # Set next data URL after buildId has been obtained

	def get_build_id(self):
		'''Obtains buildId from HNHH source code.

		Returns:
			BuildId string.
		'''
		if self.build_id:
			return self.build_id
		else:
			response = self.session.get(self.homepage + self.api_endpoint)
			soup = BeautifulSoup(response.content, 'html.parser')
			next_data = [item.text for item in soup.find_all('script') if item.get('id') == '__NEXT_DATA__'][0]
			return json.loads(next_data)['buildId']

	def get_songs(self):
		'''Obtains songs from HNHH next data.

		Returns:
			List of dictionaries containing a Spotify query and the main artist behind the song.
		'''
		response = self.session.get(self.next_data)
		return [self.song_info(item['song']) for item in response.json()['pageProps']['data']]

	def song_info(self, song):
		'''Obtains relevant info from a single song's next data.

		Args:
			song: Next data song dictionary.

		Returns:
			Dictionary containing a Spotify query and the main artist behind the song.
		'''
		song_name = html.unescape(song['songName'])
		artists = [html.unescape(item['name']) for item in song['artistTags']['nodes']]
		main_artist = artists[0]
		query = '{} {}'.format(song_name, ' '.join(artists))
		return {
			'query': query,
			'mainArtist': main_artist
		}