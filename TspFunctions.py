import tsplib95

class TspFunctions:

    problem = None

    def __init__(self, filepath):
        self.problem = tsplib95.load(filepath, special=tsplib95.models.StandardProblem)

    def get_nodes(self):
        return self.problem.dimension
    
    def get_distance(self, start, end):
        return abs(self.problem.get_weight(start, end))
    
    def get_total_distance(self, path):
        total_distance = sum(abs(self.get_distance(path[i], path[i + 1])) for i in range(0, len(path) -1))
        total_distance += abs(self.get_distance(path[-1], path[0]))
        return total_distance
    
    def get_name(self):
        return self.problem.name

    def get_graph(self):
        return self.problem.get_graph()

    def get_problem_as_dict(self):
        return self.problem.as_dict()
    
    def save_results(self):
        self.problem.save('results/' + self.problem.name + '.opt.tour', name='optimal_tour')


