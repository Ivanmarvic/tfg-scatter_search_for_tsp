import pytest 
from ScatterSearchTSP import combinationMethod

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


    
