"""
Breadth-First Search (BFS) priority function.

BFS expands nodes in order of depth (shallowest first).
Optimal for problems with uniform edge costs.
"""

from src.core.types import Node, AbstractHeuristic, StateType


def breadth_first_priority(node: Node[StateType], heuristic: AbstractHeuristic[StateType]) -> float:
    """
    Compute priority for Breadth-First Search.
    
    Priority = depth of node in search tree
    
    Nodes at shallower depths are expanded before deeper nodes,
    ensuring the shallowest goal is found first.
    
    Args:
        node: The node to compute priority for
        heuristic: Ignored (BFS doesn't use heuristics)
        
    Returns:
        The depth of the node as priority
    """
    return float(node.depth)

