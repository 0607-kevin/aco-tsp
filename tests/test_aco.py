"""Tests for ACO components and solver behaviour.

Run from the project root::

    python tests/test_aco.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from aco import (
    ACOSolver,
    Ant,
    build_distance_matrix,
    load_cities,
    nearest_neighbor_tour,
    tour_length,
)


# ----------------------------------------------------------------------
# Geometry helpers
# ----------------------------------------------------------------------
def test_distance_matrix_properties():
    points = [(0, 0), (3, 0), (3, 4)]
    dist = build_distance_matrix(points)
    for i in range(3):
        assert dist[i][i] == 0.0
        for j in range(3):
            assert dist[i][j] == dist[j][i]
    assert dist[0][1] == 3.0
    assert dist[0][2] == 5.0
    assert dist[1][2] == 4.0


def test_tour_length_is_closed():
    points = [(0, 0), (1, 0), (1, 1)]
    dist = build_distance_matrix(points)
    # 0->1 (1) + 1->2 (1) + 2->0 (sqrt2)
    assert abs(tour_length([0, 1, 2], dist) - (2 + 2 ** 0.5)) < 1e-9


def test_nearest_neighbour_is_a_valid_tour():
    points = load_cities(str(ROOT / "data" / "cities.json"), "small")
    dist = build_distance_matrix(points)
    tour = nearest_neighbor_tour(dist, start=0)
    assert sorted(tour) == list(range(len(points)))


# ----------------------------------------------------------------------
# Ant
# ----------------------------------------------------------------------
def test_ant_visits_every_city_once():
    points = load_cities(str(ROOT / "data" / "cities.json"), "small")
    dist = build_distance_matrix(points)
    import random

    ant = Ant(start_city=0)
    n = len(points)
    pheromone = [[1.0] * n for _ in range(n)]
    tour = ant.construct(n, dist, pheromone, 1.0, 3.0, random.Random(1))
    assert sorted(tour) == list(range(n))
    assert tour[0] == 0
    assert ant.tour_length_value > 0


# ----------------------------------------------------------------------
# Solver
# ----------------------------------------------------------------------
def _solve(seed=1, elitist=0.0, iterations=80):
    points = load_cities(str(ROOT / "data" / "cities.json"), "small")
    solver = ACOSolver(
        points, n_ants=20, n_iterations=iterations,
        elitist_weight=elitist, seed=seed,
    )
    tour, length = solver.run()
    return solver, tour, length


def test_solver_returns_valid_tour():
    solver, tour, length = _solve()
    assert sorted(tour) == list(range(solver.n))
    assert length == solver.best_length
    assert abs(tour_length(tour, solver.dist) - length) < 1e-9


def test_convergence_history_is_non_increasing():
    solver, _, _ = _solve()
    for a, b in zip(solver.history, solver.history[1:]):
        assert b <= a + 1e-12


def test_aco_beats_nearest_neighbour():
    solver, _, length = _solve(seed=3, elitist=10.0, iterations=120)
    nn = nearest_neighbor_tour(solver.dist, start=0)
    nn_length = tour_length(nn, solver.dist)
    assert length <= nn_length


def test_pheromone_stays_positive_and_symmetric():
    solver, _, _ = _solve(seed=2)
    for i in range(solver.n):
        for j in range(solver.n):
            assert solver.pheromone[i][j] > 0.0
            assert solver.pheromone[i][j] == solver.pheromone[j][i]


def test_elitist_does_not_worsen_result():
    _, _, plain = _solve(seed=5, elitist=0.0, iterations=100)
    _, _, elite = _solve(seed=5, elitist=10.0, iterations=100)
    assert elite <= plain + 1e-9


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\n{len(fns)} tests passed.")


if __name__ == "__main__":
    _run_all()
