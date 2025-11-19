"""
Uniform Cost Search (UCS) priority function.

UCS expands nodes in order of path cost g(n) from the initial state.
Guarantees optimal solutions for problems with non-negative edge costs.
"""

from src.core.types import Node, AbstractHeuristic, StateType


def uniform_cost_priority(node: Node[StateType], heuristic: AbstractHeuristic[StateType]) -> float:
    """
    Compute priority for Uniform Cost Search.
    
    Priority = g(n) = path cost from initial state to node
    
    Lower priority values are expanded first, so nodes with lower
    accumulated cost are explored before higher-cost nodes.
    
    Args:
        node: The node to compute priority for
        heuristic: Ignored (UCS doesn't use heuristics)
        
    Returns:
        The path cost g(n) as priority
    """
    return node.path_cost

