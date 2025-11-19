"""
Data structures module for frontier implementations.
"""

from .priority_queue import PriorityQueueFrontier
from .fifo_queue import FIFOQueueFrontier
from .lifo_stack import LIFOStackFrontier

__all__ = [
    'PriorityQueueFrontier',
    'FIFOQueueFrontier',
    'LIFOStackFrontier'
]

