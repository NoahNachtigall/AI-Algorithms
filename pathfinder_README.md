# A* Pathfinding Algorithm

This Python script implements the A* pathfinding algorithm with a graphical interface using Pygame. It allows you to visualize the algorithm finding the shortest path between a start and end point on a grid, avoiding barriers.

## Features
- Interactive grid where you can set start, end, and barrier points
- Visual representation of the A* algorithm in action
- Color-coded states: open (green), closed (red), path (purple), etc.

## Requirements
- Python 3.x
- Pygame

## Installation
1. Install Pygame:
   ```
   pip install pygame
   ```

## Usage
Run the script:
```
python pathfinder.py
```
- Left-click to set barriers
- Right-click to set start (orange) or end (turquoise) points
- Press SPACE to start the algorithm
- Press C to clear the grid

## Algorithm Details
The A* algorithm uses a priority queue to explore nodes with the lowest f-score (g + h), where g is the cost from start, and h is the heuristic (Manhattan distance to end).