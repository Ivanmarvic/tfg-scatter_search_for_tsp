from ScatterSearchTSP import ScatterSearcher, diversification, improveMethod, refSet, combinationMethod, subsetGenerator, utils
import pandas as pd 
from ScatterSearchTSP.tsp_types import TSP
import pathlib
import tsplib95 as tsplib
from typing import List, Dict, Any

RESULTS_DIR = pathlib.Path(__file__).parent / "results"
BASE_DIR = pathlib.Path(__file__).parent.parent
def run_scatter_benchmarks(
    searchers: List[ScatterSearcher.ScatterSearcherTSP], 
    problem: Any, 
    problem_name: str, 
    opt_cost: float, 
    params: Dict[str, Any],
    n_runs:int = 1 
) -> pd.DataFrame:
    rows = []
    for ss in searchers:
        runs_data:List[ScatterSearcher.SolverData] = []
        runs_sol = []
        for _ in range(n_runs):
            sol, data = ss.solve(problem)
            runs_data.append(data)
            runs_sol.append(sol)

        sol = min(runs_sol)
        optimal_deviation = ((sol.fitness - opt_cost) / opt_cost) * 100

        avg_time = sum(d.total_time_seconds for d in runs_data) / n_runs
        avg_im_time = sum(d.improve_time_seconds for d in runs_data) / n_runs
        avg_im_counter = sum(d.improve_counter for d in runs_data) / n_runs 
        avg_div_time = sum(d.diver_improve_time for d in runs_data) / n_runs
        avg_best_cost_diver = sum(d.best_cost_diver for d in runs_data) / n_runs 
        avg_scatter_loops = sum(d.scatter_loops for d in runs_data) / n_runs
        refSet_history = runs_data[0].refSet_update_data
        

        rows.append({
            "instancia": problem_name,
            "diversificator": getattr(ss.diversificator, "__class__", type(ss.diversificator)).__name__,
            "improveMethod1": getattr(ss.improveMethod1, "__clanss__", type(ss.improveMethod1)).__name__,
            "improveMethod2": getattr(ss.improveMethod2, "__class__", type(ss.improveMethod2)).__name__,
            "RefSetMethod": getattr(ss.refSet, "__class__", type(ss.refSet)).__name__,
            "combinationMethod": getattr(ss.combinationMethod, "__class__", type(ss.combinationMethod)).__name__,
            "subsetGenerationMethod": getattr(ss.subsetGenerator, "__class__", type(ss.subsetGenerator)).__name__,
            "diver_size": params.get("diver_size"),
            "b_size": params.get("b_size"),
            "d_size": params.get("d_size"),
            "total_cost": sol.fitness,
            "optimal_deviation_pct": optimal_deviation,
            "avg_total_time": avg_time,
            "avg_improve_method_time": avg_im_time,
            "avg_scatter_loops": avg_scatter_loops,
            "avg_improve_method_calls": avg_im_counter,
            "found_tour": sol.tour,
            "first_refSet_update_history": refSet_history,
            "avg_diversification_improve_time": avg_div_time,
            "avg_diver_best_cost": avg_best_cost_diver,
            "n_runs": n_runs,
        })

    return pd.DataFrame(rows)

def benchmark_improve_method(problem_name, solution_name, params):

    def create_base_searcher(im1, im2):
        diversificator = diversification.TSPLehmerDiversificator(problem_size=problem.dimension, number_of_problem_instances=params["diver_size"]) 
        ref = refSet.RefSetFixedDiversity(b_size=params["b_size"], d_size=params["d_size"], distance_fn=utils.edge_difference)
        com = combinationMethod.NaiveTSPCombination()
        sub = subsetGenerator.SimpleSubsetGenerator()
        ss = ScatterSearcher.ScatterSearcherTSP(diversificator=diversificator, improveMethod1= im1, improveMethod2= im2, 
                                                refSet=ref, combinationMethod=com, subsetGenerator=sub)
        return ss

    ppath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  problem_name
    spath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  solution_name

    problem = TSP.load(str(ppath))
    opt_sol = tsplib.load(str(spath))
    tsplib_problem = tsplib.load(str(ppath))
    opt_cost = tsplib_problem.trace_tours(opt_sol.tours)[0]

    im_cross = improveMethod.CrossEliminate(problem) 
    im_lkh = improveMethod.LKHImprove(problem)
    # ss1 = create_base_searcher(im_cross, im_cross)
    ss2 = create_base_searcher(im_lkh, im_lkh)
    # ss3 = create_base_searcher(im_cross, im_lkh)
    # ss4 = create_base_searcher(im_lkh, im_cross)
    # df = run_scatter_benchmarks([ss1, ss2, ss3, ss4], problem, problem_name, opt_cost, params)
    df = run_scatter_benchmarks([ss2], problem, problem_name, opt_cost, params)
    return df 
