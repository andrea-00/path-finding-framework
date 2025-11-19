"""
A* Search priority function.

A* combines actual cost g(n) with heuristic estimate h(n).
Guarantees optimal solutions when heuristic is admissible.
"""

from src.core.types import Node, AbstractHeuristic, StateType


def astar_priority(node: Node[StateType], heuristic: AbstractHeuristic[StateType]) -> float:
    """
    Compute priority for A* Search.
    
    Priority = f(n) = g(n) + h(n)
    
    Where:
    - g(n) = actual path cost from initial state to node
    - h(n) = heuristic estimate from node to goal
    
    A* is optimal if h(n) is admissible (never overestimates).
    A* is optimally efficient if h(n) is consistent (monotonic).
    
    Args:
        node: The node to compute priority for
        heuristic: Heuristic function providing h(n) estimates
        
    Returns:
        The f(n) = g(n) + h(n) value as priority
    """
    g_n = node.path_cost
    h_n = heuristic.h(node.state)
    f_n = g_n + h_n
    return f_n

