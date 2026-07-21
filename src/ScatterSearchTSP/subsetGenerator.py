from abc import ABC, abstractmethod
from typing import Collection, Tuple, Set
from ScatterSearchTSP.tsp_types import Tour 
import itertools

class subsetGenerator(ABC):
    @abstractmethod 
    def generateSubsets(self, b:Collection[Tour],d:Collection[Tour]) -> Collection[Collection[Tour]]:
        pass
class SimpleSubsetGenerator(subsetGenerator):
    def __init__(self) -> None:
        pass
    def generateSubsets(self, b:Collection[Tour],d:Collection[Tour]) -> Collection[Collection[Tour]]:
        subsets = set()
        subsets = subsets.union(set(itertools.combinations(b,2)))
        subsets = subsets.union(set(itertools.combinations(d,2)))
        subsets = subsets.union(set(itertools.product(b,d)))
        return subsets
