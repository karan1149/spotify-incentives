import json
from collections import defaultdict
import evaluate
import create_dataset
from tqdm import tqdm

LR = 0.001
EPSILON = 0.001

def get_spotify_assignment(streams):
	artist_counts = {artist: 0 for artist in create_dataset.ARTISTS}
	total_count = float(len(streams))

	for stream in streams:
		artist_counts[stream['artist']] += 1

	for artist in artist_counts:
		artist_counts[artist] /= total_count

	return artist_counts

def get_weighted_assignment(streams, weights):
	artist_weighted_counts = {artist: 0.0 for artist in create_dataset.ARTISTS}
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
	artist_counts = {artist: 0.0 for artist in create_dataset.ARTISTS}
	total_count = len(users)

	for user in users:
		for artist in user:
			artist_counts[artist] += 1.0 / len(user)

	for artist in artist_counts:
		artist_counts[artist] /= total_count

	return artist_counts

def get_groundtruth_assignment_by_voting(users):
	artist_counts = {artist: 0 for artist in create_dataset.ARTISTS}
	total_count = 0.0

	for user in users:
		for artist in user:
			artist_counts[artist] += 1
			total_count += 1

	for artist in artist_counts:
		artist_counts[artist] /= total_count

	return artist_counts

def calculate_gradient(data, weights, old_error):
	gradient = {k: 0.0 for k in weights}
	for k in weights:
		weights[k] += EPSILON
		weighted_assignment = get_weighted_assignment(data['streams'], weights)
		error = evaluate.calculate_mean_squared_error(weighted_assignment, groundtruth_assignment_by_splitting)
		gradient[k] = (error - old_error) / EPSILON
	return gradient

def minimize_MSE_for_dataset(data, weights):
	weighted_assignment = get_weighted_assignment(data['streams'], weights)
	old_error = evaluate.calculate_mean_squared_error(weighted_assignment, groundtruth_assignment_by_splitting)
	for i in tqdm(range(1000)):
		gradient = calculate_gradient(data, weights, old_error)
		for k in gradient:
			weights[k] -= gradient[k] * LR
		weighted_assignment = get_weighted_assignment(data['streams'], weights)
		error = evaluate.calculate_mean_squared_error(weighted_assignment, groundtruth_assignment_by_splitting)
		print("New error:", error)
		print("Difference:", old_error - error)
		old_error = error

def evaluate_assignment(assignment, groundtruth_assignment_by_splitting, groundtruth_assignment_by_voting):
	print("MSE for splitting groundtruth:", evaluate.calculate_mean_squared_error(assignment, groundtruth_assignment_by_splitting))

	print("MSE for voting groundtruth:", evaluate.calculate_mean_squared_error(assignment, groundtruth_assignment_by_voting))

	print("AAPE for splitting groundtruth:", evaluate.calculate_average_absolute_percent_error(assignment, groundtruth_assignment_by_splitting))

	print("AAPE for voting groundtruth:", evaluate.calculate_average_absolute_percent_error(assignment, groundtruth_assignment_by_voting))

	print("KL for splitting groundtruth:", evaluate.calculate_kl_divergence(assignment, groundtruth_assignment_by_splitting))

	print("KL for voting groundtruth:", evaluate.calculate_kl_divergence(assignment, groundtruth_assignment_by_voting))


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

	print("\nSpotify:")
	evaluate_assignment(spotify_assignment, groundtruth_assignment_by_splitting, groundtruth_assignment_by_voting)
	print(spotify_assignment)
	print("\nWeighted:")
	evaluate_assignment(weighted_assignment, groundtruth_assignment_by_splitting, groundtruth_assignment_by_voting)
	print(weighted_assignment)

	print()
	print(groundtruth_assignment_by_splitting)

	# minimize_MSE_for_dataset(data, weights)
	# print(weights)

