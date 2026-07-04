import tsplib95 as tsplib
from importlib import resources
from abc import ABC, abstractmethod
from typing import Callable, List, Set, NamedTuple
import ScatterSearchTSP.utils as utils
from ScatterSearchTSP.tsp_types import Tour

# tsp_path = resources.files("tsp_instances").joinpath("berlin52.tsp")

# problem = tsplib.load_problem(tsp_path)
# print(problem)
# print(problem.trace_tours([tuple(range(52))]))
# print(problem.trace_canonical_tour())


class RefSetTSP(ABC):
    @abstractmethod
    def update(self, tour:Tour) -> bool:
        pass

    @abstractmethod
    def set(self, tours: Set[Tour]) -> int:
        pass
    @property
    @abstractmethod
    def d_set(self) -> Set[Tour]:
        pass
    @property
    @abstractmethod
    def b_set(self) -> Set[Tour]:
        pass

class BTour(NamedTuple):
    cost: int
    tour: Tour

class DTour(NamedTuple):
    diversity: int
    tour: Tour

class RefSetFixedDiversity(RefSetTSP):
    def __init__(self, fitness_fn: Callable[[Tour], int], 
                 distance_fn:Callable[[Tour, Tour], int], d_size, b_size) -> None:

        self.d_size = d_size
        self.b_size = b_size
        self._b:List[BTour] = list()
        self._d:List[DTour] = list()
        self.fitness_fn = fitness_fn
        self.distance_fn = distance_fn

    def set(self, tours: Set[Tour]) -> int:
        cost_tours: List[BTour] = list()
        for b in tours:
            cost = self.fitness_fn(b)
            cost_tours.append(BTour(cost, b))
        cost_tours.sort(key=lambda x: x.cost)
        self._b = cost_tours[0: self.b_size]

        d_candidates = set(tours)
        b_tours = set()
        
        for b in self._b:
            b_tours.add(b.tour)

        d_candidates = d_candidates - b_tours
        distance_tours:List[DTour] = list()
        for t in d_candidates:
            distance = utils.min_set_distance(t,b_tours, self.distance_fn)
            distance_tours.append(DTour(distance, t))
        distance_tours.sort(key=lambda x: x.diversity)
        self._d = distance_tours[0:self.d_size]
        return len(self._d) + len(self._b)

    def update(self, tour:Tour) -> bool:
        cost = self.fitness_fn(tour)

        if cost > self._b[-1].cost:
            return False

        i = self.b_size - 1
        while cost < self._b[i].cost and i >= 0:
            i -= 1
        self._b.insert(i+1, BTour(cost, tour))
        self._b.pop()
        return True

    @property
    def d_set(self) -> Set[Tour]:
        d_set = set()
        for d in self._d:
            d_set.add(d.tour)
        return d_set

    @property
    def b_set(self) -> Set[Tour]:
        b_set = set()
        for b in self._b:
            b_set.add(b.tour)
        return b_set

            

        


