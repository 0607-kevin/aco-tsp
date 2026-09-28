# aco-tsp

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://img.shields.io/badge/tests-9%20passed-brightgreen)

Solving the **Travelling Salesman Problem** with **Ant Colony Optimization**
(Ant System with an optional elitist strategy), implemented from scratch in
Python, with tour plots, convergence curves and an iteration-by-iteration
animation.

ACO is a swarm-intelligence metaheuristic: artificial ants construct candidate
tours biased by pheromone trails (reinforced on good edges) and a distance
heuristic. It is a natural fit for combinatorial routing problems such as the
TSP and its many variants (vehicle routing, job sequencing, ...).

## How it works

At each iteration every ant builds a complete tour. From city `i` it picks the
next city `j` probabilistically:

```
P(i -> j) = tau(i,j)^alpha * eta(i,j)^beta  /  sum over unvisited k
```

where `tau` is the pheromone level and `eta = 1 / distance(i,j)` is the
heuristic desirability. Afterwards pheromone evaporates by factor `rho` and
each ant deposits `Q / tour_length` on the edges it used. Elitist ACO adds an
extra deposit on the global-best tour.

| Parameter | Role |
|-----------|------|
| `alpha` | pheromone importance |
| `beta` | heuristic (distance) importance |
| `rho` | evaporation rate |
| `Q` | deposit scaling constant |
| `elitist_weight` | extra reinforcement of the best tour |

## Project layout

```
aco-tsp/
├── aco/
│   ├── ant.py          # tour construction + roulette selection
│   ├── colony.py       # main ACO loop, pheromone update
│   ├── utils.py        # distance matrix, tour length, data loading
│   └── visualize.py    # tours, convergence, animation
├── data/
│   └── cities.json     # small (15) and medium (30) instances
├── examples/
│   ├── demo.py         # solve + compare with nearest neighbour
│   ├── benchmark.py    # beta / rho sensitivity
│   └── animated.py     # tour improvement animation
└── tests/
    └── test_aco.py
```

## Installation

```bash
git clone https://github.com/0607-kevin/aco-tsp.git
cd aco-tsp
pip install -r requirements.txt
```

## Quick start

```python
from aco import ACOSolver

points = [(0, 0), (3, 0), (3, 4), (0, 4)]
solver = ACOSolver(points, n_ants=20, n_iterations=100,
                   elitist_weight=10.0, seed=42)
best_tour, best_length = solver.run()
```

Run the examples:

```bash
python examples/demo.py         # full solve + convergence plot
python examples/benchmark.py    # parameter sensitivity
python examples/animated.py     # animated tour evolution
```

## Sample results

On the 30-city `medium` instance:

```
nearest neighbour : 618.54
ACO best          : 494.87
improvement       : 20.0%
```

Parameter sensitivity (final tour length):

```
config        final length
beta=2              499.79
beta=3              499.79
beta=5              503.87
rho=0.05            503.74
rho=0.3             502.94
```

The best-so-far curve is non-increasing by construction, and pheromone levels
stay positive and symmetric.

## Tests

```bash
python tests/test_aco.py
```

The 9 tests cover the distance matrix, closed tour length, ant validity,
monotonic convergence, pheromone properties, and verify that ACO matches or
beats the nearest-neighbour baseline.

## References

- Dorigo, M., Maniezzo, V., Colorni, A. (1996). *Ant System: Optimization by a
  Colony of Cooperating Agents.*
- Dorigo, M., Stützle, T. (2004). *Ant Colony Optimization.* MIT Press.
- Dorigo, M., Gambardella, L. M. (1997). *Ant Colony System: A Cooperative
  Learning Approach to the Traveling Salesman Problem.*

## License

Released under the [MIT License](LICENSE).
