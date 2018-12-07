# Code to generate a dataset. Outputs a JSON file containing a dictionary
# with two keys: 'streams' and 'users'. 'streams' is a list containing
# dictionaries representing individual streams (these dictionaries map 
# from stream feature name to value). 'users' is a list of lists of user
# affinities for different users, e.g. element 0 of the larger list is 
# the list of artists user 0 has an affinity for.
import json
import numpy as np
from tqdm import tqdm
import random

OUTPUT_FILE = 'dataset.json'
NUM_USERS = 2000
GEOMETRIC_AFFINITY_PROB = .2

STREAMS_BINOMIAL_N = 500
STREAMS_BINOMIAL_P = .5

AFFINITY_LISTEN_PROB = .4

ARTISTS = {
	"Drake": {"cult-following": 5, "popularity": 100},
	"Beyonce": {"cult-following": 10, "popularity": 20},
	"Radiohead": {"cult-following": 15, "popularity": 10},
	"MXXNLIGHT": {"cult-following": .3, "popularity": .3},
	"Frank Ocean": {"cult-following": 20, "popularity": 2},
	"J Cole": {"cult-following": 15, "popularity": 20},
	"Kendrick": {"cult-following": 15, "popularity": 25},
	"Nicki Minaj": {"cult-following": 2, "popularity": 30},
	"Kanye": {"cult-following": 15, "popularity": 25},
	"Chance the Rapper": {"cult-following": 20, "popularity": 15},
	"Eminem": {"cult-following": 10, "popularity": 3},
	"Sheck Wes": {"cult-following": .2, "popularity": 10}
}

def sample_artist_by_key(ARTISTS, key):
	artist_values = {}
	total = float(sum(ARTISTS[artist][key] for artist in ARTISTS))

	artist_pairs = [(artist, ARTISTS[artist][key] / total) for artist in ARTISTS]
	artist_pairs_names, artist_pairs_values = zip(*artist_pairs)
	while True:
		choice = np.random.choice(len(artist_pairs), p=artist_pairs_values)
		yield artist_pairs_names[choice]


def generate_dataset(save=True):
	users = []
	streams = []

	cult_following_generator = sample_artist_by_key(ARTISTS, 'cult-following')
	popularity_generator = sample_artist_by_key(ARTISTS, 'popularity')

	for i in tqdm(range(NUM_USERS)):
		affinities = [next(cult_following_generator)]
		while random.random() < GEOMETRIC_AFFINITY_PROB and len(affinities) < len(ARTISTS):
			next_artist = next(cult_following_generator)
			while next_artist in affinities:
				next_artist = next(cult_following_generator)
			affinities.append(next_artist)
		num_streams = np.random.binomial(STREAMS_BINOMIAL_N, STREAMS_BINOMIAL_P)
		users.append(affinities)

		for j in range(num_streams):
			# If is an "affinity listen".
			if random.random() < AFFINITY_LISTEN_PROB:
				artist = random.choice(affinities)
				first_listen = 1 if random.random() < .4 else 0
				user_hearts_song = 1 if random.random() < .3 else 0
				autoplay_song = 1 if random.random() < .3 else 0
				user_playlist_song = 1 if random.random() < .2 else 0
				spotify_playlist_song = 1 if random.random() < .05 else 0
				searched_song = 1 if random.random() < .2 else 0
				searched_album = 1 if random.random() < .3 else 0
				daily_mix = 1 if random.random() < .3 else 0
				played_recently = 1 if random.random() < .4 else 0
			else:
				artist = next(popularity_generator)
				first_listen = 1 if random.random() < .1 else 0
				user_hearts_song = 1 if random.random() < .05 else 0
				autoplay_song = 1 if random.random() < .7 else 0
				user_playlist_song = 1 if random.random() < .05 else 0
				spotify_playlist_song = 1 if random.random() < .3 else 0
				searched_song = 1 if random.random() < .01 else 0
				searched_album = 1 if random.random() < .03 else 0
				daily_mix = 1 if random.random() < .2 else 0
				played_recently = 1 if random.random() < .05 else 0

			stream = {"artist": artist, "first_listen": first_listen, "user_hearts_song": user_hearts_song, "autoplay_song": autoplay_song, "user_playlist_song": user_playlist_song, "spotify_playlist_song": spotify_playlist_song, "searched_song": searched_song, "searched_album": searched_album, "daily_mix": daily_mix, "played_recently": played_recently}
			streams.append(stream)

	dataset = {'users': users, 'streams': streams}

	if save:
		print("Saving dataset...")
		with open(OUTPUT_FILE, 'w') as f:
			json.dump(dataset, f)
		print("Saved dataset!")
	return dataset

if __name__=='__main__':
	generate_dataset()
