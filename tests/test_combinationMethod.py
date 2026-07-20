import pytest 
from ScatterSearchTSP import combinationMethod
from ScatterSearchTSP.tsp_types import TSP
import pathlib 

BASE_DIR = pathlib.Path(__file__).parent.parent
TEST_CASES = [ 
              ([(1,2,3,4), (4,3,2,1)], (1,2,4,3)),
              ([(1,2,3,4), (4,3,2,1), (3,2,4,1)], (1,2,4,3)),
              ([(1,2,3,4,5), (5,4,3,2,1), (5,3,2,4,1)], (1,2,5,3,4)),
              ]
@pytest.mark.parametrize("subset, expected", TEST_CASES)
def test_NaiveCombinationMethod(subset, expected):
    print(subset)
    combinator = combinationMethod.NaiveTSPCombination() 
    dimension = len(subset[0])
    solution = combinator.combinate(subset) 
    assert len(solution) == dimension 
    for i in subset[0]: 
        assert i in solution
    assert solution == expected


TEST_CASES = [ 
              ([(0,1,2,3,4), (3,2,1,0,4)], (1, 4, 0, 2, 3), "ulysses5.tsp"),
              ([(0,1,2,3,4), (3,2,4,1,0), (4,3,2,1,0)], (1, 4, 0, 2, 3), "ulysses5.tsp"),
              ([(0,4,2,3,1), (3,2,4,1,0), (1,3,2,4,0)], (1, 4, 0, 3, 2), "ulysses5.tsp"),
              ([(1,2,4,3,0), (1,2,4,0,3), (1,2,3,4,0)], (4, 1, 2, 0, 3), "ulysses5.tsp"),
              ]
@pytest.mark.parametrize("subset, expected, problem_str", TEST_CASES)
def test_ConvexTSPCombination(subset, expected, problem_str):
    print(subset)
    ppath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  problem_str
    problem = TSP.load(str(ppath))
    combinator = combinationMethod.ConvexTSPCombination(problem=problem) 
    dimension = len(subset[0])
    solution = combinator.combinate(subset) 
    assert len(solution) == dimension 
    for i in subset[0]: 
        assert i in solution
    assert solution == expected

    