def benchmark_combination_method(problem_name, solution_name, params):
    def create_base_searcher(im1, im2, com):
        diversificator = diversification.TSPLehmerDiversificator(problem_size=problem.dimension, number_of_problem_instances=params["diver_size"]) 
        ref = refSet.RefSetFixedDiversity(b_size=params["b_size"], d_size=params["d_size"], distance_fn=utils.edge_difference)
        sub = subsetGenerator.SimpleSubsetGenerator()
        ss = ScatterSearcher.ScatterSearcherTSP(diversificator=diversificator, improveMethod1= im1, improveMethod2= im2, 
                                                refSet=ref, combinationMethod=com, subsetGenerator=sub)
        return ss

    ppath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  problem_name
    spath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  solution_name

    problem = TSP.load(str(ppath))
    opt_sol = tsplib.load(str(spath))
    tsplib_problem = tsplib.load(str(ppath))
    opt_cost = tsplib_problem.trace_tours(opt_sol.tours)[0]

    im_cross = improveMethod.CrossEliminate(problem) 
    im_lkh = improveMethod.LKHImprove(problem)
    com_naive = combinationMethod.NaiveTSPCombination()
    com_convex = combinationMethod.ConvexTSPCombination(problem)
    ss1 = create_base_searcher(im_cross, im_cross, com_naive)
    ss2 = create_base_searcher(im_cross, im_cross, com_convex)
    ss3 = create_base_searcher(im_cross, im_lkh, com_naive)
    ss4 = create_base_searcher(im_cross, im_lkh, com_convex)
    df = run_scatter_benchmarks([ss1, ss2, ss3, ss4], problem, problem_name, opt_cost, params)
    return df
def benchmark_refSetSizes(problem_name, solution_name, sizes, params):
    def create_base_searcher(im1, im2, params):
        diversificator = diversification.TSPLehmerDiversificator(problem_size=problem.dimension, number_of_problem_instances=params["diver_size"]) 
        ref = refSet.RefSetFixedDiversity(b_size=params["b_size"], d_size=params["d_size"], distance_fn=utils.edge_difference)
        com = combinationMethod.NaiveTSPCombination()
        sub = subsetGenerator.SimpleSubsetGenerator()
        ss = ScatterSearcher.ScatterSearcherTSP(diversificator=diversificator, improveMethod1= im1, improveMethod2= im2, 
                                                refSet=ref, combinationMethod=com, subsetGenerator=sub)
        return ss

    ppath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  problem_name
    spath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  solution_name

    problem = TSP.load(str(ppath))
    opt_sol = tsplib.load(str(spath))
    tsplib_problem = tsplib.load(str(ppath))
    opt_cost = tsplib_problem.trace_tours(opt_sol.tours)[0]
    in_params = {}
    searchers = []
    for s in sizes:
        in_params["b_size"] = s[0]
        in_params["d_size"] = s[1]
        in_params["diver_size"] = params["diver_size"]
        im_cross = improveMethod.CrossEliminate(problem) 
        im_lkh = improveMethod.LKHImprove(problem)
        ss1 = create_base_searcher(im_cross, im_cross, in_params)
        ss2 = create_base_searcher(im_cross, im_lkh, in_params)
        searchers.append(ss1)
        searchers.append(ss2)
    df = run_scatter_benchmarks(searchers, problem, problem_name, opt_cost, in_params)
    return df

def benchmark_diversification(problem_name, solution_name, params):

    def create_base_searcher(diver):
        ref = refSet.RefSetFixedDiversity(b_size=params["b_size"], d_size=params["d_size"], distance_fn=utils.edge_difference)
        com = combinationMethod.NaiveTSPCombination()
        im1 = improveMethod.CrossEliminate(problem) 
        im2 = improveMethod.CrossEliminate(problem) 
        sub = subsetGenerator.SimpleSubsetGenerator()
        ss = ScatterSearcher.ScatterSearcherTSP(diversificator=diver, improveMethod1= im1, improveMethod2= im2, 
                                                refSet=ref, combinationMethod=com, subsetGenerator=sub)
        return ss

    ppath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  problem_name
    spath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  solution_name

    problem = TSP.load(str(ppath))
    opt_sol = tsplib.load(str(spath))
    tsplib_problem = tsplib.load(str(ppath))
    opt_cost = tsplib_problem.trace_tours(opt_sol.tours)[0]

    diver1 = diversification.IlustrativeTSPDiversification(problem_size=problem.dimension) 
    diver2 = diversification.TSPLehmerDiversificator(problem_size=problem.dimension, number_of_problem_instances=problem.dimension) 
    diver3 = diversification.TSPRandomDiversification(problem_size=problem.dimension, number_of_problem_instances=problem.dimension)

    ss1 = create_base_searcher(diver1)
    ss2 = create_base_searcher(diver2)
    ss3 = create_base_searcher(diver3)
    df = run_scatter_benchmarks([ss1, ss2, ss3], problem, problem_name, opt_cost, params)
    return df 

# PROBLEM_FILES = [ ("berlin52.tsp", "berlin52.opt.tour"), ("a280.tsp", "a280.opt.tour"), ("gr96.tsp", "gr96.opt.tour")]
PROBLEM_FILES = [ ("a280.tsp", "a280.opt.tour")]

results = []
for problem_name, best_tour in PROBLEM_FILES:
    params = {"diver_size": 50, "b_size": 5, "d_size": 5}
    results1 = benchmark_improve_method(problem_name, best_tour, params)
    results.append(results1)
    # results2 = benchmark_combination_method(problem_name, best_tour, params)
    # results.append(results2)
    # results3 = benchmark_refSetSizes(problem_name, best_tour, [(5,5),(10,10), (15,15)], params)
    # results.append(results3)
    # results4 = benchmark_diversification(problem_name, best_tour, params)
    # results.append(results4)

df = pd.DataFrame(results[0])
for i in range(1, len(results)):
    df = pd.concat([df, results[i]], ignore_index=True)
df.to_csv( BASE_DIR / "benchmarks" / "results" / "results_global.csv")


