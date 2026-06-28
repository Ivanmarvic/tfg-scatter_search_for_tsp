from abc import ABC, abstractmethod
from typing import List
import random

class DiversificationGenerator(ABC):
    # def __init__(self) -> None:
    #     pass
    @abstractmethod
    def diversificate(self) -> List[List[int]]:
        pass

# No se implementarlo ahora mismo
# class TSPHeapDiversification(DiversificationGenerator):
#     def __init__(self, problem_size) -> None:
#         self.n = problem_size
#         super().__init__()
#     def diversificate(self) -> List[List[int]]:

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



