"""Distance matrix, tour metrics and data loading helpers."""

from __future__ import annotations
import json
import math
from typing import List, Sequence, Tuple

Point = Tuple[float, float]


def euclidean_distance(p: Point, q: Point) -> float:
    return math.hypot(p[0] - q[0], p[1] - q[1])


def build_distance_matrix(points: Sequence[Point]) -> List[List[float]]:
    n = len(points)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = euclidean_distance(points[i], points[j])
            matrix[i][j] = d
            matrix[j][i] = d
    return matrix


def tour_length(tour: Sequence[int], dist: Sequence[Sequence[float]]) -> float:
    """Length of a closed tour (last city connects back to the first)."""
    total = 0.0
    for i in range(len(tour)):
        total += dist[tour[i]][tour[(i + 1) % len(tour)]]
    return total


def nearest_neighbor_tour(dist: Sequence[Sequence[float]],
                          start: int = 0) -> List[int]:
    """Greedy nearest-neighbour tour; a useful baseline."""
    n = len(dist)
    unvisited = set(range(n))
    tour = [start]
    unvisited.remove(start)
    current = start
    while unvisited:
        nxt = min(unvisited, key=lambda j: dist[current][j])
        tour.append(nxt)
        unvisited.remove(nxt)
        current = nxt
    return tour


def load_cities(path: str, instance: str = "small") -> List[Point]:
    """Load a named instance from a JSON file.

    The JSON structure is::

        {"instances": {"small": [{"x": .., "y": ..}, ...], ...}}
    """
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    raw = data["instances"][instance]
    return [(float(c["x"]), float(c["y"])) for c in raw]
