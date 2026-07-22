from ScatterSearchTSP import diversification
from ScatterSearchTSP import utils
import pytest

TEST_CASES = [
        {"size":10, "instances":5}
        ]
@pytest.mark.parametrize("input_fun", TEST_CASES)
def test_randomDiversification(input_fun):
    generator = diversification.TSPRandomDiversification(problem_size=input_fun["size"], 
                                                    number_of_problem_instances=input_fun["instances"])
    out = generator.diversificate()
    assert len(out) == input_fun["instances"] 
    for instance in out:
        assert len(instance) == input_fun["size"]

TEST_CASES = [
        ({"n":14, "h":4,  "s":3}, [3, 7, 11]),
        ({"n":14, "h":4,  "s":2}, [2, 6, 10]),
        ({"n":14, "h":4,  "s":1}, [1, 5, 9, 13]),
        ({"n":14, "h":4,  "s":0}, [0, 4, 8, 12]),
        ]
@pytest.mark.parametrize("input_data, expected_out", TEST_CASES)
def test_ilustrativeSubPerm(input_data, expected_out):
    generator = diversification.IlustrativeTSPDiversification(problem_size=input_data["n"])
    res = generator._sub_permutation(h=input_data["h"],s=input_data["s"])
    assert res == expected_out

TEST_CASES = [
        {"size":10, "instances":10}
        ]
@pytest.mark.parametrize("input_data", TEST_CASES)
def test_ilustrativeDiversification(input_data):
    generator = diversification.IlustrativeTSPDiversification(problem_size=input_data["size"])
    out = generator.diversificate()

    # with canonical tour we cannot assure to match a given number of instances
    # assert len(out) == input_data["instances"] 
    for instance in out:
        assert len(instance) == input_data["size"]
        for i in range(input_data["size"]):
            assert i in instance

TEST_CASES = [
        ({"n": 3, "k": 5}, [2,1,0]),
        ({"n": 7, "k": 2982}, [4,0,6,2,1,3,5]),
        ]

@pytest.mark.parametrize("input_data, expected_out", TEST_CASES)
def test_lehmerPermutation(input_data, expected_out):
    a = list(range(input_data["n"]))
    res = diversification.lehmer_Permutation(k=input_data["k"],original_array=a)
    assert res == expected_out
    
TEST_CASES = [
        {"size":10, "instances":100}
        ]

@pytest.mark.parametrize("input_data", TEST_CASES)
def test_lehmerDiversificator(input_data):
    generator = diversification.TSPLehmerDiversificator(problem_size=input_data["size"], 
                                                  number_of_problem_instances=input_data["instances"])
    out = generator.diversificate()
    assert len(out) == input_data["instances"] 
    non_repeated = set()
    for instance in out:
        non_repeated.add(tuple(instance))
        assert len(instance) == input_data["size"]
    assert len(non_repeated) == len(out)

