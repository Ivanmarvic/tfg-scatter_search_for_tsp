from abc import ABC, abstractmethod
from typing import List 
from ScatterSearchTSP.tsp_types import Tour

class CombinationMethod(ABC):
    @abstractmethod
    def combinate(self, subset:List[Tour]) -> Tour:
        pass

class NaiveTSPCombination(CombinationMethod):
    def combinate(self, subset:List[Tour]) -> Tour:
        def round_inc(j, dimension):
            if j == dimension - 1:
                    j = 0
            else:
                j = j+1 
            return j
        dimension = len(subset[0])
        n_solutions = len(subset)
        combined_solution = []
        # append first edge from first solution 
        combined_solution.append(subset[0][0])
        combined_solution.append(subset[0][1])
        for i in range(1,dimension-1):
            node = combined_solution[i]
            l = subset[i%n_solutions]
            j = l.index(node)
            j = round_inc(j,dimension)

            while l[j] in combined_solution:
                j = round_inc(j,dimension)
                print(j)

            combined_solution.append(l[j])
        return tuple(combined_solution)










                
