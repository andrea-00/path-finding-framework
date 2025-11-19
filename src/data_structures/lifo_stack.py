"""
LIFO Stack implementation for Depth-First Search.

Used by: DFS (uninformed search)
"""

from typing import List, Set
from src.core.types import AbstractFrontier, Node, StateType


class LIFOStackFrontier(AbstractFrontier[StateType]):
    """
    Last-In-First-Out stack for Depth-First Search.
    
    Maintains nodes in reverse order of insertion, expanding the most
    recently discovered nodes first (deepest-first exploration).
    
    Attributes:
        stack: List used as a stack for O(1) push/pop at end
        state_set: Set of states for O(1) membership testing
    """
    
    def __init__(self):
        """Initialize an empty LIFO stack."""
        self.stack: List[Node[StateType]] = []
        self.state_set: Set[StateType] = set()
    
    def push(self, node: Node[StateType], priority: float) -> None:
        """
        Push a node onto the top of the stack.
        
        Note: Priority is ignored for LIFO stack (all nodes have equal priority).
        
        Args:
            node: The node to insert
            priority: Ignored (LIFO doesn't use priorities)
        """
        if node.state not in self.state_set:
            self.stack.append(node)
            self.state_set.add(node.state)
    
    def pop(self) -> Node[StateType]:
        """
        Remove and return the node at the top of the stack.
        
        Returns:
            The most recently added node
            
        Raises:
            IndexError: If the stack is empty
        """
        if not self.stack:
            raise IndexError("pop from empty LIFO stack")
        
        node = self.stack.pop()
        self.state_set.discard(node.state)
        return node
    
    def is_empty(self) -> bool:
        """
        Check if the stack is empty.
        
        Returns:
            True if no nodes remain in the stack
        """
        return len(self.stack) == 0
    
    def __len__(self) -> int:
        """
        Return the number of nodes in the stack.
        
        Returns:
            Count of nodes currently in the stack
        """
        return len(self.stack)
    
    def __contains__(self, node: Node[StateType]) -> bool:
        """
        Check if a node's state is in the stack.
        
        Args:
            node: The node to check
            
        Returns:
            True if a node with this state exists in stack
        """
        return node.state in self.state_set

