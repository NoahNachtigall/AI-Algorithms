# Maze Generator & Solver

## Overview
This program demonstrates two classic algorithms working together:
1. **Maze Generation**: Uses **Recursive Backtracking** to generate a random maze
2. **Maze Solving**: Uses **A* Pathfinding Algorithm** to find the shortest path through the maze

The entire process is animated so you can watch both algorithms work in real-time!

## How to Run

1. Make sure you have Python 3 and Pygame installed:
```bash
pip install pygame
```

2. Run the program:
```bash
python "maze gen.&solver.py"
```

3. A Pygame window will open displaying a grid.

## Controls

- **Press 'G'**: Generate a new maze using recursive backtracking algorithm
  - Watch as the algorithm carves out passages through the maze
  - Purple cells show the current cell being explored
  - All paths will be carved out, creating one solution path

- **Press 'S'**: Solve the generated maze using A* algorithm
  - Green cells show cells being explored (open set)
  - Red cells show cells that have been checked (closed set)
  - Yellow cells show the final shortest path from start to end

- **Press 'Q'**: Quit the program

## Algorithm Explanations

### Maze Generation - Recursive Backtracking
The Recursive Backtracking algorithm generates a "perfect maze" (one with exactly one solution path):

1. Start at a random cell and mark it as visited
2. While there are unvisited neighbors:
   - Pick a random unvisited neighbor
   - Remove the wall between the current cell and chosen neighbor
   - Recursively visit the chosen neighbor
3. When no unvisited neighbors remain, backtrack to previous cells
4. Repeat until all cells have been visited

**Result**: A maze with exactly one path from start to finish (no loops, no isolated areas)

### Maze Solving - A* Pathfinding Algorithm
A* is a best-first search algorithm that uses a heuristic to find the shortest path:

1. Start at the beginning cell
2. For each cell, calculate:
   - `g(n)`: Actual distance from start
   - `h(n)`: Manhattan distance to end (heuristic)
   - `f(n) = g(n) + h(n)`: Estimated total cost
3. Always explore the cell with lowest `f(n)` value
4. When the end cell is reached, reconstruct the path by backtracking through `came_from` dictionary
5. Mark the path cells in bright yellow

**Why A* is efficient**: The heuristic guides the search toward the goal, avoiding wasted exploration

## Visualization Guide

| Color | Meaning |
|-------|---------|
| White | Unvisited/empty cell |
| Orange | Starting point (top-left) |
| Purple | Ending point (bottom-right) |
| Purple (during generation) | Current cell being explored by backtracking |
| Green | Cell in open set (currently being considered) |
| Red | Cell in closed set (already explored) |
| Yellow | Part of the final solution path |
| Black Lines | Walls between cells |

## Configuration

You can customize the program by editing these variables at the top of the file:

```python
ROWS = 20           # Change maze size (20x20 grid, try 30-50 for complexity)
WIDTH = 600         # Window size in pixels (won't change maze size, just cell size)
delay = 5           # Animation speed in milliseconds (lower = faster, higher = slower)
```

## Interesting Facts

- **Heuristic**: A* uses Manhattan distance: `|x1 - x2| + |y1 - y2|`
- **Optimality**: A* guarantees finding the shortest path (if heuristic is admissible)
- **Perfect Maze**: Recursive backtracking creates mazes with exactly one solution
- **Time Complexity**: A* is O(b^d) where b is branching factor and d is depth
- **Real-world Uses**: GPS navigation, video game AI pathfinding, robot motion planning

## Tips for Best Experience

1. **Start with smaller mazes** (ROWS = 20) to see the algorithms clearly
2. **Increase delay** if animations are too fast: `delay = 20` or higher
3. **Decrease delay** if you're impatient: `delay = 1`
4. **Try ROWS = 50** for a challenging maze (may take longer to generate)
5. **Watch the A* algorithm** - it's fascinating how it explores!

## Further Learning

- **Maze Generation**: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker
- **A* Algorithm**: https://en.wikipedia.org/wiki/A*_search_algorithm
- **Heuristic Functions**: https://en.wikipedia.org/wiki/Admissible_heuristic

## File Structure

```
maze gen.&solver.py
├── Spot class          # Represents each cell in the maze
├── Maze generation functions
│   ├── make_grid()
│   ├── generate_maze()
│   └── get_neighbors()
├── Maze solving functions
│   ├── a_star()
│   ├── reconstruct_path()
│   └── h() (heuristic function)
└── main()              # Event loop and user interaction
```

## Performance Notes

- **Generation**: 20x20 maze ~1-2 seconds, 30x30 maze ~3-5 seconds
- **Solving**: Most mazes solve within 1-2 seconds (depends on path length)
- **Smooth Animation**: Set `delay` to 5-10ms for optimal viewing

## Troubleshooting

**Problem**: Maze doesn't show after pressing 'G'
- Solution: Press 'G' again, the window might need a refresh

**Problem**: Animation is too slow
- Solution: Decrease the `delay` variable at the top of the file

**Problem**: Animation is too fast to see
- Solution: Increase the `delay` variable

**Problem**: "pygame not found" error
- Solution: Install pygame: `pip install pygame`

Enjoy exploring these classic algorithms in action! 🎮
