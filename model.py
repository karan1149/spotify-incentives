import json
from collections import defaultdict
import evaluate
import create_dataset

def get_spotify_assignment(streams):
	artist_counts = defaultdict(int)
	total_count = float(len(streams))

	for stream in streams:
		artist_counts[stream['artist']] += 1

	for artist in artist_counts:
		artist_counts[artist] /= total_count

	return artist_counts

def get_weighted_assignment(streams, weights):
	artist_weighted_counts = defaultdict(float)
	total_weighted_counts = 0.0

	for stream in streams:
		stream_weight = 0.0
		for key in stream:
			if key in weights:
				stream_weight += weights[key] * stream[key]
		stream_weight = max(0, stream_weight)
		artist_weighted_counts[stream['artist']] += stream_weight
		total_weighted_counts += stream_weight

	for artist in artist_weighted_counts:
		artist_weighted_counts[artist] /= total_weighted_counts

	return artist_weighted_counts


def get_groundtruth_assignment_by_splitting(users):
	artist_counts = defaultdict(int)
	total_count = len(users)

	for user in users:
		for artist in user:
			artist_counts[artist] += 1.0 / len(user)

	for artist in artist_counts:
		artist_counts[artist] /= total_count

	return artist_counts

def get_groundtruth_assignment_by_voting(users):
	artist_counts = defaultdict(int)
	total_count = 0.0

	for user in users:
		for artist in user:
			artist_counts[artist] += 1
			total_count += 1

	for artist in artist_counts:
		artist_counts[artist] /= total_count

	return artist_counts

def minimize_MSE_for_dataset(data, weights):
	pass


if __name__=='__main__':
	data = create_dataset.generate_dataset(save=False)

	spotify_assignment = get_spotify_assignment(data['streams'])

	stream_keys = data['streams'][0].keys()

	weights = {"first_listen": .2, "user_hearts_song": .25, "autoplay_song": -0.3, "user_playlist_song": .1, "spotify_playlist_song": -.15, "searched_song": .3, "searched_album": .3, "daily_mix": .05, "played_recently": .4}

	streams_keys = sorted(data['streams'][0].keys())
	weights_keys = sorted(weights.keys())

	weighted_assignment = get_weighted_assignment(data['streams'], weights)

	groundtruth_assignment_by_splitting = get_groundtruth_assignment_by_splitting(data['users'])
	groundtruth_assignment_by_voting = get_groundtruth_assignment_by_voting(data['users'])

	print("MSE between Spotify and splitting groundtruth:", evaluate.calculate_mean_squared_error(spotify_assignment, groundtruth_assignment_by_splitting))

	print("MSE between weighted and splitting groundtruth:", evaluate.calculate_mean_squared_error(weighted_assignment, groundtruth_assignment_by_splitting))

	print("MSE between Spotify and voting groundtruth:", evaluate.calculate_mean_squared_error(spotify_assignment, groundtruth_assignment_by_voting))

	print("MSE between weighted and voting groundtruth:", evaluate.calculate_mean_squared_error(weighted_assignment, groundtruth_assignment_by_voting))

	print("AAPE between Spotify and splitting groundtruth:", evaluate.calculate_average_absolute_percent_error(spotify_assignment, groundtruth_assignment_by_splitting))

	print("AAPE between weighted and splitting groundtruth:", evaluate.calculate_average_absolute_percent_error(weighted_assignment, groundtruth_assignment_by_splitting))

	print("AAPE between Spotify and voting groundtruth:", evaluate.calculate_average_absolute_percent_error(spotify_assignment, groundtruth_assignment_by_voting))

	print("AAPE between weighted and voting groundtruth:", evaluate.calculate_average_absolute_percent_error(weighted_assignment, groundtruth_assignment_by_voting))

	print("KL between Spotify and splitting groundtruth:", evaluate.calculate_kl_divergence(spotify_assignment, groundtruth_assignment_by_splitting))

	print("KL between weighted and splitting groundtruth:", evaluate.calculate_kl_divergence(weighted_assignment, groundtruth_assignment_by_splitting))

	print("KL between Spotify and voting groundtruth:", evaluate.calculate_kl_divergence(spotify_assignment, groundtruth_assignment_by_voting))

	print("KL between weighted and voting groundtruth:", evaluate.calculate_kl_divergence(weighted_assignment, groundtruth_assignment_by_voting))

