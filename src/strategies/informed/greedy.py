"""
Greedy Best-First Search priority function.

Greedy Search expands nodes that appear closest to the goal based solely on h(n).
Does not guarantee optimal solutions but can be very fast.
"""

from src.core.types import Node, AbstractHeuristic, StateType


def greedy_best_first_priority(node: Node[StateType], heuristic: AbstractHeuristic[StateType]) -> float:
    """
    Compute priority for Greedy Best-First Search.
    
    Priority = h(n) = heuristic estimate from node to goal
    
    Greedy search ignores the actual path cost g(n) and focuses solely
    on the estimated distance to the goal. This makes it fast but
    does not guarantee optimal solutions.
    
    Args:
        node: The node to compute priority for
        heuristic: Heuristic function providing h(n) estimates
        
    Returns:
        The h(n) value as priority
    """
    return heuristic.h(node.state)

