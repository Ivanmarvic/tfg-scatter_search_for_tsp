from typing import Tuple, NamedTuple

type Tour = Tuple[int, ...]
class FitTour(NamedTuple):
    fitness: int
    tour: Tour
