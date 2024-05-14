import os
from helpers import *
from hnhh import HNHH
from spotify import Spotify

if __name__ == '__main__':
	header()
	config = load_from_json('config.json')
	os.environ['SPOTIPY_REDIRECT_URI'] = config['redirectURI']
	if not os.getenv('SPOTIPY_CLIENT_ID') or not os.getenv('SPOTIPY_CLIENT_SECRET'):
		environ = load_from_json(config['environmentVariables'])
		os.environ['SPOTIPY_CLIENT_ID'] = environ['SPOTIPY_CLIENT_ID']
		os.environ['SPOTIPY_CLIENT_SECRET'] = environ['SPOTIPY_CLIENT_SECRET']
	if os.getenv('SPOTIPY_CLIENT_ID') and os.getenv('SPOTIPY_CLIENT_SECRET'):
		while True:
			for playlist in config['playlists']:
				print('{}\r'.format(center('[{}] Gathering songs for {} playlist...'.format(smart_time(), playlist['apiEndpoint']), display=False)), end='')
				scraper = HNHH(playlist['apiEndpoint'], config['artistReplacements'])
				songs = scraper.get_songs()
				sp = Spotify(config['username'], playlist['scope'])
				print('{}\r'.format(center('[{}] Gathering track IDs for {} playlist...'.format(smart_time(), playlist['apiEndpoint']), display=False)), end='')
				track_ids = [item for item in [sp.get_track_id(song) for song in songs] if item]
				if track_ids:
					sp.spotify.playlist_replace_items(playlist['playlistId'], track_ids)
					center('[{}] Successfully updated {} playlist with {:,}/{:,} songs.'.format(smart_time(), playlist['apiEndpoint'], len(track_ids), len(songs)))
			smart_sleep(3600)
	else:
		center('[{}] Please set environment variables, SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET, before proceeding.'.format(smart_time()))