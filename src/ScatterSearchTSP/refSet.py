from abc import ABC, abstractmethod
from typing import Callable, List, Set, NamedTuple, List, Tuple
import warnings 
import ScatterSearchTSP.utils as utils
from ScatterSearchTSP.tsp_types import Tour, FitTour
import itertools




class RefSetTSP(ABC):
    @abstractmethod
    def update(self, tours:List[FitTour]) -> bool:
        pass

    @abstractmethod
    def set(self, tours: List[FitTour]) -> int:
        pass
    @property
    @abstractmethod
    def d_set(self) -> Set[Tour]:
        pass
    @property
    @abstractmethod
    def b_set(self) -> Set[Tour]:
        pass
    @property
    @abstractmethod 
    def best_solution(self) -> FitTour:
        pass
    @property
    @abstractmethod 
    def last_inserted_indices(self) -> List[int]:
        pass


class DTour(NamedTuple):
    diversity: int
    fitness: int
    tour: Tour

class RefSetFixedDiversity(RefSetTSP):
    def __init__(self, distance_fn:Callable[[Tour, Tour], int], d_size, b_size) -> None:

        self.d_size = d_size
        self.b_size = b_size
        # first b_size position for best solutions and last d_size positions for diversity solutions
        self._refList:List[FitTour] = list() 
        self.distance_fn = distance_fn
        self._l_inserted = [] 

    def set(self, tours: List[FitTour]) -> int:
        if len(tours) < self.d_size + self.b_size: 
            warnings.warn(
                    message=f"RefSet set method called with few solutions, either reduce refSet b_size and d_size or get more solutions from diversificator",
                    category=UserWarning)

        tours.sort(key=lambda x: x.fitness)
        self._refList = tours[0: self.b_size]
        d_candidates = tours[self.b_size:]
        for _ in range(self.d_size):
            max_min_d = None
            max_min_idx = None
            for j in range(len(d_candidates)):
                curr_d = utils.min_set_distance(d_candidates[j],self._refList, lambda x,y: self.distance_fn(x.tour, y.tour))
                if max_min_d is None or max_min_d < curr_d:
                    max_min_d = curr_d
                    max_min_idx = j

            assert max_min_d is not None and max_min_idx is not None
            new_tour = d_candidates[max_min_idx]
            self._refList.append(new_tour)
            del d_candidates[max_min_idx]
        return len(self._refList)

    @property
    def last_inserted_indices(self) -> List[int]:
        return self._l_inserted

    def update(self, tours:List[FitTour]) -> bool:

        assert self._refList is not None 
        assert len(self._refList) > 0
        b_size = self.b_size 
        current_b = self._refList[:b_size]
        ref_set = set(self._refList)
        new_tours = list()
        for t in tours:
            if t not in ref_set:
                new_tours.append(t)

        combined_tours = new_tours + current_b
        combined_tours.sort(key=lambda x: x.fitness)
        new_b = combined_tours[0:self.b_size]
        ref_new_index:List[int] = []
        for tour in new_b:
            if tour in new_tours:
                ref_new_index.append(new_b.index(tour)) 
        self._l_inserted = ref_new_index 
        self._refList[0:b_size] = new_b
        return len(ref_new_index) > 0

    @property
    def d_set(self) -> Set[Tour]:
        d_set = set()
        for d in self._refList[self.b_size:]:
            d_set.add(d.tour)
        return d_set

    @property
    def b_set(self) -> Set[Tour]:
        b_set = set()
        for b in self._refList[0:self.b_size]:
            b_set.add(b.tour)
        return b_set
    
    @property
    def best_solution(self) -> FitTour:
        return self._refList[0]

            

        


