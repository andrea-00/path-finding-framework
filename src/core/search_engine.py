"""
Core Search Engine Implementation.

This module contains the problem-agnostic search engine that uses dependency
injection to separate the search algorithm from problem-specific logic.
"""

from typing import Set, Dict, Optional, Callable, Generic
from .types import (
    AbstractProblem,
    AbstractFrontier,
    AbstractHeuristic,
    Node,
    SearchResult,
    NullHeuristic,
    StateType
)


class SearchEngine(Generic[StateType]):
    """
    Problem-agnostic search engine using Dependency Injection.
    
    The engine orchestrates the search loop while delegating problem-specific
    logic to injected components:
    - Problem: Defines initial state, goal test, and successors
    - Frontier: Determines node expansion order (strategy)
    - Priority Function: Computes node priority based on strategy
    - Heuristic: Provides h(n) estimates for informed strategies
    
    Attributes:
        problem: The problem definition
        frontier: The frontier data structure
        priority_fn: Function that computes priority for a node
        heuristic: Heuristic function (NullHeuristic for uninformed search)
        graph_search: If True, use closed set to avoid revisiting states
        allow_revisit: If True, allow revisiting states with better cost
    
    Notes:
        For graphs with NON-NEGATIVE edge costs:
            - Use graph_search=True, allow_revisit=False (default, optimal)
        
        For graphs with NEGATIVE edge costs:
            - Use graph_search=True, allow_revisit=True
            - This allows finding better paths to already-visited states
            - Warning: May not terminate if negative cycles exist
    """
    
    def __init__(
        self,
        problem: AbstractProblem[StateType],
        frontier: AbstractFrontier[StateType],
        priority_fn: Callable[[Node[StateType], AbstractHeuristic[StateType]], float],
        heuristic: Optional[AbstractHeuristic[StateType]] = None,
        graph_search: bool = True,
        allow_revisit: bool = False
    ):
        """
        Initialize the search engine with injected dependencies.
        
        Args:
            problem: Problem definition (initial state, goal test, successors)
            frontier: Frontier data structure for node ordering
            priority_fn: Function computing priority from (node, heuristic)
            heuristic: Heuristic function (optional, defaults to NullHeuristic)
            graph_search: If True, track visited states (Graph Search vs Tree Search)
            allow_revisit: If True, allow re-expanding states with improved cost.
                          Required for graphs with negative edge weights.
        
        Important:
            The default settings (graph_search=True, allow_revisit=False) assume
            NON-NEGATIVE edge costs. For problems with negative edges, set
            allow_revisit=True to find optimal solutions.
        """
        self.problem = problem
        self.frontier = frontier
        self.priority_fn = priority_fn
        self.heuristic = heuristic if heuristic is not None else NullHeuristic()
        self.graph_search = graph_search
        self.allow_revisit = allow_revisit
        
        # Statistics tracking
        self.nodes_expanded = 0
        self.nodes_generated = 0
        self.max_frontier_size = 0
        
        # Closed set for Graph Search
        self.closed: Set[StateType] = set()
        
        # Best cost tracking for allow_revisit mode
        # Maps state -> best path cost found so far
        self.best_cost: Dict[StateType, float] = {}
    
    def search(self) -> SearchResult[StateType]:
        """
        Execute the search algorithm.
        
        This is the core search loop that:
        1. Initializes frontier with root node
        2. Repeatedly pops best node according to priority
        3. Tests for goal state
        4. Expands node by generating successors
        5. Adds successors to frontier with computed priorities
        
        The behavior adapts based on configuration:
        - graph_search=False: Tree search (may revisit states)
        - graph_search=True, allow_revisit=False: Classic graph search
          (assumes non-negative costs)
        - graph_search=True, allow_revisit=True: Graph search with cost tracking
          (handles negative edges correctly)
        
        Returns:
            SearchResult containing solution path and statistics
        """
        # Reset statistics
        self.nodes_expanded = 0
        self.nodes_generated = 0
        self.max_frontier_size = 0
        self.closed.clear()
        self.best_cost.clear()
        
        # Initialize with root node
        initial_state = self.problem.initial_state()
        root_node = Node(
            state=initial_state,
            parent=None,
            action=None,
            path_cost=0.0,
            depth=0
        )
        
        # Add root to frontier
        priority = self.priority_fn(root_node, self.heuristic)
        self.frontier.push(root_node, priority)
        self.nodes_generated = 1
        
        # Track initial state cost
        if self.allow_revisit:
            self.best_cost[initial_state] = 0.0
        
        # Main search loop
        while not self.frontier.is_empty():
            # Update statistics
            self.max_frontier_size = max(self.max_frontier_size, len(self.frontier))
            
            # Get next node to expand
            current_node = self.frontier.pop()
            
            # Goal test
            if self.problem.is_goal(current_node.state):
                return self._build_success_result(current_node)
            
            # Graph Search: Handle visited states
            if self.graph_search:
                if self.allow_revisit:
                    # Check if we've found a better path to this state
                    current_cost = current_node.path_cost
                    best = self.best_cost.get(current_node.state, float('inf'))
                    
                    if current_cost > best:
                        # We've already found a better path to this state
                        continue
                    
                    # Update best cost for this state
                    self.best_cost[current_node.state] = current_cost
                else:
                    # Classic graph search: skip if already visited
                    # NOTE: This assumes NON-NEGATIVE edge costs
                    if current_node.state in self.closed:
                        continue
                    
                    # Mark as visited
                    self.closed.add(current_node.state)
            
            # Expand node
            self.nodes_expanded += 1
            self._expand_node(current_node)
        
        # No solution found
        return self._build_failure_result()
    
    def _expand_node(self, node: Node[StateType]) -> None:
        """
        Expand a node by generating its successors and adding them to frontier.
        
        Args:
            node: The node to expand
        """
        # Get successors from problem definition
        successors = self.problem.get_successors(node.state)
        
        for next_state, action, step_cost in successors:
            # Calculate new path cost
            new_cost = node.path_cost + step_cost
            
            # Graph Search: Handle visited states
            if self.graph_search:
                if self.allow_revisit:
                    # Check if this path is better than any we've seen
                    best = self.best_cost.get(next_state, float('inf'))
                    if new_cost >= best:
                        # Not an improvement, skip
                        continue
                    # Note: We don't update best_cost here, we do it when popping
                    # This allows multiple paths to compete in the frontier
                else:
                    # Classic graph search: skip if already in closed set
                    if next_state in self.closed:
                        continue
            
            # Create child node
            child_node = Node(
                state=next_state,
                parent=node,
                action=action,
                path_cost=new_cost,
                depth=node.depth + 1
            )
            
            # Compute priority and add to frontier
            priority = self.priority_fn(child_node, self.heuristic)
            self.frontier.push(child_node, priority)
            self.nodes_generated += 1
    
    def _build_success_result(self, goal_node: Node[StateType]) -> SearchResult[StateType]:
        """
        Build a SearchResult for a successful search.
        
        Args:
            goal_node: The goal node found
            
        Returns:
            SearchResult with solution path and statistics
        """
        path, actions = self._reconstruct_path(goal_node)
        
        return SearchResult(
            success=True,
            goal_node=goal_node,
            nodes_expanded=self.nodes_expanded,
            nodes_generated=self.nodes_generated,
            max_frontier_size=self.max_frontier_size,
            path=path,
            actions=actions,
            total_cost=goal_node.path_cost
        )
    
    def _build_failure_result(self) -> SearchResult[StateType]:
        """
        Build a SearchResult for a failed search.
        
        Returns:
            SearchResult indicating no solution found
        """
        return SearchResult(
            success=False,
            goal_node=None,
            nodes_expanded=self.nodes_expanded,
            nodes_generated=self.nodes_generated,
            max_frontier_size=self.max_frontier_size,
            path=[],
            actions=[],
            total_cost=float('inf')
        )
    
    def _reconstruct_path(self, goal_node: Node[StateType]) -> tuple:
        """
        Reconstruct the path from initial state to goal by following parent links.
        
        Args:
            goal_node: The goal node to trace back from
            
        Returns:
            Tuple of (path, actions) where:
                - path: List of states from initial to goal
                - actions: List of actions taken
        """
        path = []
        actions = []
        current = goal_node
        
        # Trace back to root
        while current is not None:
            path.append(current.state)
            if current.action is not None:
                actions.append(current.action)
            current = current.parent
        
        # Reverse to get initial -> goal order
        path.reverse()
        actions.reverse()
        
        return path, actions

