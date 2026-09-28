"""Benchmark how beta (heuristic strength) and rho (evaporation) affect
convergence on the same instance.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt

from aco import ACOSolver, load_cities
from aco.visualize import plot_convergence


def main() -> None:
    points = load_cities(str(ROOT / "data" / "cities.json"), "medium")

    configs = [
        ("beta=2", dict(beta=2.0)),
        ("beta=3", dict(beta=3.0)),
        ("beta=5", dict(beta=5.0)),
        ("rho=0.05", dict(rho=0.05)),
        ("rho=0.3", dict(rho=0.3)),
    ]

    histories = {}
    print(f"{'config':<10}{'final length':>14}")
    for name, overrides in configs:
        params = dict(n_ants=30, n_iterations=80, rho=0.1, beta=3.0,
                      elitist_weight=8.0, seed=42)
        params.update(overrides)
        solver = ACOSolver(points, **params)
        _, best = solver.run()
        histories[name] = solver.history
        print(f"{name:<10}{best:>14.2f}")

    plot_convergence(histories, title="Parameter sensitivity")
    plt.show()


if __name__ == "__main__":
    main()
