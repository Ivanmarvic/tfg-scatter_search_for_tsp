from ScatterSearchTSP import subrutines
import pytest

TEST_CASES = [
        {"size":10, "instances":5}
        ]
@pytest.mark.parametrize("input_fun", TEST_CASES)
def test_randomDiversification(input_fun):
    generator = subrutines.TSPRandomDiversification(problem_size=input_fun["size"], 
                                                    number_of_problem_instances=input_fun["instances"])
    out = generator.diversificate()
    assert len(out) == input_fun["instances"] 
    for instance in out:
        assert len(instance) == input_fun["size"]
