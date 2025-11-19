"""
Depth-First Search (DFS) priority function.

DFS expands nodes in order of depth (deepest first).
Explores as deep as possible before backtracking.
"""

from src.core.types import Node, AbstractHeuristic, StateType


def depth_first_priority(node: Node[StateType], heuristic: AbstractHeuristic[StateType]) -> float:
    """
    Compute priority for Depth-First Search.
    
    Priority = -depth of node in search tree
    
    Negative depth ensures deeper nodes have lower priority values
    (higher priority in min-heap), causing depth-first exploration.
    
    Args:
        node: The node to compute priority for
        heuristic: Ignored (DFS doesn't use heuristics)
        
    Returns:
        The negative depth of the node as priority
    """
    return -float(node.depth)

