"""
FIFO Queue implementation for Breadth-First Search.

Used by: BFS (uninformed search)
"""

from collections import deque
from typing import Set
from src.core.types import AbstractFrontier, Node, StateType


class FIFOQueueFrontier(AbstractFrontier[StateType]):
    """
    First-In-First-Out queue for Breadth-First Search.
    
    Maintains nodes in order of insertion, expanding nodes in the order
    they were discovered (shallowest nodes first).
    
    Attributes:
        queue: Deque for efficient O(1) operations at both ends
        state_set: Set of states for O(1) membership testing
    """
    
    def __init__(self):
        """Initialize an empty FIFO queue."""
        self.queue: deque[Node[StateType]] = deque()
        self.state_set: Set[StateType] = set()
    
    def push(self, node: Node[StateType], priority: float) -> None:
        """
        Add a node to the back of the queue.
        
        Note: Priority is ignored for FIFO queue (all nodes have equal priority).
        
        Args:
            node: The node to insert
            priority: Ignored (FIFO doesn't use priorities)
        """
        if node.state not in self.state_set:
            self.queue.append(node)
            self.state_set.add(node.state)
    
    def pop(self) -> Node[StateType]:
        """
        Remove and return the node at the front of the queue.
        
        Returns:
            The oldest node in the queue
            
        Raises:
            IndexError: If the queue is empty
        """
        if not self.queue:
            raise IndexError("pop from empty FIFO queue")
        
        node = self.queue.popleft()
        self.state_set.discard(node.state)
        return node
    
    def is_empty(self) -> bool:
        """
        Check if the queue is empty.
        
        Returns:
            True if no nodes remain in the queue
        """
        return len(self.queue) == 0
    
    def __len__(self) -> int:
        """
        Return the number of nodes in the queue.
        
        Returns:
            Count of nodes currently in the queue
        """
        return len(self.queue)
    
    def __contains__(self, node: Node[StateType]) -> bool:
        """
        Check if a node's state is in the queue.
        
        Args:
            node: The node to check
            
        Returns:
            True if a node with this state exists in queue
        """
        return node.state in self.state_set

