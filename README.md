# Pathfinding Framework

A **modular, problem-agnostic** Python framework for search algorithms demonstrating advanced design patterns including **Dependency Injection** and **Inversion of Control (IoC)**.

## Project Goals

This framework separates the **search engine core** from **problem-specific logic**, enabling:

- **Reusability**: Write the search algorithm once, apply to any problem
- **Flexibility**: Mix and match problems, strategies, and heuristics
- **Extensibility**: Add new problems or algorithms without modifying core code
- **Testability**: Each component can be tested in isolation

## Architecture

The framework uses Dependency Injection to decouple components:

```
┌─────────────────────────────────────────────────────────┐
│                    SearchEngine                         │
│                  (Problem-Agnostic)                     │
└────────────┬────────────┬────────────┬──────────────────┘
             │            │            │
    ┌────────▼──────┐ ┌──▼──────────┐ ┌▼────────────────┐
    │   Problem     │ │  Frontier   │ │   Strategy      │
    │  (What to     │ │ (How to     │ │ (What order     │
    │   solve)      │ │  store)     │ │  to expand)     │
    └───────────────┘ └─────────────┘ └─────────────────┘
            │                               │
            │                      ┌────────▼────────┐
            │                      │   Heuristic     │
            │                      │  (Domain        │
            │                      │   knowledge)    │
            │                      └─────────────────┘
            │
    Implements AbstractProblem
      - initial_state()
      - is_goal(state)
      - get_successors(state)
```

### Directory Structure

```
path-finding-framework/
├── src/
│   ├── core/                      # Core search engine (problem-agnostic)
│   │   ├── types.py               # Abstract interfaces (contracts)
│   │   └── search_engine.py      # Main search loop
│   ├── strategies/                # Priority functions
│   │   ├── uninformed/            # Uninformed strategies (BFS, DFS, UCS)
│   │   └── informed/              # Informed strategies (A*, Greedy)
│   └── data_structures/           # Frontier implementations
│       ├── priority_queue.py      # Min-heap for best-first search
│       ├── fifo_queue.py          # Queue for BFS
│       └── lifo_stack.py          # Stack for DFS
├── examples/                      # Benchmark and demonstrations
│   └── framework_demo.ipynb       # Comprehensive demo notebook
├── pyproject.toml                 # Python package configuration
├── LICENSE                        # MIT License
└── README.md                      # This file
```

## Key Interfaces

### 1. `AbstractProblem[StateType]`
Defines the problem space:
- `initial_state() -> StateType`: Starting state
- `is_goal(state) -> bool`: Goal test
- `get_successors(state) -> List[Tuple[State, Action, Cost]]`: State expansion

### 2. `AbstractFrontier[StateType]`
Manages the open set:
- `push(node, priority)`: Add node with priority
- `pop() -> Node`: Remove highest-priority node
- `is_empty() -> bool`: Check if frontier is empty

### 3. `AbstractHeuristic[StateType]`
Provides domain knowledge for informed search:
- `h(state) -> float`: Estimate cost to goal
- `is_admissible() -> bool`: Never overestimates
- `is_consistent() -> bool`: Monotonic property

## Quick Start

### Installation

```bash
# Option 1: Install directly from git (recommended)
pip install git+https://github.com/andrea-difelice/pathfinding-framework.git

# Option 2: Install with benchmark dependencies
pip install "git+https://github.com/andrea-difelice/pathfinding-framework.git#egg=pathfinding-framework[benchmark]"

# Option 3: Clone and install locally
git clone https://github.com/andrea-difelice/pathfinding-framework.git
cd pathfinding-framework
pip install .

# Option 4: Install in development mode (for contributing)
pip install -e ".[dev]"
```

### Running the Benchmark

```bash
# Install with benchmark dependencies
pip install "git+https://github.com/andrea-difelice/pathfinding-framework.git#egg=pathfinding-framework[benchmark]"

# Or if cloned locally
pip install ".[benchmark]"

# Run the demo notebook
jupyter notebook examples/framework_demo.ipynb
```

The benchmark script demonstrates:
- **Problem Generation**: Creates a weighted graph with negative edges
- **Framework Implementation**: Defines problem-specific classes (GraphProblem, GraphNode, Heuristics)
- **Algorithm Comparison**: Runs UCS and A* from the framework
- **NetworkX Comparison**: Runs Bellman-Ford algorithm
- **Validation**: Verifies that results match between frameworks

