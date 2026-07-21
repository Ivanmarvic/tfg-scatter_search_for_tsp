import pytest 
import pathlib

from ScatterSearchTSP.tsp_types import TSP
from ScatterSearchTSP import ScatterSearcher, diversification, improveMethod, refSet, combinationMethod, subsetGenerator, utils


BASE_DIR = pathlib.Path(__file__).parent.parent
TEST_CASES = [
        ["berlin52.tsp", {"b_size":6, "d_size": 6}], ["ulysses5.tsp", {"b_size":2, "d_size": 1}] ]

@pytest.mark.parametrize("problem_file, params", TEST_CASES)
def test_scatterSearcher(problem_file, params):
    ppath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  problem_file
    problem = TSP.load(str(ppath))
    diversificator = diversification.IlustrativeTSPDiversification(problem_size=problem.dimension) 
    im = improveMethod.CrossEliminate(problem) 
    ref = refSet.RefSetFixedDiversity(b_size=params["b_size"], d_size=params["d_size"], distance_fn=utils.permutation_difference)
    com = combinationMethod.NaiveTSPCombination()
    sub = subsetGenerator.SimpleSubsetGenerator()
    ss = ScatterSearcher.ScatterSearcherTSP(diversificator=diversificator, improveMethod1= im, improveMethod2= im, 
                                            refSet=ref, combinationMethod=com, subsetGenerator=sub)
    best, data = ss.solve(problem) 
    print(f"best tour is {best.tour} with cost {best.fitness}, execution data {data}")
    for i in range(problem.dimension):
        assert i in best.tour
    for sol in ref._refList:
        assert sol.fitness >= best.fitness
    assert False, "to get the stdout"
