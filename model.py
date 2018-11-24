import json
from collections import defaultdict

def get_spotify_assignment(streams):
	artist_counts = defaultdict(int)
	total_count = len(streams)

	for stream in streams:
		artist_counts[stream['artist']] += 1

	for artist in artist_counts:
		artist_counts[artist] /= float(total_count)

	return artist_counts

def get_weighted_assignment(streams, weights):
	artist_weighted_counts = defaultdict(float)
	total_weighted_counts = 0.0

	for stream in streams:
		for key in stream:
			if key in weights:
				artist_weighted_counts[stream['artist']] += weights[key] * stream[key]
				total_weighted_counts += weights[key] * stream[key]

	for artist in artist_weighted_counts:
		artist_weighted_counts[artist] /= total_weighted_count

	return artist_weighted_counts


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

	weights = pass
	weighted_assignment = get_weighted_assignment(data['streams'], weights)

	groundtruth_assignment = get_groundtruth_assignment(data['fanbases'])

