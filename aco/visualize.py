"""Matplotlib visualisation: tours, convergence curves and iteration animation."""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

Point = Tuple[float, float]


def plot_tour(points: Sequence[Point], tour: Sequence[int],
              ax=None, title: str = "", color: str = "#1565c0"):
    created = ax is None
    if created:
        fig, ax = plt.subplots(figsize=(7, 7))

    xs = [points[c][0] for c in tour] + [points[tour[0]][0]]
    ys = [points[c][1] for c in tour] + [points[tour[0]][1]]
    ax.plot(xs, ys, color=color, linewidth=1.6, zorder=3)
    ax.scatter([p[0] for p in points], [p[1] for p in points],
               s=28, color="#ef6c00", zorder=4)
    for i, (x, y) in enumerate(points):
        ax.annotate(str(i), (x, y), textcoords="offset points",
                    xytext=(4, 4), fontsize=7, color="#424242")
    ax.set_aspect("equal")
    ax.grid(alpha=0.25)
    ax.set_title(title)
    return ax


def plot_convergence(histories: Dict[str, Sequence[float]], ax=None,
                     title: str = "Convergence"):
    created = ax is None
    if created:
        fig, ax = plt.subplots(figsize=(8, 5))
    for name, history in histories.items():
        ax.plot(range(1, len(history) + 1), history, marker="o",
                markersize=3, label=name)
    ax.set_xlabel("iteration")
    ax.set_ylabel("best tour length")
    ax.set_title(title)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    return ax


def animate_tours(points: Sequence[Point],
                  tour_history: Sequence[Sequence[int]],
                  length_history: Sequence[float],
                  interval: int = 120):
    """Animate the best tour at every iteration."""
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter([p[0] for p in points], [p[1] for p in points],
               s=28, color="#ef6c00", zorder=4)
    ax.set_aspect("equal")
    ax.grid(alpha=0.25)
    (line,) = ax.plot([], [], color="#1565c0", linewidth=1.6, zorder=3)

    def update(frame):
        tour = tour_history[frame]
        line.set_data(
            [points[c][0] for c in tour] + [points[tour[0]][0]],
            [points[c][1] for c in tour] + [points[tour[0]][1]],
        )
        ax.set_title(f"iteration {frame + 1} | length={length_history[frame]:.2f}")
        return (line,)

    anim = FuncAnimation(fig, update, frames=len(tour_history),
                         interval=interval, blit=True, repeat=False)
    return fig, anim
