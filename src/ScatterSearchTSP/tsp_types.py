from typing import Tuple, NamedTuple, Collection
import tsplib95 as tsplib
from pathlib import Path

type Tour = Tuple[int, ...]
class FitTour(NamedTuple):
    fitness: int
    tour: Tour


class TSP():
    def __init__(self, tsplib95_problem:tsplib.models.StandardProblem) -> None:
        self._tsp95problem = tsplib95_problem 
        self.node_coords = {}
        self.dimension = int(tsplib95_problem.dimension)
        self.edge_weight_type = tsplib95_problem.edge_weight_type
        # we work with 0 index in the future we will have to adapt to the convention 1-index
        for i, coords in tsplib95_problem.node_coords.items():
            self.node_coords[i-1] = tuple(coords)
    def trace_tours(self, tours:Collection[Tour]):
        in_tours = list()
        for t in tours:
            tour_list = list(t)
            for i in range(len(t)):
                tour_list[i] += 1
            in_tours.append(tour_list)
        return self._tsp95problem.trace_tours(in_tours)
    @staticmethod
    def load(filepath:str ):
        print(filepath)
        problem_95 = tsplib.load(filepath)
        problem = TSP(problem_95)
        assert problem.dimension > 0
        return problem


