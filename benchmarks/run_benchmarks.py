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
    def get_method_name(method_obj: Any) -> str:
        """Devuelve la propiedad .name del objeto si existe, o el nombre de su clase."""
        if hasattr(method_obj, "name"):
            return getattr(method_obj, "name")
        return getattr(method_obj, "__class__", type(method_obj)).__name__
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
            "diversificator": get_method_name(ss.diversificator),
            "improveMethod1": get_method_name(ss.improveMethod1),
            "improveMethod2": get_method_name(ss.improveMethod2),
            "RefSetMethod": get_method_name(ss.refSet),
            "combinationMethod": get_method_name(ss.combinationMethod),
            "subsetGenerationMethod": get_method_name(ss.subsetGenerator),
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

def benchmark_improve_method_python(problem_name, solution_name, params):

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
    im_lkh = improveMethod.LKImprove(problem)
    ss1 = create_base_searcher(im_cross, im_cross)
    ss2 = create_base_searcher(im_lkh, im_lkh)
    ss3 = create_base_searcher(im_cross, im_lkh)
    ss4 = create_base_searcher(im_lkh, im_cross)
    df = run_scatter_benchmarks([ss1, ss2, ss3, ss4], problem, problem_name, opt_cost, params, n_runs=2)
    # df = run_scatter_benchmarks([ss2], problem, problem_name, opt_cost, params)
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

    simple_params = {
            'RUNS': 1,                     
            'MAX_TRIALS': 1,                
            'KICKS': 0,                      
            'MOVE_TYPE': 2,                 
            'TRACE_LEVEL': 0,              
            'MAX_CANDIDATES': 5,
            'ASCENT_CANDIDATES': 2,
            'OPTIMUM': opt_cost,
            }

    complex_params = {
            'RUNS': 1,                     
            'MAX_TRIALS': 1,                
            'KICKS': 0,                      # Sin perturbaciones
            'MOVE_TYPE': 5,                  # 5-opt
            'TRACE_LEVEL': 0,                 # Silencioso
            'MAX_CANDIDATES': 5,
            'ASCENT_CANDIDATES': 50,
            'OPTIMUM': opt_cost,
            }

    im_simple_lkh = improveMethod.LKHImprove(problem, params=simple_params) 
    im_lkh = improveMethod.LKHImprove(problem, params=complex_params)
    com_naive = combinationMethod.NaiveTSPCombination()
    com_convex = combinationMethod.ConvexTSPCombination(problem)
    ss1 = create_base_searcher(im_simple_lkh, im_simple_lkh, com_naive)
    ss2 = create_base_searcher(im_simple_lkh, im_simple_lkh, com_convex)
    ss3 = create_base_searcher(im_simple_lkh, im_lkh, com_naive)
    ss4 = create_base_searcher(im_simple_lkh, im_lkh, com_convex)
    df = run_scatter_benchmarks([ss1, ss2, ss3, ss4], problem, problem_name, opt_cost, params, n_runs=5)
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
    simple_params = {
            'RUNS': 1,                     
            'MAX_TRIALS': 1,                
            'KICKS': 0,                      
            'MOVE_TYPE': 2,                 
            'TRACE_LEVEL': 0,              
            'MAX_CANDIDATES': 5,
            'ASCENT_CANDIDATES': 2,
            'OPTIMUM': opt_cost,
            }

    complex_params = {
            'RUNS': 1,                     
            'MAX_TRIALS': 1,                
            'KICKS': 0,                      # Sin perturbaciones
            'MOVE_TYPE': 5,                  # 5-opt
            'TRACE_LEVEL': 0,                 # Silencioso
            'MAX_CANDIDATES': 5,
            'ASCENT_CANDIDATES': 50,
            'OPTIMUM': opt_cost,
            }
    for s in sizes:
        in_params["b_size"] = s[0]
        in_params["d_size"] = s[1]
        in_params["diver_size"] = params["diver_size"]
        im_simple_lkh = improveMethod.LKHImprove(problem, params=simple_params) 
        im_lkh = improveMethod.LKHImprove(problem, params=complex_params)
        ss1 = create_base_searcher(im_simple_lkh, im_simple_lkh, in_params)
        ss2 = create_base_searcher(im_simple_lkh, im_lkh, in_params)
        searchers.append(ss1)
        searchers.append(ss2)
    df = run_scatter_benchmarks(searchers, problem, problem_name, opt_cost, in_params, n_runs=5)
    return df

