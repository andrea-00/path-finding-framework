"""
Uninformed search strategies that don't use domain knowledge.

These strategies rely only on g(n) - the path cost from initial state.
"""

from .ucs import uniform_cost_priority
from .bfs import breadth_first_priority
from .dfs import depth_first_priority

__all__ = [
    'uniform_cost_priority',
    'breadth_first_priority',
    'depth_first_priority'
]

