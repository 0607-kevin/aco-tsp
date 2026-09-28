"""A single ant builds a TSP tour following the pheromone/desirability rule."""

from __future__ import annotations

import random
from typing import List, Sequence, Tuple

from .utils import tour_length


class Ant:
    def __init__(self, start_city: int = 0):
        self.start_city = start_city
        self.tour: List[int] = []
        self.tour_length_value: float = 0.0

    # ------------------------------------------------------------------
    def construct(
        self,
        n_cities: int,
        dist: Sequence[Sequence[float]],
        pheromone: Sequence[Sequence[float]],
        alpha: float,
        beta: float,
        rng: random.Random,
    ) -> List[int]:
        visited = [False] * n_cities
        city = self.start_city
        self.tour = [city]
        visited[city] = True

        for _ in range(n_cities - 1):
            choices: List[Tuple[int, float]] = []
            for j in range(n_cities):
                if visited[j]:
                    continue
                d = dist[city][j]
                tau = pheromone[city][j] ** alpha
                eta = (1.0 / d) ** beta
                choices.append((j, tau * eta))

            city = self._roulette(choices, rng)
            self.tour.append(city)
            visited[city] = True

        self.tour_length_value = tour_length(self.tour, dist)
        return self.tour

    # ------------------------------------------------------------------
    @staticmethod
    def _roulette(choices: Sequence[Tuple[int, float]],
                  rng: random.Random) -> int:
        total = sum(weight for _, weight in choices)
        pick = rng.random() * total
        cumulative = 0.0
        for city, weight in choices:
            cumulative += weight
            if pick <= cumulative:
                return city
        # Fallback for any floating-point edge case.
        return choices[-1][0]
