from typing import Callable
def heapPermutations(k:int, array:list, output: Callable[[list], None]) -> None:
    if k == 1:
        output(array)
    else:
        for i in range(k):
            #even / par
            heapPermutations(k-1, array, output)
            if k % 2 == 0: 
                array[i], array[k-1] = array[k-1], array[i]
            else:
                array[0], array[k-1] = array[k-1], array[0]
