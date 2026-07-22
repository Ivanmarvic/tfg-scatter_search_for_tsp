from ScatterSearchTSP import diversification, improveMethod, combinationMethod, refSet, subsetGenerator
from importlib import resources
from typing import Dict, NamedTuple
import pathlib
import time 

from ScatterSearchTSP.tsp_types import TSP, FitTour 

class SolverData(NamedTuple):
    total_time_seconds: float
    improve_time_seconds: float
    scatter_loops: int 
    improve_counter: int
    refSet_update_data: Dict
    diver_improve_time: float
    best_cost_diver: float

class ScatterSearcherTSP():
    def __init__(self, diversificator: diversification.DiversificationGenerator, 
                 improveMethod1: improveMethod.ImproveMethod, improveMethod2: improveMethod.ImproveMethod, refSet:refSet.RefSetTSP, 
                 combinationMethod: combinationMethod.CombinationMethod, subsetGenerator: subsetGenerator.subsetGenerator ) -> None:
        self.diversificator = diversificator 
        self.improveMethod1 = improveMethod1 
        self.improveMethod2 = improveMethod2 
        self.refSet = refSet 
        self.combinationMethod = combinationMethod 
        self.subsetGenerator = subsetGenerator 

    def reset(self):
        self.subsetGenerator.reset()

    def solve(self, problem:TSP):
        init_time = time.perf_counter()
        improve_time = 0
        improve_counter = 0
        initial_solutions = self.diversificator.diversificate()
        im_tours = set()
        for sol in initial_solutions:
            t0 = time.perf_counter()
            im_sol = self.improveMethod1.improve(sol)
            improve_counter += 1
            t1 = time.perf_counter() 
            improve_time += t1 - t0

            im_tours.add(im_sol)

        im_tours = list(im_tours)
        tour_costs = problem.trace_tours(im_tours)
        fit_tours = list() 

        for i in range(len(im_tours)):
            fit = FitTour(fitness=tour_costs[i], tour=im_tours[i])
            fit_tours.append(fit)

        nsol = self.refSet.set(fit_tours) 
        print(f"working with {nsol} initial solutions")
        print(f"best solution from diversification {self.refSet.best_solution.fitness}")
        costs = problem.trace_tours(self.refSet.b_set)
        for c in costs:
            print("coste: " , c)
        print("DIVERSIFICATION")
        costs = problem.trace_tours(self.refSet.d_set)
        for c in costs:
            print("coste: " , c)
        diver_improve_time = time.perf_counter() - init_time
        best_cost_diver = self.refSet.best_solution.fitness

        updated = True 
        loop_counter = 0
        refSet_history = dict()
        while updated:
            subsets = self.subsetGenerator.generateSubsets(b= self.refSet.b_set, d=self.refSet.d_set) 
            new_solutions = set()
            for s in subsets:
                solution = self.combinationMethod.combinate(list(s)) 
                t0 = time.perf_counter()
                solution = self.improveMethod2.improve(solution)
                improve_counter += 1
                t1 = time.perf_counter()
                improve_time += t1 - t0
                new_solutions.add(solution)

            new_solutions = list(new_solutions)
            costs = problem.trace_tours(new_solutions)
            fit_tours = list()
            for i in range(len(new_solutions)):
                fit = FitTour(fitness=costs[i], tour=new_solutions[i])
                fit_tours.append(fit)
            updated = self.refSet.update(fit_tours)
            if updated: 
                loop_counter += 1
                refSet_history[loop_counter] = self.refSet.last_inserted_indices
                print(f" {len(refSet_history[loop_counter])} new candidates found by combination")
                if 0 in self.refSet.last_inserted_indices:
                    print(f"New best solution found by combination ... cost: {self.refSet.best_solution.fitness}")

        best = self.refSet.best_solution
        total_time = time.perf_counter() - init_time
        execution_data = SolverData(total_time, improve_time, loop_counter, improve_counter, refSet_history, diver_improve_time, best_cost_diver)
        print(f"Scatter search finalized ... cost: {self.refSet.best_solution.fitness} time: {total_time}")
        self.reset()
        return best, execution_data
