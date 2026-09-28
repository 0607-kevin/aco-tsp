"""Solve a TSP instance with ACO and compare against nearest neighbour."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt

from aco import ACOSolver, load_cities, nearest_neighbor_tour, tour_length
from aco.visualize import plot_convergence, plot_tour


def main() -> None:
    data_path = ROOT / "data" / "cities.json"
    points = load_cities(str(data_path), instance="medium")

    solver = ACOSolver(
        points,
        n_ants=30,
        n_iterations=120,
        alpha=1.0,
        beta=3.0,
        rho=0.1,
        elitist_weight=10.0,
        seed=42,
    )
    best_tour, best_length = solver.run()

    nn_tour = nearest_neighbor_tour(solver.dist, start=0)
    nn_length = tour_length(nn_tour, solver.dist)

    print(f"cities            : {len(points)}")
    print(f"nearest neighbour : {nn_length:.2f}")
    print(f"ACO best          : {best_length:.2f}")
    print(f"improvement       : "
          f"{(1 - best_length / nn_length) * 100:.1f}%")

    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    plot_tour(points, best_tour, ax=axes[0],
              title=f"ACO tour (length={best_length:.2f})")
    plot_convergence({"ACO": solver.history}, ax=axes[1])
    plt.show()


if __name__ == "__main__":
    main()
