from ScatterSearchTSP import subrutines
from ScatterSearchTSP import utils
import pytest
import math

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

TEST_CASES = [
        ({"n":14, "h":4,  "s":3}, [3, 7, 11]),
        ({"n":14, "h":4,  "s":2}, [2, 6, 10]),
        ({"n":14, "h":4,  "s":1}, [1, 5, 9, 13]),
        ({"n":14, "h":4,  "s":0}, [0, 4, 8, 12]),
        ]
@pytest.mark.parametrize("input_data, expected_out", TEST_CASES)
def test_ilustrativeSubPerm(input_data, expected_out):
    generator = subrutines.IlustrativeTSPDiversification(problem_size=input_data["n"])
    res = generator._sub_permutation(h=input_data["h"],s=input_data["s"])
    assert res == expected_out

TEST_CASES = [
        {"size":10, "instances":10}
        ]
@pytest.mark.parametrize("input_data", TEST_CASES)
def test_ilustrativeDiversification(input_data):
    generator = subrutines.IlustrativeTSPDiversification(problem_size=input_data["size"])
    out = generator.diversificate()
    assert len(out) == input_data["instances"] 
    for instance in out:
        assert len(instance) == input_data["size"]
        # print(instance)
    # assert False
TEST_CASES = [
        {"n": 4}
        ]
@pytest.mark.parametrize("input_data", TEST_CASES)
def test_heapPermutations(input_data):
    a = list(range(input_data["n"]))
    perms = list()
    utils.heapPermutations(input_data["n"], a,lambda a: perms.append(a.copy()))
    assert len(perms) == math.factorial(input_data["n"])
    non_repeated = set()
    for instance in perms:
        non_repeated.add(tuple(instance))
    assert len(non_repeated) == len(perms)


TEST_CASES = [
        {"size":10, "instances":10}
        ]
@pytest.mark.parametrize("input_data", TEST_CASES)
def test_ilustrativeDiversification(input_data):
    generator = subrutines.TSPHeapDiversification(problem_size=input_data["size"], 
                                                  number_of_problem_instances=input_data["instances"])
    out = generator.diversificate()
    assert len(out) == input_data["instances"] 
    for instance in out:
        assert len(instance) == input_data["size"]
    

