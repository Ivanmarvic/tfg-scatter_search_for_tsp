import math

# devuelve la permutación k del array original O(n²)
def lehmerPermutation(k:int, original_array:list) -> list:
    array_copy = original_array.copy()
    result = list()
    for i in range(len(array_copy),  0, -1):
        fact = math.factorial(i - 1)
        p = k // fact
        result.append(array_copy.pop(p))
        k = k % fact
        
    return result

