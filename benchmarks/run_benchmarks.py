from ScatterSearchTSP import ScatterSearcher, diversification, improveMethod, refSet, combinationMethod, subsetGenerator, utils
import pandas as pd 
from ScatterSearchTSP.tsp_types import TSP
import pathlib
import tsplib95 as tsplib
from typing import List, Dict, Any

RESULTS_DIR = pathlib.Path(__file__).parent / "results"
BASE_DIR = pathlib.Path(__file__).parent.parent
TEST_CASES = [
        ["berlin52.tsp", {"b_size":6, "d_size": 6}], ["ulysses5.tsp", {"b_size":2, "d_size": 1}] ]

    # ppath = BASE_DIR / "src" / "ScatterSearchTSP" / "tsp_instances" /  problem_file

def run_scatter_benchmarks(
    searchers: List[Any], 
    problem: Any, 
    problem_name: str, 
    opt_cost: float, 
    params: Dict[str, Any]
) -> pd.DataFrame:
    """
    Ejecuta una lista de configuraciones de ScatterSearcher en un problema dado 
    y recopila las métricas en un DataFrame de Pandas.
    """
    rows = []

    for ss in searchers:
        # 1. Ejecución del solver
        sol, data = ss.solve(problem)
        
        # 2. Cálculo de la desviación porcentual respecto al óptimo
        optimal_deviation = ((sol.fitness - opt_cost) / opt_cost) * 100

        # 3. Mapeo de métricas dinámico (extrae nombres de clases de los objetos)
        rows.append({
            "instancia": problem_name,
            "diversificator": getattr(ss.diversificator, "__class__", type(ss.diversificator)).__name__,
            "improveMethod1": getattr(ss.improveMethod1, "__class__", type(ss.improveMethod1)).__name__,
            "improveMethod2": getattr(ss.improveMethod2, "__class__", type(ss.improveMethod2)).__name__,
            "RefSetMethod": getattr(ss.refSet, "__class__", type(ss.refSet)).__name__,
            "combinationMethod": getattr(ss.combinationMethod, "__class__", type(ss.combinationMethod)).__name__,
            "subsetGenerationMethod": getattr(ss.subsetGenerator, "__class__", type(ss.subsetGenerator)).__name__,
            "b_size": params.get("b_size"),
            "d_size": params.get("d_size"),
            "total_cost": sol.fitness,
            "optimal_deviation_pct": optimal_deviation,
            "total_time": getattr(data, "total_time_seconds", None),
            "improve_method_time": getattr(data, "improve_time_seconds", None),
            "scatter_loops": getattr(data, "scatter_loops", None),
            "improve_method_calls": getattr(data, "improve_counter", None),
            "found_tour": sol.tour,
            "refSet_update_history": getattr(data, "refSet_update_data", None),
        })

    return pd.DataFrame(rows)

def benchmark_improve_method(problem_name, solution_name, params):

    def create_base_searcher(im1, im2):
        diversificator = diversification.IlustrativeTSPDiversification(problem_size=problem.dimension) 
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
    df = run_scatter_benchmarks([ss1, ss2, ss3, ss4], problem, problem_name, opt_cost, params)
    # sol_ss1, data_ss1 = ss1.solve(problem) 
    # sol_ss2, data_ss2 = ss2.solve(problem) 
    # sol_ss3, data_ss3 = ss3.solve(problem) 

    # optimal_d1 = ((sol_ss1.fitness - opt_cost) / opt_cost) * 100
    # optimal_d2 = ((sol_ss2.fitness - opt_cost) / opt_cost) * 100
    # optimal_d3 = ((sol_ss3.fitness - opt_cost) / opt_cost) * 100

    # data = {
    #         "instancia": [problem_name, problem_name, problem_name],
    #         "diversificator": ["Ilustrative", "Ilustrative", "Ilustrative"],
    #         "improveMethod1": ["im_cross", "lkh", "im_cross"],
    #         "improveMethod2": ["im_cross", "lkh", "lkh"],
    #         "RefSetMethod": ["Fixed_Diversity","Fixed_Diversity","Fixed_Diversity"],
    #         "combinationMethod":["Naive","Naive","Naive"],
    #         "subsetGenerationMethod":["Simple", "Simple", "Simple"],
    #         "b_size":[params["b_size"],params["b_size"],params["b_size"]],
    #         "d_size":[params["d_size"],params["d_size"],params["d_size"]],
    #         "total_cost":[sol_ss1.fitness, sol_ss2.fitness, sol_ss3.fitness],
    #         "optimal_desviation":[optimal_d1, optimal_d2, optimal_d3],
    #         "total_time":[data_ss1.total_time_seconds, data_ss2.total_time_seconds, data_ss3.total_time_seconds],
    #         "improve_method time":[data_ss1.improve_time_seconds, data_ss2.improve_time_seconds, data_ss3.improve_time_seconds],
    #         "scatter loops":[data_ss1.scatter_loops, data_ss2.scatter_loops, data_ss3.scatter_loops],
    #         "improve method calls":[data_ss1.improve_counter, data_ss2.improve_counter, data_ss3.improve_counter],
    #         "found_tour":[sol_ss1.tour, sol_ss2.tour,sol_ss3.tour,],
    #         "refSet_update_history":[data_ss1.refSet_update_data, data_ss2.refSet_update_data, data_ss3.refSet_update_data],
    #         }
    # df = pd.DataFrame(data)
    return df 
def benchmark_combination_method(problem_name, solution_name, params):
    def create_base_searcher(im1, im2, com):
        diversificator = diversification.IlustrativeTSPDiversification(problem_size=problem.dimension) 
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
    im_lkh = improveMethod.LKImprove(problem)
    com_naive = combinationMethod.NaiveTSPCombination()
    com_convex = combinationMethod.ConvexTSPCombination(problem)
    ss1 = create_base_searcher(im_cross, im_cross, com_naive)
    ss2 = create_base_searcher(im_cross, im_cross, com_convex)
    ss3 = create_base_searcher(im_cross, im_lkh, com_naive)
    ss4 = create_base_searcher(im_cross, im_lkh, com_convex)
    df = run_scatter_benchmarks([ss1, ss2, ss3, ss4], problem, problem_name, opt_cost, params)
    return df


params = {"b_size": 6, "d_size": 6}
# results1 = benchmark_improve_method("berlin52.tsp", "berlin52.opt.tour", params)
# results1.to_csv(RESULTS_DIR / "results_improve_method.csv")
results2 = benchmark_combination_method("berlin52.tsp", "berlin52.opt.tour", params)
results2.to_csv(RESULTS_DIR / "results_combination_method.csv")

