"""
Informed search strategies that use domain knowledge via heuristics.

These strategies combine g(n) with h(n) - heuristic estimate to goal.
"""

from .astar import astar_priority
from .greedy import greedy_best_first_priority

__all__ = [
    'astar_priority',
    'greedy_best_first_priority'
]

