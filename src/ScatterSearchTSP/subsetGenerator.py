from abc import ABC, abstractmethod
from typing import Collection, Tuple, Set
from ScatterSearchTSP.tsp_types import Tour 
import itertools

class subsetGenerator(ABC):
    @abstractmethod 
    def generateSubsets(self, b:Collection[Tour],d:Collection[Tour]) -> Collection[Collection[Tour]]:
        pass
    @abstractmethod
    def reset(self) -> None:
        pass
class SimpleSubsetGenerator(subsetGenerator):
    def __init__(self) -> None:
        self._generated = set()
        pass
    def generateSubsets(self, b:Collection[Tour],d:Collection[Tour]) -> Collection[Collection[Tour]]:
        subsets = set()
        subsets = subsets.union(set(itertools.combinations(b,2)))
        subsets = subsets.union(set(itertools.combinations(d,2)))
        subsets = subsets.union(set(itertools.product(b,d)))
        new_sets = subsets - self._generated 
        self._generated = self._generated.union(new_sets)
        return new_sets
    def reset(self) -> None:
        self._generated = set()
