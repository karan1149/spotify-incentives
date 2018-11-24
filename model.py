import json
from collections import defaultdict

def get_spotify_assignment(streams):
	artist_counts = defaultdict(int)
	total_count = len(streams)

	for stream in streams:
		artist_counts[stream['artist']] += 1

	for artist in artist_counts:
		artist_counts[artist] /= total_count

	return artist_counts

def get_weighted_assignment(streams, weights):
	pass

def get_groundtruth_assignment(fanbases):
	artist_counts = defaultdict(int)
	total_count = 0.0

	for artist in fanbases:
		artist_counts[artist] += fanbases[artist]
		total_count += fanbases[artist]

	for artist in artist_counts:
		artist_counts[artist] /= total_count

	return artist_counts


if __name__=='__main__':
	with open('dataset.json', 'r') as f:
		data = json.load(f)

	spotify_assignment = get_spotify_assignment(data['streams'])

