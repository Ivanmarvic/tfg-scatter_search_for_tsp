from abc import ABC, abstractmethod
import warnings
from ScatterSearchTSP.tsp_types import Tour, TSP
import heapq
from sortedcontainers import SortedList

class ImproveMethod(ABC):
    @abstractmethod 
    def improve(self, solution:Tour) -> Tour:
        pass

class LKImprove():
    def __init__(self, problem) -> None:
        self.problem = problem

    def improve(self, solution:Tour) -> Tour:
        return solution



#sweep_line_intersection implementation from  https://dmj.one/edu/su/course/csu083/theory/sweep-line-algorithm
class Event:
    def __init__(self, x, segment, is_start):
        self.x = x
        self.segment = segment
        self.is_start = is_start
    
    def __lt__(self, other):
        return self.x < other.x  # Sorting events by x-coordinate

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

def sweep_line_intersection(segments):
    """ Detect intersections using Sweep Line Algorithm. """
    events = []
    for seg in segments:
        events.append(Event(seg[0][0], seg, True))  # Start event
        events.append(Event(seg[1][0], seg, False)) # End event
    events.sort()  # Sorting events by x-coordinate
    active_segments = SortedList(key=lambda seg: seg[0][1])  # Sort by y-coordinate
    intersections = []
    edges_idx = []

    for event in events:
        seg = event.segment
        if event.is_start:
            idx = active_segments.bisect(seg)
            if idx > 0 and do_intersect(active_segments[idx - 1], seg):
                intersections.append((active_segments[idx - 1], seg))
            if idx < len(active_segments) and do_intersect(active_segments[idx], seg):
                intersections.append((active_segments[idx], seg))
            active_segments.add(seg)
        else:
            idx = active_segments.index(seg)
            if 0 < idx < len(active_segments) - 1 and do_intersect(active_segments[idx - 1], active_segments[idx + 1]):
                intersections.append((active_segments[idx - 1], active_segments[idx + 1]))
                edges_idx.append((idx - 1, idx + 1))
            active_segments.remove(seg)

    return intersections 

# this improve method is only valid if the distance has triange inequality property i.e. Euclidean-Distance like
class CrossEliminate(ImproveMethod):
    def __init__(self, problem:TSP) -> None:
        if(problem.edge_weight_type != "EUC_2D"):
            warnings.warn(message=f"CrossEliminate does not support {problem.edge_weight_type}", category=UserWarning)
        self.problem = problem

    def improve(self, solution:Tour) -> Tour:

        if(self.problem.edge_weight_type != "EUC_2D"):
            warnings.warn(message=f"CrossEliminate does not support {self.problem.edge_weight_type}, aborting improve", category=UserWarning)
            return solution

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
                seg = (tuple(p1), tuple(p2))
                seg_edges.append(seg)
                edge_pos[seg] = i

            intersections = sweep_line_intersection(seg_edges)
            # print(f"intersections: {intersections}")
            # print(f"positions: {edge_pos}")
            if len(intersections) > 0:
                inter = intersections[0]
                idx_a = edge_pos[inter[0]]
                idx_b = edge_pos[inter[1]]
                i = min(idx_a, idx_b)
                j = max(idx_a, idx_b)
                print(f" i: {i} j: {j}")
                new_sol[i+1], new_sol[j] = new_sol[j], new_sol[i+1]
                assert i + 2 <= j
                new_sol[i+2:j] = list(reversed(new_sol[i+2:j]))
            else:
                improved = False

        return tuple(new_sol)





