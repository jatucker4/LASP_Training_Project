from NeuralEvolutionSnake.species import Species


class NEAT(object):

    def __init__(self,
                 topology,
                 num_species=5,
                 num_generations_per_spec=100,
                 num_networks_per_gen=10):
        # Create class variables from the values passed in
        self.num_species = num_species
        self.num_generations_per_spec = num_generations_per_spec
        self.num_networks_per_gen = num_networks_per_gen
        self.organism_topology = topology

        self.species = {}

    def start_evolutionary_process(self):
        """ This method creates new species up to the number of species
            and it addes them to the species dictionary. It then prints
            their ID in a well formatted way.

            There are no inputs or outputs
        """
        # Create a new species up to the number of species
        for s_id in range(self.num_species):
            new_species = Species(self.organism_topology,
                                  self.num_generations_per_spec,
                                  self.num_networks_per_gen,
                                  s_id)
            # Add the species to the species dictionary
            self.species[s_id] = new_species
        # print the species ID and evolve the species
        for s_id, s in self.species.items():
            self.pretty_print_s_id(s_id)
            s.evolve()

    def pretty_print_s_id(self, s_id):
        """ This method prints the spcies ID in a well formatted way. """
        print("\n")
        print("====================")
        print("===  Species:", s_id, " ===")
        print("====================")
        print("\n")

