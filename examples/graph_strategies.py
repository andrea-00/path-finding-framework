"""
Problem-specific priority functions for graph pathfinding with negative cycles.

These strategies extend the framework's generic priority functions with 
protection against negative cycles by monitoring path length.

Design Note:
    These are PROBLEM-SPECIFIC implementations and belong in /examples/, 
    not in /src/. The core framework remains problem-agnostic.
"""

from src.core.types import Node, AbstractHeuristic, StateType


class NegativeCycleDetectedError(Exception):
    """
    Exception raised when a negative cycle is detected in the graph.
    
    A negative cycle exists if the search explores a path longer than
    the number of nodes in the graph, indicating a cycle that reduces cost.
    """
    pass


def robust_uniform_cost_priority(
    node: Node[StateType], 
    heuristic: AbstractHeuristic[StateType],
    max_nodes: int
) -> float:
    """
    Uniform Cost Search priority with negative cycle detection.
    
    This is a problem-specific wrapper around the standard UCS priority
    function that adds protection against negative cycles in graphs.
    
    Strategy:
        If the path length (depth) exceeds the number of nodes in the graph,
        a cycle must exist. For graphs with negative edges, this could be
        a negative cycle that would cause infinite looping.
    
    Args:
        node: The node to compute priority for
        heuristic: Ignored (UCS doesn't use heuristics)
        max_nodes: Maximum number of nodes in the graph
        
    Returns:
        The path cost g(n) as priority
        
    Raises:
        NegativeCycleDetectedError: If path length exceeds number of nodes,
            indicating a potential negative cycle
    
    Example:
        >>> from examples.graph_strategies import robust_uniform_cost_priority
        >>> from functools import partial
        >>> 
        >>> # Create problem-specific priority function
        >>> priority_fn = partial(robust_uniform_cost_priority, max_nodes=10)
        >>> 
        >>> engine = SearchEngine(
        ...     problem=graph_problem,
        ...     frontier=PriorityQueueFrontier(),
        ...     priority_fn=priority_fn,
        ...     heuristic=None
        ... )
    """
    # Check for negative cycle by path length
    path_length = node.depth + 1  # depth is 0-indexed, add 1 for actual length
    
    if path_length > max_nodes:
        raise NegativeCycleDetectedError(
            f"Negative cycle detected: path length ({path_length}) exceeds "
            f"number of nodes ({max_nodes}). This indicates a cycle with "
            f"negative total cost that would cause infinite looping."
        )
    
    # Standard UCS priority: g(n)
    return node.path_cost


def robust_astar_priority(
    node: Node[StateType], 
    heuristic: AbstractHeuristic[StateType],
    max_nodes: int
) -> float:
    """
    A* Search priority with negative cycle detection.
    
    This is a problem-specific wrapper around the standard A* priority
    function that adds protection against negative cycles in graphs.
    
    Strategy:
        If the path length (depth) exceeds the number of nodes in the graph,
        a cycle must exist. For graphs with negative edges, this could be
        a negative cycle that would cause infinite looping.
    
    Note:
        A* with admissible heuristics is NOT guaranteed to be optimal in
        graphs with negative edges. This function is provided for completeness
        but should be used with caution. Consider using robust_uniform_cost_priority
        instead for graphs with negative edges.
    
    Args:
        node: The node to compute priority for
        heuristic: Heuristic function providing h(n) estimates
        max_nodes: Maximum number of nodes in the graph
        
    Returns:
        The f(n) = g(n) + h(n) value as priority
        
    Raises:
        NegativeCycleDetectedError: If path length exceeds number of nodes,
            indicating a potential negative cycle
    
    Example:
        >>> from examples.graph_strategies import robust_astar_priority
        >>> from functools import partial
        >>> 
        >>> # Create problem-specific priority function
        >>> priority_fn = partial(robust_astar_priority, max_nodes=10)
        >>> 
        >>> engine = SearchEngine(
        ...     problem=graph_problem,
        ...     frontier=PriorityQueueFrontier(),
        ...     priority_fn=priority_fn,
        ...     heuristic=my_heuristic
        ... )
    """
    # Check for negative cycle by path length
    path_length = node.depth + 1  # depth is 0-indexed, add 1 for actual length
    
    if path_length > max_nodes:
        raise NegativeCycleDetectedError(
            f"Negative cycle detected: path length ({path_length}) exceeds "
            f"number of nodes ({max_nodes}). This indicates a cycle with "
            f"negative total cost that would cause infinite looping."
        )
    
    # Standard A* priority: f(n) = g(n) + h(n)
    g_n = node.path_cost
    h_n = heuristic.h(node.state)
    f_n = g_n + h_n
    return f_n


def create_robust_priority_function(base_priority_fn, max_nodes: int):
    """
    Factory function to create a robust priority function from any base function.
    
    This is a more generic approach that wraps any priority function with
    negative cycle detection.
    
    Args:
        base_priority_fn: The base priority function to wrap
        max_nodes: Maximum number of nodes in the graph
        
    Returns:
        A wrapped priority function with cycle detection
        
    Example:
        >>> from src.strategies import uniform_cost_priority
        >>> from examples.graph_strategies import create_robust_priority_function
        >>> 
        >>> robust_ucs = create_robust_priority_function(
        ...     uniform_cost_priority, 
        ...     max_nodes=10
        ... )
        >>> 
        >>> engine = SearchEngine(
        ...     problem=graph_problem,
        ...     frontier=PriorityQueueFrontier(),
        ...     priority_fn=robust_ucs,
        ...     heuristic=None
        ... )
    """
    def wrapped_priority_fn(node: Node[StateType], heuristic: AbstractHeuristic[StateType]) -> float:
        # Check for negative cycle
        path_length = node.depth + 1
        
        if path_length > max_nodes:
            raise NegativeCycleDetectedError(
                f"Negative cycle detected: path length ({path_length}) exceeds "
                f"number of nodes ({max_nodes})."
            )
        
        # Call the base priority function
        return base_priority_fn(node, heuristic)
    
    return wrapped_priority_fn


# Example usage documentation
if __name__ == "__main__":
    print(__doc__)
    print("\nExample Usage:")
    print("-" * 70)
    print("""
from functools import partial
from src.core import SearchEngine
from src.data_structures import PriorityQueueFrontier
from examples.graph_strategies import robust_uniform_cost_priority

# Method 1: Use partial to bind max_nodes
priority_fn = partial(robust_uniform_cost_priority, max_nodes=10)

engine = SearchEngine(
    problem=my_graph_problem,
    frontier=PriorityQueueFrontier(),
    priority_fn=priority_fn,
    heuristic=None,
    graph_search=True
)

try:
    result = engine.search()
    if result.success:
        print(f"Solution found: {result.path}")
except NegativeCycleDetectedError as e:
    print(f"Error: {e}")
    print("The graph contains a negative cycle!")

# Method 2: Use the factory function
from src.strategies import uniform_cost_priority
from examples.graph_strategies import create_robust_priority_function

robust_ucs = create_robust_priority_function(uniform_cost_priority, max_nodes=10)

engine = SearchEngine(
    problem=my_graph_problem,
    frontier=PriorityQueueFrontier(),
    priority_fn=robust_ucs,
    heuristic=None
)
""")
    print("-" * 70)

