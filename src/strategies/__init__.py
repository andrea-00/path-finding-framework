"""
Search strategies module containing priority functions for different algorithms.
"""

from .uninformed.ucs import uniform_cost_priority
from .uninformed.bfs import breadth_first_priority
from .uninformed.dfs import depth_first_priority
from .informed.astar import astar_priority
from .informed.greedy import greedy_best_first_priority

__all__ = [
    'uniform_cost_priority',
    'breadth_first_priority',
    'depth_first_priority',
    'astar_priority',
    'greedy_best_first_priority'
]

