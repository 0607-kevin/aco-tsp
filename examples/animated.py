"""Animate how the best tour improves iteration by iteration."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt

from aco import ACOSolver, load_cities
from aco.visualize import animate_tours


def main() -> None:
    points = load_cities(str(ROOT / "data" / "cities.json"), "small")

    solver = ACOSolver(
        points, n_ants=20, n_iterations=60,
        elitist_weight=8.0, seed=7,
    )
    solver.run()

    _, anim = animate_tours(
        points, solver.best_tour_history, solver.history, interval=120
    )
    plt.show()


if __name__ == "__main__":
    main()
