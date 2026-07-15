import pytest
import tsplib95 as tsplib
from ScatterSearchTSP import improveMethod
from ScatterSearchTSP.tsp_types import TSP
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
def test_LKImprove():
    ppath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  "berlin52.tsp"
    problem = tsplib.load(ppath)
    improver = improveMethod.LKImprove(problem)
    initial_sol = tuple(range(int(problem.dimension)))
    sol = improver.improve(initial_sol)
    assert sol != initial_sol

TEST_CASES = [
        "berlin52.tsp"
        ]
@pytest.mark.parametrize("problem_instance", TEST_CASES)
def test_CrossEliminate(problem_instance):
    ppath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  problem_instance
    problem = TSP.load(str(ppath))
    improver = improveMethod.CrossEliminate(problem)
    initial_sol = tuple(range(problem.dimension))
    assert problem.dimension > 0
    sol = improver.improve(initial_sol)
    assert sol != initial_sol
    costs = problem.trace_tours([initial_sol, sol])
    assert costs[1]< costs[0]
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