def benchmark_diversification(problem_name, solution_name, params):

    def create_base_searcher(diver):
        simple_params = {
                'RUNS': 1,                     
                'MAX_TRIALS': 1,                
                'KICKS': 0,                      
                'MOVE_TYPE': 2,                 
                'TRACE_LEVEL': 0,              
                'MAX_CANDIDATES': 5,
                'ASCENT_CANDIDATES': 2,
                'OPTIMUM': opt_cost,
                }

        complex_params = {
                'RUNS': 1,                     
                'MAX_TRIALS': 1,                
                'KICKS': 0,                      # Sin perturbaciones
                'MOVE_TYPE': 5,                  # 5-opt
                'TRACE_LEVEL': 0,                 # Silencioso
                'MAX_CANDIDATES': 5,
                'ASCENT_CANDIDATES': 50,
                'OPTIMUM': opt_cost,
                }

        ref = refSet.RefSetFixedDiversity(b_size=params["b_size"], d_size=params["d_size"], distance_fn=utils.edge_difference)
        com = combinationMethod.NaiveTSPCombination()
        im1 = improveMethod.LKHImprove(problem, simple_params) 
        im2 = improveMethod.LKHImprove(problem, complex_params) 
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
    diver2 = diversification.TSPLehmerDiversificator(problem_size=problem.dimension, number_of_problem_instances=params["diver_size"]) 
    diver3 = diversification.TSPRandomDiversification(problem_size=problem.dimension, number_of_problem_instances=params["diver_size"])

    ss1 = create_base_searcher(diver1)
    ss2 = create_base_searcher(diver2)
    ss3 = create_base_searcher(diver3)
    df = run_scatter_benchmarks([ss1, ss2, ss3], problem, problem_name, opt_cost, params, n_runs=5)
    return df 

# PROBLEM_FILES = [ ("berlin52.tsp", "berlin52.opt.tour")]
PROBLEM_FILES = [ ("berlin52.tsp", "berlin52.opt.tour"), ("gr96.tsp", "gr96.opt.tour")]
for problem_name, best_tour in PROBLEM_FILES:
    results = []
    params = {"diver_size": 50, "b_size": 5, "d_size": 5}
    results1 = benchmark_improve_method_python(problem_name, best_tour, params)
    results.append(results1)
    df = pd.DataFrame(results[0])
    for i in range(1, len(results)):
        df = pd.concat([df, results[i]], ignore_index=True)
    df.to_csv( BASE_DIR / "benchmarks" / "results" / f"results_{problem_name}.csv")

PROBLEM_FILES = [ ("a280.tsp", "a280.opt.tour"), ("gr666.tsp", "gr666.opt.tour"), ("pa561.tsp", "pa561.opt.tour")]
# PROBLEM_FILES = [ ("a280.tsp", "a280.opt.tour")]
for problem_name, best_tour in PROBLEM_FILES:
    results = []
    params = {"diver_size": 100, "b_size": 5, "d_size": 5}
    results2 = benchmark_combination_method(problem_name, best_tour, params)
    results.append(results2)
    results3 = benchmark_refSetSizes(problem_name, best_tour, [(5,5),(10,10), (15,15)], params)
    results.append(results3)
    results4 = benchmark_diversification(problem_name, best_tour, params)
    results.append(results4)
    print(f"ESCRIBIENDO RESULTADOS de {problem_name}")
    df = pd.DataFrame(results[0])
    for i in range(1, len(results)):
        df = pd.concat([df, results[i]], ignore_index=True)
    df.to_csv( BASE_DIR / "benchmarks" / "results" / f"results_c_{problem_name}.csv")


