from enum import Enum
import random

class MutationMethodEnum(Enum):
    SINGLE_NEIGHBOUR = 'SingleNeighbour'
    SINGLE_SWAP = 'SingleSwap'
    CHAIN = 'Chain'
    
class SelectionAlgorithmEnum(Enum):
    ROULETTE_WHEEL = 'RouletteWheel'
    TOURNAMENT = 'Tournament'
    RANK = 'Rank'

class CrossoverSchemeEnum(Enum):
    ONE_POINT = 'OnePoint'
    TWO_POINT = 'TwoPoint'
    UNIFORM = 'Uniform'


class MyGeneticAlgorithm:    
    #####--Selection Algorithms---#####
    def roulette_wheel_selection(self, population, fitness):
        total_fitness = sum(fitness)
        probabilities = [f/total_fitness for f in fitness]
        cumulative_probabilities = [sum(probabilities[:i+1]) for i in range(len(probabilities))]

        selected_individuals = []
        for i in range(2):
            number = random.uniform(0, 1)
            for j in range(len(population)-1):
                if cumulative_probabilities[j] < number <= cumulative_probabilities[j+1]:
                    selected_individuals.append(population[j+1])
                    break
            if i == len(selected_individuals):
                selected_individuals.append(population[0])

        return selected_individuals


    def rank_selection(self, population, fitness):
        total_fitness = sum(fitness)
        probabilities = [f/total_fitness for f in fitness]
        cumulative_probabilities = [sum(probabilities[:i+1]) for i in range(len(probabilities))]

        selected_individuals = []
        for i in range(2):
            number = random.uniform(0, 1)
            for j in range(len(population)-1):
                if cumulative_probabilities[j] < number <= cumulative_probabilities[j+1]:
                    selected_individuals.append(population[j+1])
                    break
            if i == len(selected_individuals):
                selected_individuals.append(population[0])

        return selected_individuals
    
    def tournament_selection(self, population, fitness):
        selected_individuals = []
        for i in range(2):
            tournament_size = 5
            tournament_population = random.sample(population, tournament_size)
            tournament_fitness = [fitness[population.index(individual)] for individual in tournament_population]
            selected_individuals.append(tournament_population[tournament_fitness.index(max(tournament_fitness))])
        return selected_individuals
    
    selection_Algorithms = {
        SelectionAlgorithmEnum.ROULETTE_WHEEL: roulette_wheel_selection,
        SelectionAlgorithmEnum.RANK: rank_selection,
        SelectionAlgorithmEnum.TOURNAMENT: tournament_selection
    }
    ####################################
    
    #####----Crossover Schemes-----#####
    def one_point_crossover(self, pair):
        chromosome1, chromosome2 = pair
        length = len(chromosome1)
        cut_point = random.randint(1, length - 1)
        new_chromosome1 = chromosome1[:cut_point] + [item for item in chromosome2 if item not in chromosome1[:cut_point]]
        new_chromosome2 = chromosome2[:cut_point] + [item for item in chromosome1 if item not in chromosome2[:cut_point]]
        return [new_chromosome1, new_chromosome2]

    def two_point_crossover(self, pair):
        chromosome1, chromosome2 = pair
        length = len(chromosome1)
        cut_point1 = random.randint(1, length - 3)
        cut_point2 = random.randint(cut_point1 + 1, length - 1)
        new_chromosome1 = chromosome1[:cut_point1] + [item for item in chromosome2 if item not in chromosome1[:cut_point1] and item not in chromosome1[cut_point2:]] + chromosome1[cut_point2:]
        new_chromosome2 = chromosome2[:cut_point1] + [item for item in chromosome1 if item not in chromosome2[:cut_point1] and item not in chromosome2[cut_point2:]] + chromosome2[cut_point2:]
        return [new_chromosome1, new_chromosome2]
        

    def uniform_crossover(self, pair):
        chromosome1, chromosome2 = pair
        length = len(chromosome1)
        new_chromosome1 = []
        new_chromosome2 = []
        for i in range(length):
            if random.uniform(0, 1) < 0.5:
                new_chromosome1.append(next(item for item in chromosome1 if item not in new_chromosome1))
                new_chromosome2.append(next(item for item in chromosome2 if item not in new_chromosome2))
            else:
                new_chromosome1.append(next(item for item in chromosome2 if item not in new_chromosome1))
                new_chromosome2.append(next(item for item in chromosome1 if item not in new_chromosome2))
        return [new_chromosome1, new_chromosome2]

        
    crossover_schemes = {
        CrossoverSchemeEnum.ONE_POINT: one_point_crossover,
        CrossoverSchemeEnum.TWO_POINT: two_point_crossover,
        CrossoverSchemeEnum.UNIFORM: uniform_crossover
    }
    ####################################

    #####----Mutation Functions----#####
    def single_neighbour_mutation(self, pair, mutation_rate):
        for individual in pair:
            if random.uniform(0, 1) < mutation_rate:
                mutation_point = random.randint(1, len(individual)-1)
                individual[mutation_point], individual[mutation_point - 1] = individual[mutation_point - 1], individual[mutation_point]
        return pair
    
    def single_swap_mutation(self, pair, mutation_rate):
        for individual in pair:
            if random.uniform(0, 1) < mutation_rate:
                mutation_point1 = random.randint(1, len(individual)-1)
                mutation_point2 = random.randint(mutation_point1, len(individual)-1)
                individual[mutation_point1], individual[mutation_point2] = individual[mutation_point2], individual[mutation_point1]
        return pair
    
    def chain_mutation(self, pair, mutation_rate):
        for individual in pair:
            for mutation_point in range(1, len(individual)-1):
                if random.uniform(0, 1) < mutation_rate:
                    individual[mutation_point], individual[mutation_point - 1] = individual[mutation_point - 1], individual[mutation_point]
        return pair   

    mutation_methods = {
        MutationMethodEnum.SINGLE_NEIGHBOUR: single_neighbour_mutation,
        MutationMethodEnum.SINGLE_SWAP: single_swap_mutation,
        MutationMethodEnum.CHAIN: chain_mutation
    }
    ####################################

    #####-----Fitness Function-----#####
    fitness_function = lambda self, distance: 1/distance
    ####################################

    #####-------Selections---------#####
    selected_algorithm = None
    selected_crossover = None
    selected_mutation = None
    ####################################

    #####------Return values------#####
    optimal_fitness = None
    optimal_chromosome = []
    tsp = None
    ####################################

    def __init__(self,selection_algorithm, crossover_scheme, mutation_method):
        self.selected_algorithm = self.selection_Algorithms[selection_algorithm]
        self.selected_crossover = self.crossover_schemes[crossover_scheme]
        self.selected_mutation = self.mutation_methods[mutation_method]

    def run(self, tsp, population, generations, mutation_rate, elitism_rate = 0):
        self.optimal_fitness = 0
        self.optimal_chromosome = []
        self.tsp = tsp
        ga_logs = {"Test": tsp.get_name(),
                   "Config": {"SelectionAlgorithm": self.selected_algorithm.__name__, "CrossoverScheme": self.selected_crossover.__name__, "MutationMethod": self.selected_mutation.__name__},
                   "Args": {"Population": population, "Generations": generations, "MutationRate": mutation_rate, "ElitismRate": elitism_rate},
                   "Evolution": [],
                   "BestResult": {"Fitness": 0, "Chromosome": [], "Distance": 0}
                }
        #Initialize population P
        p = self.Initialize_population(population)
        #Evaluate fitness of all individuals in P
        fitness = self.evaluateFitness(p)
        #For each generation
        for i in range(generations):
            p_d = []                                        #P' = {}
            #For each pair in Population
            for _ in range(int(population/2)):
                #Selection: Select two individuals (c1, c2) from P
                pair = self.selected_algorithm(self, p, fitness)
                #Crossover: (c'1, c'2) <- crossover of (c1, c2)
                pair_d = self.selected_crossover(self, pair)
                #Mutation: Mutate individuals (c'1, c'2)
                pair_d = self.selected_mutation(self, pair_d, mutation_rate)
                #P' <- P' U {c'1, c'2}
                p_d.extend(pair_d)
            #Elitism: add best fitted individuals of P to P'
            if int(population * elitism_rate) > 0:
                p.sort(key=lambda x: self.tsp.get_total_distance(x))
                p_d.extend(p[:int(population * elitism_rate)])
            #P <- P'
            p = p_d
            #Evaluate fitness of all individuals in P
            fitness = self.evaluateFitness(p)
            ga_logs["Evolution"].append({"Generation":str(i), "Fitness":str(round(max(fitness), 6)), "Chromosome":str(p[fitness.index(max(fitness))]),"Distance":str(self.tsp.get_total_distance(p[fitness.index(max(fitness))]))})
            #Update optimal fitness and chromosome
            if max(fitness) > self.optimal_fitness: 
                self.optimal_fitness = max(fitness)
                self.optimal_chromosome = p[fitness.index(max(fitness))]
        #Return best individual in P
        ga_logs["BestResult"]["Fitness"] = self.optimal_fitness
        ga_logs["BestResult"]["Chromosome"] = self.optimal_chromosome
        ga_logs["BestResult"]["Distance"] = tsp.get_total_distance(self.optimal_chromosome)
        return ga_logs



    def Initialize_population(self, population): 
        # Generate random individuals and add them to the population
        p = []
        for _ in range(population):
            individual = list(range(1, self.tsp.get_nodes() + 1))
            p.append(random.sample(individual, len(individual)))
        return p

    def evaluateFitness(self, p):
        fitness = []
        for individual in p:
            fitness.append(self.fitness_function(self.tsp.get_total_distance(individual)))
        return fitness
