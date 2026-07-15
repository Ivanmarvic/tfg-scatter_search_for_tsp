import pytest
import tsplib95 as tsplib
from ScatterSearchTSP import improveMethod
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
def test_LKImprove():
    ppath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  "berlin52.tsp"
    problem = tsplib.load(ppath)
    improver = improveMethod.LKImprove(problem)
    initial_sol = tuple(range(int(problem.dimension)))
    sol = improver.improve(initial_sol)
    assert sol != initial_sol
def test_CrossEliminate():
    ppath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  "berlin52.tsp"
    problem = tsplib.load(ppath)
    improver = improveMethod.CrossEliminate(problem)
    # problem.node_coords = list(map(lambda c: (int(c), int(c)) , problem.node_coords))
    # for i in range(1, int(problem.dimension) + 1):
    #     problem.node_coords[i][0] = int(problem.node_coords[i][0])
    #     problem.node_coords[i][1] = int(problem.node_coords[i][1])

    initial_sol = tuple(range(1,int(problem.dimension)+1))
    sol = improver.improve(initial_sol)
    assert sol != initial_sol
    print(sol)
    cost0 = problem.trace_tours([initial_sol])[0]
    cost1 = problem.trace_tours([sol])[0] 
    assert cost1 < cost0
    for i in initial_sol:
        assert i in sol



TEST_CASES = [
        {

        "segments": [
            ((1, 1), (5, 5)),
            ((2, 5), (6, 1)),
            ((3, 3), (7, 7)),
            ((1, 1), (2, 3)),
        ],
        "expected_intersections":[(((1, 1), (5, 5)), ((2, 5), (6, 1))), (((2, 5), (6, 1)), ((3, 3), (7, 7)))],
        "expected_indices":[(0,1),(1,2)],
        },

        ]
@pytest.mark.parametrize("test_case", TEST_CASES)
def test_sweepLine(test_case):
    intersections = improveMethod.sweep_line_intersection(test_case["segments"])
    print(intersections)
    assert intersections == test_case["expected_intersections"]


