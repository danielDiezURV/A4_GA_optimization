from enum import Enum
import random

class fitnessFunctionEnum(Enum):
    INVERSE_DISTANCE = 'inverseDistance'

class SelectionAlgorithmEnum(Enum):
    ROULETTE_WHEEL = 'RouletteWheel'
    TOURNAMENT = 'Tournament'
    RANK = 'Rank'
    SUS = 'StochasticUniversalSampling'

class CrossoverSchemeEnum(Enum):
    ONE_POINT = 'OnePoint'
    TWO_POINT = 'TwoPoint'
    UNIFORM = 'Uniform'


class MyGeneticAlgorithm:
    #####----Fitness Functions----#####
    fitness_functions = {fitnessFunctionEnum.INVERSE_DISTANCE : lambda x: 1/x}
    ####################################
    
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


    selection_Algorithms = {
        SelectionAlgorithmEnum.ROULETTE_WHEEL: roulette_wheel_selection,
        #SelectionAlgorithmEnum.TOURNAMENT: tournament_selection,
        #SelectionAlgorithmEnum.RANK: rank_selection
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

    crossover_schemes = {
        CrossoverSchemeEnum.ONE_POINT: one_point_crossover,
        #CrossoverSchemeEnum.TWO_POINT: two_point_crossover,
        #CrossoverSchemeEnum.UNIFORM: uniform_crossover
    }
    ####################################
        
    #####-------Selections---------#####
    selected_fitness = None
    selected_algorithm = None
    selected_crossover = None
    ####################################

    #####------Return values------#####
    optimal_fitness = None
    optimal_chromosome = []
    tsp = None
    ####################################

    def __init__(self,fitness_function, selection_algorithm, crossover_scheme):
        self.selected_fitness = self.fitness_functions[fitness_function]
        self.selected_algorithm = self.selection_Algorithms[selection_algorithm]
        self.selected_crossover = self.crossover_schemes[crossover_scheme]

    def run(self, tsp, population, generations, mutation_rate, elitism_rate = 0):
        self.optimal_fitness = 0
        self.optimal_chromosome = []
        self.tsp = tsp
        ga_logs = {"test": tsp.get_name(),
                   "args": {"population": population, "generations": generations, "mutation_rate": mutation_rate, "elitism_rate": elitism_rate},
                   "evolution": [],
                   "bestResult": {"fitness": 0, "chromosome": [], "distance": 0}
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
                pair_d = self.mutate_individuals(pair_d, mutation_rate)
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
            ga_logs["evolution"].append("[Generation: "+ str(i)+"] ---> fitness: "+ str(round(max(fitness), 6)) +" --- chromosome: " + str(p[fitness.index(max(fitness))]) +" --- distance: " + str(self.tsp.get_total_distance(p[fitness.index(max(fitness))])))
            #Update optimal fitness and chromosome
            if max(fitness) > self.optimal_fitness: 
                self.optimal_fitness = max(fitness)
                self.optimal_chromosome = p[fitness.index(max(fitness))]
        #Return best individual in P
        ga_logs["bestResult"]["fitness"] = self.optimal_fitness
        ga_logs["bestResult"]["chromosome"] = self.optimal_chromosome
        ga_logs["bestResult"]["distance"] = tsp.get_total_distance(self.optimal_chromosome)
        return ga_logs



    def Initialize_population(self, population): 
        # Initialize population P
        p = []
        # Generate random individuals and add them to the population
        for _ in range(population):
            individual = list(range(1, self.tsp.get_nodes() + 1))
            p.append(random.sample(individual, len(individual)))
        return p

    def evaluateFitness(self, p):
        fitness = []
        for individual in p:
            fitness.append(self.selected_fitness(self.tsp.get_total_distance(individual)))
        return fitness
    
    def mutate_individuals(self, pair, mutation_rate):
        for individual in pair:
            if random.uniform(0, 1) < mutation_rate:
                mutation_point = random.randint(1, len(individual)-1)
                individual[mutation_point], individual[mutation_point - 1] = individual[mutation_point - 1], individual[mutation_point]
        return pair