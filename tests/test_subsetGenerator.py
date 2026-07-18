import pytest 
from ScatterSearchTSP import subsetGenerator
import math

TEST_CASES = [ 
              (( (1,2), ), ( (2,1), )),

              (( (1,2,3), (3,2,1) ), ( (2,1,3), )),
              ]
@pytest.mark.parametrize("b, d", TEST_CASES)
def test_SimpleGenerator(b,d):
    print(b)

    generator = subsetGenerator.SimpleSubsetGenerator()
    subsets = generator.generateSubsets(b,d)
    assert len(subsets) == math.comb(len(b) + len(d), 2)
