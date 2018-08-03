from NeuralEvolutionFlappy.neat import NEAT
import sys


# Driver for NEAT solution to FlapPyBird
def evolutionary_driver(network_options):
	""" This function takes in user parameters for the neural network
		and boots up the neural net via the start evolutionary process method

		Input: dictionary {}
		No outputs
	"""
	# Pass in:
	#	 Topology of an organism (input neurons, output neurons, hidden neurons, hidden layers)
	#	 Number of species to create
	#	 Number of generations per species
	#	 Number of organisms/networks per generation

	# Instantiate a NEAT object
	solver = NEAT(network_options, 5, 10000, 10)
	# Boot up the NEAT algorithm
	solver.start_evolutionary_process()


if __name__ == "__main__":
	# Create variables for the neural network parameters and the game parameter
	def_input_neurons = 10
	def_output_neurons = 1
	def_hidden_neurons = 2
	def_hidden_layers = 1
	def_parameter_options = 0
	def_load_from_save = "None"
	# Create a dictionary to hold these values and associate them with flags
	options = {}
	options['-i'] = def_input_neurons
	options['-o'] = def_output_neurons
	options['-h'] = def_hidden_neurons
	options['-l'] = def_hidden_layers
	options['-p'] = def_parameter_options
	options['-x'] = def_load_from_save
	# Check for flags and if they exist loop through them to find out which ones they are
	if (len(sys.argv) > 1):
		for i in range(1, len(sys.argv), 2):
			if sys.argv[i] == '-x':
				options[sys.argv[i]] = sys.argv[i + 1]
			else:
				options[sys.argv[i]] = int(sys.argv[i + 1])

	params = (options['-i'], options['-o'], options['-h'], options['-l'], options['-p'], options['-x'])

	# Call the above function with the user inputs
	evolutionary_driver(params)
