"""Ant Colony Optimization for the TSP.

This implements the classic *Ant System* (Dorigo et al.) with an optional
elitist strategy that deposits extra pheromone on the best-so-far tour.
"""

from __future__ import annotations

import random
from typing import List, Optional, Sequence, Tuple

from .ant import Ant
from .utils import (
    build_distance_matrix,
    nearest_neighbor_tour,
    tour_length,
)

Point = Tuple[float, float]


class ACOSolver:
    def __init__(
        self,
        points: Sequence[Point],
        n_ants: int = 20,
        n_iterations: int = 100,
        alpha: float = 1.0,
        beta: float = 3.0,
        rho: float = 0.1,
        q: float = 1.0,
        elitist_weight: float = 0.0,
        seed: Optional[int] = None,
    ):
        if len(points) < 2:
            raise ValueError("at least two cities are required")
        self.points = list(points)
        self.n = len(points)
        self.dist = build_distance_matrix(self.points)

        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.elitist_weight = elitist_weight
        self.rng = random.Random(seed)

        # Best-so-far tracking.
        self.best_tour: Optional[List[int]] = None
        self.best_length = float("inf")

        # Convergence data.
        self.history: List[float] = []          # best length per iteration
        self.best_tour_history: List[List[int]] = []

        self.pheromone = self._initial_pheromone()

    # ------------------------------------------------------------------
    def _initial_pheromone(self) -> List[List[float]]:
        """Initialise pheromone using the nearest-neighbour tour length."""
        nn_tour = nearest_neighbor_tour(self.dist, start=0)
        nn_length = tour_length(nn_tour, self.dist)
        tau0 = 1.0 / (self.n * nn_length)
        return [[tau0] * self.n for _ in range(self.n)]

    # ------------------------------------------------------------------
    def run(self) -> Tuple[List[int], float]:
        for _ in range(self.n_iterations):
            ants: List[Ant] = []
            for _ in range(self.n_ants):
                start = self.rng.randrange(self.n)
                ant = Ant(start)
                ant.construct(
                    self.n, self.dist, self.pheromone,
                    self.alpha, self.beta, self.rng,
                )
                ants.append(ant)

                if ant.tour_length_value < self.best_length:
                    self.best_length = ant.tour_length_value
                    self.best_tour = list(ant.tour)

            self._update_pheromone(ants)

            self.history.append(self.best_length)
            self.best_tour_history.append(list(self.best_tour))  # type: ignore[arg-type]

        return self.best_tour, self.best_length  # type: ignore[return-value]

    # ------------------------------------------------------------------
    def _update_pheromone(self, ants: Sequence[Ant]) -> None:
        # 1. Evaporation.
        for i in range(self.n):
            for j in range(self.n):
                self.pheromone[i][j] *= 1.0 - self.rho

        # 2. Deposit from every ant (Ant System).
        for ant in ants:
            deposit = self.q / ant.tour_length_value
            self._deposit_on_tour(ant.tour, deposit)

        # 3. Elitist deposit on the global-best tour.
        if self.elitist_weight > 0 and self.best_tour is not None:
            deposit = self.elitist_weight * self.q / self.best_length
            self._deposit_on_tour(self.best_tour, deposit)

    def _deposit_on_tour(self, tour: Sequence[int], amount: float) -> None:
        for k in range(len(tour)):
            a = tour[k]
            b = tour[(k + 1) % len(tour)]
            self.pheromone[a][b] += amount
            self.pheromone[b][a] += amount
