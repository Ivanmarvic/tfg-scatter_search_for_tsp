from ScatterSearchTSP import ScatterSearcher, diversification, improveMethod, refSet, combinationMethod, subsetGenerator, utils
import pandas as pd 
from ScatterSearchTSP.tsp_types import TSP
import pathlib
import tsplib95 as tsplib

RESULTS_DIR = pathlib.Path(__file__).parent / "results"
BASE_DIR = pathlib.Path(__file__).parent.parent
TEST_CASES = [
        ["berlin52.tsp", {"b_size":6, "d_size": 6}], ["ulysses5.tsp", {"b_size":2, "d_size": 1}] ]

    # ppath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  problem_file
def benchmark_improve_method(problem_name, solution_name, params):
    ppath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  problem_name
    spath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  solution_name
    params = {"b_size": 6, "d_size": 6}

    problem = TSP.load(str(ppath))
    opt_sol = tsplib.load(str(spath))
    tsplib_problem = tsplib.load(str(ppath))
    opt_cost = tsplib_problem.trace_tours(opt_sol.tours)[0]

    diversificator = diversification.IlustrativeTSPDiversification(problem_size=problem.dimension) 
    im_cross = improveMethod.CrossEliminate(problem) 
    im_lkh = improveMethod.LKImprove(problem)
    ref = refSet.RefSetFixedDiversity(b_size=params["b_size"], d_size=params["d_size"], distance_fn=utils.permutation_difference)
    com = combinationMethod.NaiveTSPCombination()
    sub = subsetGenerator.SimpleSubsetGenerator()

    ss1 = ScatterSearcher.ScatterSearcherTSP(diversificator=diversificator, improveMethod1= im_cross, improveMethod2= im_cross, 
                                            refSet=ref, combinationMethod=com, subsetGenerator=sub)

    ss2 = ScatterSearcher.ScatterSearcherTSP(diversificator=diversificator, improveMethod1= im_lkh, improveMethod2= im_lkh, 
                                            refSet=ref, combinationMethod=com, subsetGenerator=sub)
    ss3 = ScatterSearcher.ScatterSearcherTSP(diversificator=diversificator, improveMethod1= im_cross, improveMethod2= im_lkh, 
                                            refSet=ref, combinationMethod=com, subsetGenerator=sub)
    sol_ss1, data_ss1 = ss1.solve(problem) 
    sol_ss2, data_ss2 = ss2.solve(problem) 
    sol_ss3, data_ss3 = ss3.solve(problem) 

    optimal_d1 = ((opt_cost - sol_ss1.fitness) / opt_cost) * 100
    optimal_d2 = ((opt_cost - sol_ss2.fitness) / opt_cost) * 100
    optimal_d3 = ((opt_cost - sol_ss3.fitness) / opt_cost) * 100

    data = {
            "instancia": [problem_name, problem_name, problem_name],
            "diversificator": ["Ilustrative", "Ilustrative", "Ilustrative"],
            "improveMethod1": ["im_cross", "lkh", "im_cross"],
            "improveMethod2": ["im_cross", "lkh", "lkh"],
            "RefSetMethod": ["Fixed_Diversity","Fixed_Diversity","Fixed_Diversity"],
            "combinationMethod":["Naive","Naive","Naive"],
            "subsetGenerationMethod":["Simple", "Simple", "Simple"],
            "b_size":[params["b_size"],params["b_size"],params["b_size"]],
            "d_size":[params["d_size"],params["d_size"],params["d_size"]],
            "total_cost":[sol_ss1.fitness, sol_ss2.fitness, sol_ss3.fitness],
            "optimal_desviation":[optimal_d1, optimal_d2, optimal_d3],
            "total_time":[data_ss1.total_time_seconds, data_ss2.total_time_seconds, data_ss3.total_time_seconds],
            "improve_method time":[data_ss1.improve_time_seconds, data_ss2.improve_time_seconds, data_ss3.improve_time_seconds],
            "scatter loops":[data_ss1.scatter_loops, data_ss2.scatter_loops, data_ss3.scatter_loops],
            "improve method calls":[data_ss1.improve_counter, data_ss2.improve_counter, data_ss3.improve_counter],
            "found_tour":[sol_ss1.tour, sol_ss2.tour,sol_ss3.tour,],
            }
    df = pd.DataFrame(data)
    return df 


params = {"b_size": 6, "d_size": 6}
results1 = benchmark_improve_method("berlin52.tsp", "berlin52.opt.tour", params)
results1.to_csv(RESULTS_DIR / "results_improve_method.csv")

