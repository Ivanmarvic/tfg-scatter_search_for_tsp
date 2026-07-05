
import pytest
from ScatterSearchTSP import utils
from ScatterSearchTSP import refSet
import tsplib95 as tsplib
from ScatterSearchTSP import tsp_types
from typing import NamedTuple, Collection


TEST_CASES = [
        ({"tour1":(1,2,3,4), "tour2":(2,1,3,4)}, 2),
        ({"tour1":(1,2,3,4), "tour2":(1,2,3,4)}, 0),
        ]
@pytest.mark.parametrize("input_data, expected_output", TEST_CASES)
def test_difference_utils(input_data, expected_output):
    diff = utils.permutation_difference(input_data["tour1"], input_data["tour2"])
    assert diff == expected_output

TEST_CASES = [
        ((1,2,3,4), {(1,2,3,4),(2,1,3,4)}, 0),
        ((1,2,3,4), {(1,3,4,2),(2,1,3,4)}, 2),
        ]

@pytest.mark.parametrize("tour, tourSet, expected_distance", TEST_CASES)
def test_min_set_distance(tour, tourSet, expected_distance):
    diff = utils.min_set_distance(tour, tourSet, utils.permutation_difference)
    assert diff == expected_distance

class expected_RefSet(NamedTuple):
    b:Collection[tsp_types.Tour]
    d:Collection[tsp_types.Tour]
TEST_CASES = [
        (1,2, [

            tsp_types.FitTour(5,(1,2,3,4)), 
            tsp_types.FitTour(2,(4,3,2,1)),
            tsp_types.FitTour(1,(3,4,2,1)),
            tsp_types.FitTour(8,(3,4,1,2)),

               ],
         expected_RefSet(b= [(3,4,2,1), (4,3,2,1)], d= [(1,2,3,4)]),
         tsp_types.FitTour(-99,(2,4,3,1)),
        ),

        (2,2, [

            tsp_types.FitTour(5,(1,2,3,4)), 
            tsp_types.FitTour(2,(4,3,2,1)),
            tsp_types.FitTour(1,(3,4,2,1)),
            tsp_types.FitTour(8,(3,4,1,2)),
            tsp_types.FitTour(12,(3,1,2,4)),

               ],
         expected_RefSet(b= [(3,4,2,1), (4,3,2,1)], d= [(1,2,3,4), (3,4,1,2)]),
         tsp_types.FitTour(-99,(2,4,3,1)),
        ),
        (1,2, [

            tsp_types.FitTour(-5,(1,2,3,4)), 
            tsp_types.FitTour(-2,(4,3,2,1)),
            tsp_types.FitTour(-1,(3,4,2,1)),
            tsp_types.FitTour(-8,(3,4,1,2)),

               ],
         expected_RefSet(b= [(3,4,1,2), (1,2,3,4)], d= [(4,3,2,1)]),
         tsp_types.FitTour(-99,(2,4,3,1)),
        ),
        ]

@pytest.mark.parametrize("d_size, b_size, fit_tours, expected_RefSet, best_tour", TEST_CASES)
def test_refSetFixedDiversity(d_size, b_size, fit_tours, expected_RefSet, best_tour):
    ref = refSet.RefSetFixedDiversity(d_size=d_size, b_size=b_size, 
                                      distance_fn=utils.permutation_difference)
    res = ref.set(fit_tours)
    assert res == d_size + b_size
    assert len(ref.b_set) == b_size
    assert len(ref.d_set) == d_size

    updated = ref.update(fit_tours)
    assert updated == False
    for i in range(b_size):
        assert ref._refList[i].tour == expected_RefSet.b[i]
    for i in range(d_size):
        assert ref._refList[b_size + i].tour == expected_RefSet.d[i] 

    for sol in ref.b_set:
        assert sol in expected_RefSet.b
    for sol in ref.d_set:
        assert sol in expected_RefSet.d

    fit_tours.append(best_tour)
    updated = ref.update(fit_tours)
    assert updated == True
    assert best_tour.tour in ref.b_set