### Benchmark Highlights

The script validates the framework by comparing it with NetworkX's Bellman-Ford algorithm on a graph with **positive edge weights**:

| Algorithm | Correctness | Performance |
|-----------|-------------|-------------|
| Framework UCS | ✓ Identical to NetworkX | Comparable |
| Framework A* (h=0) | ✓ Identical to NetworkX | Comparable |
| NetworkX Bellman-Ford | Reference | Baseline |

**Key Finding**: The framework produces **identical results** to NetworkX, validating its correctness while demonstrating superior architectural design through Dependency Injection.

## Usage Example

The best way to learn how to use the framework is to explore the **framework_demo.ipynb** notebook in the `examples/` directory. It provides a complete, working example.

### Quick Example: Custom Problem

```python
from dataclasses import dataclass
from typing import List, Tuple
from src.core import AbstractProblem, AbstractState, SearchEngine
from src.data_structures import PriorityQueueFrontier
from src.strategies import uniform_cost_priority

# 1. Define your state
@dataclass(frozen=True)
class MyState(AbstractState):
    value: int
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        return isinstance(other, MyState) and self.value == other.value
    
    def __repr__(self):
        return f"State({self.value})"

# 2. Implement AbstractProblem
class MyProblem(AbstractProblem[MyState]):
    def initial_state(self) -> MyState:
        return MyState(0)
    
    def is_goal(self, state: MyState) -> bool:
        return state.value == 10
    
    def get_successors(self, state: MyState) -> List[Tuple[MyState, str, float]]:
        return [
            (MyState(state.value + 1), "add_1", 1.0),
            (MyState(state.value + 2), "add_2", 2.0)
        ]

# 3. Create and run the search engine
engine = SearchEngine(
    problem=MyProblem(),
    frontier=PriorityQueueFrontier(),
    priority_fn=uniform_cost_priority,
    heuristic=None,
    graph_search=True
)

result = engine.search()

if result.success:
    print(f"✓ Found path: {' → '.join([str(s.value) for s in result.path])}")
    print(f"  Cost: {result.total_cost}")
```

**Output:**
```
✓ Found path: 0 → 2 → 4 → 6 → 8 → 10
  Cost: 10.0
```

## Supported Algorithms

### Uninformed Search (No Heuristic Required)
- **Breadth-First Search (BFS)**: Explores by depth level
- **Depth-First Search (DFS)**: Explores deepest paths first
- **Uniform Cost Search (UCS/Dijkstra)**: Expands by path cost g(n)

### Informed Search (Requires Heuristic)
- **A\* Search**: Optimal with admissible heuristic, f(n) = g(n) + h(n)
- **Greedy Best-First**: Fast but non-optimal, f(n) = h(n)

## Design Patterns

### 1. **Dependency Injection**
Components are passed to `SearchEngine` rather than hard-coded:
```python
SearchEngine(problem=..., frontier=..., priority_fn=..., heuristic=...)
```

### 2. **Strategy Pattern**
Priority functions encapsulate different search strategies:
- `uniform_cost_priority`: g(n)
- `astar_priority`: g(n) + h(n)
- `greedy_best_first_priority`: h(n)

### 3. **Template Method**
`SearchEngine.search()` defines the algorithm skeleton while delegating specifics to injected components.

### 4. **Null Object Pattern**
`NullHeuristic` provides h(n) = 0 for uninformed search, eliminating special cases.

## Extending the Framework

### Add a New Problem

1. Implement `AbstractProblem[YourStateType]`
2. Implement `AbstractState` for your state representation
3. Optionally create heuristics implementing `AbstractHeuristic[YourStateType]`

### Add a New Strategy

1. Create a new priority function in `src/strategies/`
2. Function signature: `(Node, Heuristic) -> float`
3. Import and use with any compatible frontier

### Add a New Frontier

1. Implement `AbstractFrontier[StateType]`
2. Choose appropriate data structure for your needs
3. Ensure O(1) membership testing for efficiency

## Contributing

This project is currently maintained by **[Andrea Di Felice/andrea-00]**.

We welcome contributions! If you would like to contribute, please follow these steps:
1.  **Fork** this repository.
2.  Create a new branch.
3.  Commit your changes.
4.  Open a **Pull Request** with a clear description of your changes.

For more details, please see our (future) `CONTRIBUTING.md` file.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for full details.

`Copyright (c) 2025 Andrea Di Felice <andrealav2901@gmail.com>`

