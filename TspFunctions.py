import tsplib95

class TspFunctions:
    
    problem = None

    def __init__(self, filepath):
        self.problem = tsplib95.load(filepath)

    def get_nodes(self):
        return self.problem.dimension
    
    def get_distance(self, start, end):
        return self.problem.get_weight(start, end)

    def get_graph(self):
        return self.problem.get_graph()

    def get_problem_as_dict(self):
        return self.problem.as_dict()
    
    def save_results(self):
        self.problem.save('results/' + self.problem.name + '.opt.tour', name='optimal_tour')


