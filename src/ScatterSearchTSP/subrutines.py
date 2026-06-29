from abc import ABC, abstractmethod
from typing import List
import random
from ScatterSearchTSP import utils
import math

class DiversificationGenerator(ABC):
    # def __init__(self) -> None:
    #     pass
    @abstractmethod
    def diversificate(self) -> List[List[int]]:
        pass

# No se implementarlo ahora mismo

# O(n² * I)
class TSPLehmerDiversificator(DiversificationGenerator):
    def __init__(self, problem_size, number_of_problem_instances) -> None:
        self.n = problem_size
        self.instances = number_of_problem_instances
        super().__init__()
    def diversificate(self) -> List[List[int]]:
        output_list = list()
        n_perms = math.factorial(self.n)
        distance = n_perms // self.instances 
        original_array = list(range(self.n))
        i = 0
        while i < n_perms and len(output_list) < self.instances:
            instance = utils.lehmerPermutation(i, original_array)
            output_list.append(instance)
            i += distance
        return output_list

        

# I * O(random.shuffle(n))  o así depende random.shuffle
class TSPRandomDiversification(DiversificationGenerator):
    def __init__(self, problem_size, number_of_problem_instances) -> None:
        self.instances = number_of_problem_instances
        self.n = problem_size
        super().__init__()
    def diversificate(self) -> List[List[int]]:
        output_list = list()
        city_list = list(range(self.n))
        for _ in range(self.instances):
            new_instance = city_list.copy()
            random.shuffle(new_instance)
            output_list.append(new_instance)
        return output_list

# O(n²) o así
class IlustrativeTSPDiversification(DiversificationGenerator):
    def __init__(self, problem_size) -> None:
        self.n = problem_size
        super().__init__()

    def _sub_permutation(self, h,s):
        i = s
        result = list()
        while i < self.n:
            result.append(i)
            i += h
        return result

    def _perm_h(self,h) -> List[int]:
        result = list()
        for s in range(h-1, -1, -1):
            result.extend(self._sub_permutation(h,s))

        # assert len(result) == self.n

        return result

    def diversificate(self) -> List[List[int]]:
        output_list = list()
        for i in range(1,self.n+1):
            instance = self._perm_h(i)
            output_list.append(instance)
        return output_list




