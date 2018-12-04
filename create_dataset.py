# Code to generate a dataset. Outputs a JSON file containing a dictionary
# with two keys: 'streams' and 'users'. 'streams' is a list containing
# dictionaries representing individual streams (these dictionaries map 
# from stream feature name to value). 'users' is a list of lists of user
# affinities for different users, e.g. element 0 of the larger list is 
# the list of artists user 0 has an affinity for.
import json

OUTPUT_FILE = 'dataset.json'

def generate_dataset():
	users = []
	streams = []


	dataset = {'users': users, 'streams': streams}

	with open(OUTPUT_FILE, 'w') as f:
		json.dump(dataset, f)

if __name__=='__main__':
	generate_dataset()
