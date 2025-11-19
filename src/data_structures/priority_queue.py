"""
Priority Queue implementation for informed search strategies.

Used by: Uniform Cost Search, A*, Greedy Best-First Search
"""

import heapq
from typing import List, Tuple, Dict
from src.core.types import AbstractFrontier, Node, StateType


class PriorityQueueFrontier(AbstractFrontier[StateType]):
    """
    Min-heap based priority queue for best-first search strategies.
    
    Maintains nodes ordered by priority (lower value = higher priority).
    Supports efficient:
    - O(log n) insertion
    - O(log n) extraction of minimum
    - O(1) membership testing via state lookup
    
    Attributes:
        heap: Min-heap of (priority, counter, node) tuples
        entry_finder: Dict mapping states to heap entries for fast lookup
        counter: Tie-breaker for nodes with equal priority (FIFO order)
    """
    
    def __init__(self):
        """Initialize an empty priority queue."""
        self.heap: List[Tuple[float, int, Node[StateType]]] = []
        self.entry_finder: Dict[StateType, Tuple[float, int, Node[StateType]]] = {}
        self.counter = 0  # Tie-breaker for stable sorting
    
    def push(self, node: Node[StateType], priority: float) -> None:
        """
        Insert a node with given priority, or update if better priority exists.
        
        Args:
            node: The node to insert
            priority: The priority value (lower = higher priority)
        """
        # Check if state already in frontier
        if node.state in self.entry_finder:
            # Get existing entry
            old_priority, _, _ = self.entry_finder[node.state]
            # Only update if new priority is better (lower)
            if priority < old_priority:
                # Remove old entry (lazy deletion - mark as invalid)
                del self.entry_finder[node.state]
            else:
                # Keep existing entry with better priority
                return
        
        # Add new entry
        entry = (priority, self.counter, node)
        self.entry_finder[node.state] = entry
        heapq.heappush(self.heap, entry)
        self.counter += 1
    
    def pop(self) -> Node[StateType]:
        """
        Remove and return the node with lowest priority.
        
        Returns:
            The node with highest priority (lowest value)
            
        Raises:
            IndexError: If the frontier is empty
        """
        # Pop until we find a valid entry (not lazily deleted)
        while self.heap:
            priority, count, node = heapq.heappop(self.heap)
            
            # Check if this is the current entry for this state
            if node.state in self.entry_finder:
                current_entry = self.entry_finder[node.state]
                # Verify this is the same entry (not outdated)
                if current_entry == (priority, count, node):
                    del self.entry_finder[node.state]
                    return node
        
        raise IndexError("pop from empty priority queue")
    
    def is_empty(self) -> bool:
        """
        Check if the frontier is empty.
        
        Returns:
            True if no valid nodes remain
        """
        return len(self.entry_finder) == 0
    
    def __len__(self) -> int:
        """
        Return the number of nodes in the frontier.
        
        Returns:
            Count of valid nodes (excluding lazily deleted entries)
        """
        return len(self.entry_finder)
    
    def __contains__(self, node: Node[StateType]) -> bool:
        """
        Check if a node's state is in the frontier.
        
        Args:
            node: The node to check
            
        Returns:
            True if a node with this state exists in frontier
        """
        return node.state in self.entry_finder

