# Functions to take in two artist payout assignments (predicted and
# groudtruth) and calculate the disparity. Assignments are a mapping
# from artist name to portion of total revenue, in [0, 1].

# Returns average absolute percent error across all artist names.
# e.g. if one artist has payout +30% of groundtruth, another has 
# -45% and another has 15%, the result is .3.
def calculate_average_absolute_percent_error(predicted, groundtruth):
	assert(set(predicted.keys()) == set(groundtruth.keys()))

	total_names = len(predicted)

	total_absolute_percent_error = 0.0

	for name in predicted:
		total_absolute_percent_error += abs(groundtruth[name] - predicted[name]) / groundtruth[name]

	return total_absolute_percent_error / total_names

def test_calculate_average_absolute_percent_error():
	predicted = {'a': .25, 'b': .5, 'c': .25}
	groundtruth = {'a': .25, 'b': .5, 'c': .25}
	assert(calculate_average_absolute_percent_error(predicted, groundtruth) == 0)

	predicted = {'a': .5, 'b': .25, 'c': .25}
	groundtruth = {'a': .25, 'b': .5, 'c': .25}
	assert(calculate_average_absolute_percent_error(predicted, groundtruth) == .5)

if __name__=='__main__':
	test_calculate_average_absolute_percent_error()