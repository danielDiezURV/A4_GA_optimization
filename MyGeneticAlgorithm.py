from enum import Enum

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
    def roulette_wheel_selection(self):
        pass

    selection_Algorithms = {
        SelectionAlgorithmEnum.ROULETTE_WHEEL: roulette_wheel_selection,
        #SelectionAlgorithmEnum.TOURNAMENT: tournament_selection,
        #SelectionAlgorithmEnum.RANK: rank_selection
    }
    ####################################
    
    #####----Crossover Schemes-----#####
    def one_point_crossover(self):
        pass

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
    ####################################
    
    def __init__(self,fitness_function, selection_algorithm, crossover_scheme):
        optimal_fitness = None
        optimal_chromosome = []
        self.selected_fitness = self.fitness_functions(fitness_function)
        self.selected_algorithm = self.selection_Algorithms(selection_algorithm)
        self.selected_crossover = self.crossover_schemes(crossover_scheme)

    def run(self, graph, population, generations, mutation_rate, has_elitism):
        #Initialize population P
        #Evaluate fitness of all individuals in P
        #For each generation
            #P' = 0
            #For each pair in Population
                #Selection: Select two individuals (c1, c2) from P
                #Crossover: (c'1, c'2) <- crossover of (c1, c2)
                #Mutation: Mutate individuals (c'1, c'2)
                #P' <- P' U {c'1, c'2}
            #Elitism: add best fitted individuals of P to P'
            #P <- P'
            #Evaluate fitness of all individuals in P
        pass

