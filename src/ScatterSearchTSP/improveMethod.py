from abc import ABC, abstractmethod
import os
from typing import Dict
import warnings
from ScatterSearchTSP.tsp_types import Tour, TSP
from pyCombinatorial.utils import util as py_util
from pyCombinatorial.algorithm import lin_kernighan_helsgaun
import numpy as np
import lkh
import pathlib
import tempfile

class ImproveMethod(ABC):
    @abstractmethod 
    def improve(self, solution:Tour) -> Tour:
        pass

class LKImprove(ImproveMethod):
    def __init__(self, problem:TSP) -> None:
        self.problem = problem
        coordinates = [self.problem.node_coords[i] for i in range(self.problem.dimension)]
        coordinates = np.array(coordinates, dtype=float)
        self._distance_matrix = py_util.build_distance_matrix(coordinates)

    def improve(self, solution:Tour) -> Tour:
        solution_base_1 = [node + 1 for node in solution] 
        city_tour = [solution_base_1, self.problem.trace_tours([solution])[0]]
        parameters = {
               'city_tour': city_tour,
               'initial_location': -1,
               'candidate_size': 5,
               'alpha_candidates': False,
               'ascent_iterations': 0,
               'max_depth': 4,
               'breadth':3,
               'patching': True,
               'patching_trials': 2,
               'restarts': 0,
               'kicks': 0,
               'three_opt': True,
               'three_opt_trials': 5,
               'max_passes': 3,
               'elite_candidates': False,
               'seed': None,
               'use_dont_look_bits': True,
               'verbose': False,
             }
        route, _ = lin_kernighan_helsgaun(self._distance_matrix, **parameters)
        route_base_0 = [int(node) - 1 for node in route]
        return Tour(route_base_0[:self.problem.dimension])


PROYECT_ROOT = pathlib.Path(__file__).parent.parent.parent 
class LKHImprove(ImproveMethod):
    DEFAULT_PARAMS:Dict[str, int | str] = {
            'RUNS': 1,                     
            'MAX_TRIALS': 1,                
            'KICKS': 0,                      # Sin perturbaciones
            'MOVE_TYPE': 5,                  # 5-opt
            'TRACE_LEVEL': 0,                 # Silencioso
            'MAX_CANDIDATES': 5,
            }
    def __init__(self, problem:TSP, params = None) -> None:
        self.problem = problem
        self.params = self.DEFAULT_PARAMS.copy()
        coordinates = [self.problem.node_coords[i] for i in range(self.problem.dimension)]
        coordinates = np.array(coordinates, dtype=float)
        if params is not None:
            self.params.update(params)

    def improve(self, solution: Tour) -> Tour:
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".tour", delete=False) as tour_f:
            tour_path = tour_f.name
            tour_f.write("NAME : InitialTour\n")
            tour_f.write("TYPE : TOUR\n")
            tour_f.write(f"DIMENSION : {self.problem.dimension}\n")
            tour_f.write("TOUR_SECTION\n")
            for node in solution:
                tour_f.write(f"{node + 1}\n") 
            tour_f.write("-1\n")
            tour_f.write("EOF\n")
        self.params["INITIAL_TOUR_FILE"] = tour_path

        try:
            solver_path = PROYECT_ROOT / "lib" / "LKH-3.0.6" / "LKH"
            routes = lkh.solve(str(solver_path), problem=self.problem._tsp95problem, **self.params)
            route_base_0 = []
            for node in routes[0]:
                route_base_0.append(node - 1)
        finally:
            if os.path.exists(tour_path):
                os.remove(tour_path)
        return Tour(route_base_0[:self.problem.dimension])
    




def do_intersect(seg1, seg2):
    """ Check if two line segments intersect using orientation test. """
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        return 0 if val == 0 else (1 if val > 0 else -1)
    
    p1, q1 = seg1
    p2, q2 = seg2
    
    # if the segments have a point in common they do not intersect (for this application)
    if(p1 == p2 or q1 == q2 or p1 == q2 or p2 == q1):
        return False
    
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    return o1 != o2 and o3 != o4

# O(n^2) with early exit
def find_first_intersection(segments):
    for i in range(len(segments)):
        for j in range(len(segments)):
            if do_intersect(segments[i], segments[j]):
                return(segments[i], segments[j])
    return None

# this improve method is only valid if the distance has triange inequality property i.e. Euclidean-Distance like
class CrossEliminate(ImproveMethod):
    def __init__(self, problem:TSP) -> None:
        if(problem.edge_weight_type not in {"EUC_2D", "GEO"}):
            warnings.warn(message=f"CrossEliminate does not support {problem.edge_weight_type}", category=UserWarning)
        self.problem = problem

    def improve(self, solution:Tour) -> Tour:

        if(self.problem.edge_weight_type != "EUC_2D"):
            warnings.warn(message=f"CrossEliminate does not support {self.problem.edge_weight_type} unexpected behavior may happen ", category=UserWarning)
            # return solution

        new_sol = list(solution)
        improved = True
        while improved:
            seg_edges = []
            edge_pos = {}
            for i in range(self.problem.dimension):
                curr = new_sol[i]
                if i < self.problem.dimension - 1:
                    next = new_sol[i+1]
                else:
                    next = new_sol[0]
                p1 = self.problem.node_coords[curr]
                p2 = self.problem.node_coords[next]
                if p1 > p2 : 
                    p1, p2 = p2, p1
                seg = (p1, p2)
                seg_edges.append(seg)
                edge_pos[seg] = i

            inter = find_first_intersection(seg_edges)
            if inter:
                idx_a = edge_pos[inter[0]]
                idx_b = edge_pos[inter[1]]
                i = min(idx_a, idx_b)
                j = max(idx_a, idx_b)
                new_sol[i+1], new_sol[j] = new_sol[j], new_sol[i+1]
                assert i + 2 <= j
                new_sol[i+2:j] = list(reversed(new_sol[i+2:j]))
            else:
                improved = False

        return Tour(new_sol)





