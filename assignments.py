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