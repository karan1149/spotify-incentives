import json
from collections import defaultdict
import evaluate
import create_dataset
from tqdm import tqdm
from assignments import *
import matplotlib.pyplot as plt
import numpy as np

LR = 0.001
EPSILON = 0.001

def calculate_gradient(data, weights, old_error):
	gradient = {k: 0.0 for k in weights}
	for k in weights:
		weights[k] += EPSILON
		weighted_assignment = get_weighted_assignment(data['streams'], weights)
		error = evaluate.calculate_sum_squared_error(weighted_assignment, groundtruth_assignment_by_splitting)
		gradient[k] = (error - old_error) / EPSILON
	return gradient

def minimize_MSE_for_dataset(data, weights):
	weighted_assignment = get_weighted_assignment(data['streams'], weights)
	old_error = evaluate.calculate_sum_squared_error(weighted_assignment, groundtruth_assignment_by_splitting)
	for i in tqdm(range(1000)):
		gradient = calculate_gradient(data, weights, old_error)
		for k in gradient:
			weights[k] -= gradient[k] * LR
		weighted_assignment = get_weighted_assignment(data['streams'], weights)
		error = evaluate.calculate_sum_squared_error(weighted_assignment, groundtruth_assignment_by_splitting)
		print("New error:", error)
		print("Difference:", old_error - error)
		old_error = error

def evaluate_assignment(assignment, groundtruth_assignment_by_splitting, groundtruth_assignment_by_voting):
	print("MSE for splitting groundtruth:", evaluate.calculate_sum_squared_error(assignment, groundtruth_assignment_by_splitting))

	print("MSE for voting groundtruth:", evaluate.calculate_sum_squared_error(assignment, groundtruth_assignment_by_voting))

	print("AAPE for splitting groundtruth:", evaluate.calculate_average_absolute_percent_error(assignment, groundtruth_assignment_by_splitting))

	print("AAPE for voting groundtruth:", evaluate.calculate_average_absolute_percent_error(assignment, groundtruth_assignment_by_voting))

	print("KL for splitting groundtruth:", evaluate.calculate_kl_divergence(assignment, groundtruth_assignment_by_splitting))

	print("KL for voting groundtruth:", evaluate.calculate_kl_divergence(assignment, groundtruth_assignment_by_voting))

def perturb_weights_from_initial(data, weights, groundtruth_assignment_by_splitting, spotify_splitting_mse_error):
	initial_weights = weights.copy()
	weights_size = len(weights)
	weighted_assignment = get_weighted_assignment(data['streams'], initial_weights)
	initial_error = evaluate.calculate_sum_squared_error(weighted_assignment, groundtruth_assignment_by_splitting)
	errors = [0]
	for i in tqdm(range(100)):
		curr_weights = initial_weights.copy()
		perturbations = np.random.randn(weights_size) * 0.1
		for i, k in enumerate(curr_weights):
			curr_weights[k] += perturbations[i]

		weighted_assignment = get_weighted_assignment(data['streams'], curr_weights)
		error = evaluate.calculate_sum_squared_error(weighted_assignment, groundtruth_assignment_by_splitting) - initial_error

		errors.append(error)

	print(errors)
	plt.hist(errors, bins=20)
	plt.title("Errors upon Weight Perturbations")
	plt.xlabel("Change in MSE Error")
	plt.ylabel("Count")
	plt.savefig('perturb_from_initial.png')


def perturb_weights_continuously(data, weights, groundtruth_assignment_by_splitting, spotify_splitting_mse_error):
	initial_weights = weights.copy()
	weights_size = len(initial_weights)
	weighted_assignment = get_weighted_assignment(data['streams'], initial_weights)
	initial_error = evaluate.calculate_sum_squared_error(weighted_assignment, groundtruth_assignment_by_splitting)
	errors = [0]
	for i in tqdm(range(100)):
		perturbations = np.random.randn(weights_size) * 0.1
		for i, k in enumerate(initial_weights):
			initial_weights[k] += perturbations[i]

		weighted_assignment = get_weighted_assignment(data['streams'], initial_weights)
		error = evaluate.calculate_sum_squared_error(weighted_assignment, groundtruth_assignment_by_splitting) - initial_error

		errors.append(error)

	print(errors)
	plt.plot(errors)
	plt.ylim(min(errors) * 1.05, max(max(errors) * 1.05, spotify_splitting_mse_error))
	plt.title("A Random Walk in Weights")
	plt.xlabel("Iteration Number")
	plt.ylabel("Change in MSE Error")
	plt.axhline(y=(spotify_splitting_mse_error - initial_error), color='orange', linestyle='--', label='Spotify Assignment Error')
	plt.legend()
	plt.savefig('perturb_continuously.png')


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

	if any(x == 0 for x in groundtruth_assignment_by_splitting):
		print("WARNING: an artist gets value 0 in groundtruth!")

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

	spotify_splitting_mse_error = evaluate.calculate_sum_squared_error(spotify_assignment, groundtruth_assignment_by_splitting)

	perturb_weights_from_initial(data, weights, groundtruth_assignment_by_splitting, spotify_splitting_mse_error)
	perturb_weights_continuously(data, weights, groundtruth_assignment_by_splitting, spotify_splitting_mse_error)

