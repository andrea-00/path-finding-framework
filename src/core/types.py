"""
Core Type Definitions and Abstract Interfaces for the Pathfinding Framework.

This module defines the contracts (interfaces) that enable Dependency Injection
and Inversion of Control in the search engine architecture.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Tuple, Optional, Generic, TypeVar
from dataclasses import dataclass


# Type variable for generic state representation
StateType = TypeVar('StateType')


@dataclass
class Node(Generic[StateType]):
    """
    Represents a node in the search tree.
    
    Attributes:
        state: The state representation at this node
        parent: Reference to the parent node (None for root)
        action: The action taken to reach this state from parent
        path_cost: The cumulative cost g(n) from the initial state
        depth: The depth of this node in the search tree
    """
    state: StateType
    parent: Optional['Node[StateType]'] = None
    action: Optional[Any] = None
    path_cost: float = 0.0
    depth: int = 0
    
    def __hash__(self) -> int:
        """Enable nodes to be used in sets/dicts via state hashing."""
        return hash(self.state)
    
    def __eq__(self, other: object) -> bool:
        """Equality based on state comparison."""
        if not isinstance(other, Node):
            return NotImplemented
        return self.state == other.state


class AbstractState(ABC):
    """
    Abstract interface for problem states.
    
    Concrete states must be hashable to support Graph Search
    (closed set / visited tracking).
    """
    
    @abstractmethod
    def __hash__(self) -> int:
        """Return hash of the state for use in sets and dictionaries."""
        pass
    
    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Check equality with another state."""
        pass
    
    @abstractmethod
    def __repr__(self) -> str:
        """String representation for debugging."""
        pass


class AbstractProblem(ABC, Generic[StateType]):
    """
    Abstract interface for problem definition.
    
    Defines the problem space: initial state, goal test, and successor function.
    This interface enables the search engine to be problem-agnostic.
    """
    
    @abstractmethod
    def initial_state(self) -> StateType:
        """
        Return the initial state of the problem.
        
        Returns:
            The starting state for the search
        """
        pass
    
    @abstractmethod
    def is_goal(self, state: StateType) -> bool:
        """
        Test whether the given state is a goal state.
        
        Args:
            state: The state to test
            
        Returns:
            True if state is a goal state, False otherwise
        """
        pass
    
    @abstractmethod
    def get_successors(self, state: StateType) -> List[Tuple[StateType, Any, float]]:
        """
        Generate successor states from the current state.
        
        Args:
            state: The current state to expand
            
        Returns:
            List of tuples (next_state, action, step_cost) where:
                - next_state: The resulting state after taking the action
                - action: The action taken (can be any type)
                - step_cost: The cost of taking this action (non-negative)
        """
        pass


class AbstractHeuristic(ABC, Generic[StateType]):
    """
    Abstract interface for heuristic functions.
    
    Used by informed search strategies (A*, Greedy Best-First Search).
    The heuristic provides an estimate h(n) of the cost from state to goal.
    """
    
    @abstractmethod
    def h(self, state: StateType) -> float:
        """
        Calculate the heuristic estimate from state to goal.
        
        Args:
            state: The state to evaluate
            
        Returns:
            Estimated cost from state to nearest goal (non-negative)
        """
        pass
    
    @abstractmethod
    def is_admissible(self) -> bool:
        """
        Indicate whether this heuristic is admissible (never overestimates).
        
        Returns:
            True if heuristic is admissible, False otherwise
        """
        pass
    
    @abstractmethod
    def is_consistent(self) -> bool:
        """
        Indicate whether this heuristic is consistent (monotonic).
        
        A consistent heuristic satisfies: h(n) <= cost(n, n') + h(n')
        for every node n and successor n'.
        
        Returns:
            True if heuristic is consistent, False otherwise
        """
        pass


class AbstractFrontier(ABC, Generic[StateType]):
    """
    Abstract interface for frontier data structures.
    
    The frontier (open set) stores nodes to be expanded, ordered according
    to the search strategy. Different strategies require different data structures:
    - Stack (LIFO) for DFS
    - Queue (FIFO) for BFS
    - Priority Queue for UCS, A*, Greedy
    """
    
    @abstractmethod
    def push(self, node: Node[StateType], priority: float) -> None:
        """
        Insert a node into the frontier with the given priority.
        
        Args:
            node: The node to insert
            priority: The priority value (lower = higher priority for min-heap)
        """
        pass
    
    @abstractmethod
    def pop(self) -> Node[StateType]:
        """
        Remove and return the node with highest priority.
        
        Returns:
            The node with highest priority according to the strategy
            
        Raises:
            IndexError: If the frontier is empty
        """
        pass
    
    @abstractmethod
    def is_empty(self) -> bool:
        """
        Check if the frontier is empty.
        
        Returns:
            True if no nodes remain in the frontier, False otherwise
        """
        pass
    
    @abstractmethod
    def __len__(self) -> int:
        """
        Return the number of nodes in the frontier.
        
        Returns:
            Count of nodes currently in the frontier
        """
        pass
    
    @abstractmethod
    def __contains__(self, node: Node[StateType]) -> bool:
        """
        Check if a node (by state) is already in the frontier.
        
        Args:
            node: The node to check
            
        Returns:
            True if a node with the same state exists in frontier
        """
        pass


class NullHeuristic(AbstractHeuristic[StateType]):
    """
    Null heuristic that always returns 0.
    
    Used by uninformed search strategies (UCS, BFS, DFS) that don't use heuristics.
    This implements the Null Object pattern.
    """
    
    def h(self, state: StateType) -> float:
        """Return zero for all states."""
        return 0.0
    
    def is_admissible(self) -> bool:
        """Null heuristic is trivially admissible."""
        return True
    
    def is_consistent(self) -> bool:
        """Null heuristic is trivially consistent."""
        return True


@dataclass
class SearchResult(Generic[StateType]):
    """
    Result object returned by the search engine.
    
    Attributes:
        success: Whether a goal state was found
        goal_node: The goal node if found, None otherwise
        nodes_expanded: Number of nodes expanded during search
        nodes_generated: Total number of nodes generated
        max_frontier_size: Maximum size of the frontier during search
        path: List of states from initial to goal (if success)
        actions: List of actions taken from initial to goal (if success)
        total_cost: Total path cost g(n) of the solution
    """
    success: bool
    goal_node: Optional[Node[StateType]] = None
    nodes_expanded: int = 0
    nodes_generated: int = 0
    max_frontier_size: int = 0
    path: List[StateType] = None
    actions: List[Any] = None
    total_cost: float = float('inf')
    
    def __post_init__(self):
        """Initialize empty lists for path and actions if None."""
        if self.path is None:
            self.path = []
        if self.actions is None:
            self.actions = []

