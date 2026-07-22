from typing import Any, Callable, Collection
import warnings
from ScatterSearchTSP.tsp_types import Tour
from tsplib95.models import Problem


#assumes positive distances
def min_set_distance(element, distanceSet:Collection, distance_fn:Callable[[Any, Any], int]) -> int:
    assert len(distanceSet) > 0, "distance set is empty"
    min_distance = None
    for s in distanceSet:
        if min_distance == None or distance_fn(element, s) < min_distance:
            min_distance = distance_fn(element,s)

    assert min_distance is not None
    if min_distance == 0: 
        warnings.warn(message="min_distance is == 0, the element is in the set", category=UserWarning)
        
    if min_distance < 0: 
        warnings.warn(message="min_distance is < 0, working with negative distances", category=UserWarning)
        
    return min_distance

# this distance calculation is too Naive !!! 
def permutation_difference(tour1:Tour, tour2:Tour) -> int:
    assert len(tour1) == len(tour2), "error trying to compute a distance between tours with different length"
    distance = 0
    for i in range(len(tour1)):
        if tour1[i] != tour2[i]: distance += 1
    if distance == 0:
        warnings.warn(message="permutation difference == 0, comparing same permutation")

    return distance

def edge_difference(tour1:Tour, tour2: Tour) -> int:
    assert len(tour1) == len(tour2), "error trying to compute a distance between tours with different length"
    edges_1 = set() 
    edges_2 = set()
    for i in range(len(tour1)):
        start = tour1[i]
        if i == len(tour1) - 1:
            end = tour1[0]
        else:
            end = tour1[i + 1]
        if start > end:
            start, end = end, start
        edges_1.add((start,end))
    for i in range(len(tour2)):
        start = tour2[i]
        if i == len(tour2) - 1:
            end = tour2[0]
        else:
            end = tour2[i + 1]
        if start > end:
            start, end = end, start
        edges_2.add((start,end))

    return len(edges_1 - edges_2)



# change permutation 0 notation (0,1,2,3) to 1 notation (1,2,3,4) so that tsplib95 problem.trace_tours does not break
def trace_tours(problem:Problem, tours:Collection[Tour]) -> int:
    in_tours = list()
    for t in tours:
        tour_list = list(t)
        for i in range(len(t)):
            tour_list[i] += 1
        in_tours.append(tour_list)
    return problem.trace_tours(in_tours)









