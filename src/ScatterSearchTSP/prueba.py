import tsplib95 as tsplib
from importlib import resources

tsp_path = resources.files("tsp_instances").joinpath("berlin52.tsp")

problem = tsplib.load_problem(tsp_path)
print(problem)
tour = list(range(52))
for i in range(len(tour)):
    tour[i] += 1

print(problem.trace_tours([tuple(tour)]))
