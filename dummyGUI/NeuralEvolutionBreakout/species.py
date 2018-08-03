import os, pickle, datetime
import breakout.breakout as breakout
from NeuralEvolutionBreakout.network import Network

os.chdir(os.getcwd() + '/breakout/')


class Species(object):

    def __init__(self, topology, num_generations, num_networks_per_gen, s_id):

        # Create class variables from the passed in parameters
        self.species_id = s_id
        self.num_generations = num_generations
        self.num_networks_per_gen = num_networks_per_gen
        self.organism_topology = topology
        self.load_Flag = self.organism_topology[5]
        # Check if the user specified a file path
        if self.load_Flag == 'None':
            self.generations = {}
        else:
            self.generations = self.load_from_File(self.load_Flag)

    def evolve(self):
        """ This method has no inputs but for every generation it creates
            a generation of the NEAT algorithm and generates a fitness for it.
        """
        # replicated network ID's is the network ID's selected to survive
        # It is initially set to none to create the generation of networks
        replicated_network_ids = None
        # for every generation create the generation and generate a fitness for it
        for gen in range(self.num_generations):
            self.create_generation(gen, replicated_network_ids)
            self.generate_fitness(gen, self.organism_topology[4])
            replicated_network_ids = self.select_survivors(gen)

    def create_generation(self, generation_number, replicate_ids):
        """ This method takes in the generation number and the ID's for the
            networks that will be replicated. From here it  will either create
            networks or mutate the networks based on the replicate ID's

            Input: Integer, List [<Integers>]
        """
        networks = {}

        # Create a non-inherited generation
        if (not replicate_ids):
            for network_number in range(self.num_networks_per_gen):
                network_info = {"network": network_number,
                                "generation": generation_number,
                                "species": self.species_id}
                # Create a new Network object
                new_neural_network = Network(self.organism_topology, network_info)
                # Create a list of neural networks
                networks[network_number] = new_neural_network

        # Spawn a generation consisting of progeny from fittest predecessors
        elif (replicate_ids):
            network_number = 0
            for r_id in replicate_ids:

                parent_network = self.generations[generation_number - 1][r_id]

                for i in range(2):
                    # Mutated progenies
                    network_info_mutation = {"network": network_number,
                                             "generation": generation_number,
                                             "species": self.species_id}

                    mutated_neural_network = Network(self.organism_topology,
                                                     network_info_mutation,
                                                     parent_network.get_genes())
                    mutated_neural_network.mutate()
                    networks[network_number] = mutated_neural_network

                    network_number += 1

        self.generations[generation_number] = networks

        if self.load_Flag == 'None':
            self.save_to_File(self.generations)

    # This function holds the interface and interaction with Breakout
    def generate_fitness(self, generation_number, parameterNumber):
        """ This method takes in the generation number and the parameter number
            for the user selected in game option. It passes the parameter number
            into the game, and the generation number is used to print the score.

            Input: Integer, Integer
            Output: No output but prints network ID, generation ID, and scores for both"""
        # Initialize the score for the generation to be 0
        generation_score = 0

        print(generation_number)

        for network_num, network in self.generations[generation_number].items():
            # Run the game with each network in the current generation
            results = breakout.main(network, parameterNumber)

            fitness_score = (results) - 200

            # Set the fitness for this network
            network.set_fitness(fitness_score)
            print(network_num)
            print(fitness_score)
            # Add this networks score to the overall score of the generation
            generation_score += fitness_score

    def select_survivors(self, generation_number):
        """ This method takes in the generation number sorts them by fitness
            then selects the networks that will survive and returns them.

            Input: integer
            Output: List [<integers>]"""
        sorted_network_ids = sorted(self.generations[generation_number],
                                    key=lambda k: self.generations[generation_number][k].fitness,
                                    reverse=True)

        alive_network_ids = sorted_network_ids[:self.num_networks_per_gen // 2]
        dead_network_ids = sorted_network_ids[self.num_networks_per_gen // 2:]
        return alive_network_ids

    def save_to_File(self, generations):
        """ This method saves the generation into the Save File folder for the game

            Inputs: Dictionary {Network Objects}
            Outputs: No outputs"""
        # Create a datestring to append to the filename
        dateString = datetime.datetime.now().strftime("%I:%M%pon%B%d")
        # Create the file object with the filename
        file_object = open("SaveFiles/breakout_" + dateString + ".savefile", 'wb')
        # Use pickle to dump the generation structure into the file object
        pickle.dump(generations, file_object)

    def load_from_File(self, filePath):
        """ This method loads the generation structure from a specific file of the users choosing

            Inputs: String
            Outputs: No outputs"""
        # Create file object
        fileObject = open(filePath, 'rb')
        # Load from the file object
        b = pickle.load(fileObject)
        return b
