from abc import ABC, abstractmethod
from typing import List, NamedTuple
from dataclasses import dataclass
from ScatterSearchTSP.tsp_types import Tour, TSP

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

            combined_solution.append(l[j])
        return Tour(combined_solution)


@dataclass(slots=True)
class EdgeScore():
    score: float 
    start: int 
    end: int 

class ConvexTSPCombination(CombinationMethod):
    def __init__(self, problem:TSP) -> None:
        self._problem = problem
        super().__init__()

    def combinate(self, subset: List[Tour]) -> Tour:
        lambdas = []
        dimension = len(subset[0])
        total_costs = self._problem.trace_tours(subset)
        inverse_sum = 0 
        for i in range(len(subset)):
            inverse_sum += 1/total_costs[i]

        for i in range(len(subset)):
            lambda_t = (1/total_costs[i])/inverse_sum
            lambdas.append(lambda_t)

        scored_edges: List[EdgeScore] = []
        added_edges = []

        for i, solution in enumerate(subset):
            for j in range(len(solution)):
                start = solution[j]
                if j == len(solution) - 1:
                    end = solution[0]
                else:
                    end = solution[j+1]
                #normalized edges 2 -> 1 is 1 -> 2
                if start > end:
                    start, end = end, start

                edge = (start, end)
                if edge in added_edges: 
                    k = added_edges.index(edge) 
                    scored_edges[k].score += lambdas[i]
                else: 
                    added_edges.append(edge) 
                    scored = EdgeScore(lambdas[i], start, end)
                    scored_edges.append(scored)

        visited = set()
        ady = [ [] for _ in range(dimension)]
        def node_grad(node):
            return len(ady[node])
        def node_connect(start, end):
            ady[start].append(end)
            ady[end].append(start)

        scored_edges.sort(key= lambda e: e.score, reverse=True)

        #Hamiltonial path creation with priority to the scored_edges
        for e in scored_edges: 
            if ((node_grad(e.start) < 1 and node_grad(e.end) < 2) or 
            (node_grad(e.start) < 2 and node_grad(e.end) < 1) or
            (node_grad(e.start) == 1 and node_grad(e.end) == 1 and len(visited) == dimension ) ):
                node_connect(e.start,e.end)
                visited.add(e.start)
                visited.add(e.end)

        grade_0_nodes = []
        grade_1_nodes = []
        for i, node in enumerate(ady):
            if node_grad(i) == 1:
                grade_1_nodes.append(i)
            elif node_grad(i) == 0:
                grade_0_nodes.append(i) 

        #connect grade_1_nodes to grade_0_nodes 
        while len(grade_1_nodes) > 0:
            node_1 = grade_1_nodes.pop() 
            if len(grade_0_nodes) > 0:
                node_0 = grade_0_nodes.pop()
                grade_1_nodes.append(node_0)
            else:
                node_0 = grade_1_nodes.pop()
            node_connect(node_0, node_1)

        assert len(grade_0_nodes) == len(grade_1_nodes) == 0, "Error, some nodes are isolated, invalid tour"

        #Create the permutation from ady
        visited = set() 
        combined_solution = []
        for node in ady:
            for neighboar in node:
                if neighboar not in visited:
                    visited.add(neighboar)
                    combined_solution.append(neighboar)

        return Tour(combined_solution)







                
