#PLEASE READ THE "readme.txt" FILE IN THIS FOLDER or on my Github: Noah Nachtigall FOR INSTRUCTIONS ON HOW TO RUN THIS CODE AND WHAT IT DOES

# Maze Generator and Solver using Pygame
# Generates maze with animated recursive backtracking
# Solves with animated A* algorithm
#I know that this code is a bit long, but I wanted to include both the maze generation and solving in one file for simplicity. The code is well-commented to help YOU understand each part. 
#You can adjust the ROWS variable to create larger or smaller mazes, and the delay variable to speed up or slow down the animation.
#You can probably see a lot of helper functions in this code that are similar to the ones in my pathfinder code - that's because the A* implementation is very similar, I just had to add the maze generation part on top of it.

#I would recommend reading the Wikipedia page on the Recursive Backtracking algorithm for maze generation to understand how it works: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker
#And watch some tutorials for Maze generation & Solving. It's really interesting how "Intelligent" the algorithms can look when visualized, even though they're just following simple rules.

#Press 'G' to generate maze, 'S' to solve



import pygame
import random
from queue import PriorityQueue

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Window setup
WIDTH = 1000     #Window size (won't affect maze size, just cell size)                                                  
ROWS = 5       #Number of rows/columns in the maze (maze will be ROWS x ROWS)
delay = 1000      #Delay in milliseconds for animation speed
GAP = WIDTH // ROWS
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Maze Generator & Solver")


#each Cell in the Maze is represented by a Spot object, which has properties for its position, color, neighbors, walls, and visited status. 
#The Spot class also has methods for drawing itself, updating its neighbors based on the walls, and changing its color to indicate different states (start, end, barrier, path, open, closed).
class Spot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * GAP
        self.y = row * GAP
        self.color = WHITE
        self.neighbors = []
        self.walls = [True, True, True, True]  # top, right, bottom, left
        self.visited = False

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = PURPLE

    def make_barrier(self):
        self.color = BLACK

    def make_path(self):
        self.color = BLUE

    def make_open(self):
        self.color = GREEN

    def make_closed(self):
        self.color = RED

    def make_current(self):
        self.color = PURPLE

    def draw(self, win):
        for i, wall in enumerate(self.walls):
            if wall:
                if i == 0:  # top
                    pygame.draw.line(win, BLACK, (self.x, self.y), (self.x + GAP, self.y), 4)
                elif i == 1:  # right
                    pygame.draw.line(win, BLACK, (self.x + GAP, self.y), (self.x + GAP, self.y + GAP), 4)
                elif i == 2:  # bottom
                    pygame.draw.line(win, BLACK, (self.x, self.y + GAP), (self.x + GAP, self.y + GAP), 4)
                elif i == 3:  # left
                    pygame.draw.line(win, BLACK, (self.x, self.y), (self.x, self.y + GAP), 4)

        pygame.draw.rect(win, self.color, (self.x + 3, self.y + 3, GAP - 6, GAP - 6))

    def update_neighbors(self, grid):
        self.neighbors = []
        if not self.walls[0] and self.row > 0:  # top
            self.neighbors.append(grid[self.row - 1][self.col])
        if not self.walls[1] and self.col < ROWS - 1:  # right
            self.neighbors.append(grid[self.row][self.col + 1])
        if not self.walls[2] and self.row < ROWS - 1:  # bottom
            self.neighbors.append(grid[self.row + 1][self.col])
        if not self.walls[3] and self.col > 0:  # left
            self.neighbors.append(grid[self.row][self.col - 1])

def make_grid():
    grid = []
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            spot = Spot(i, j)
            grid[i].append(spot)
    return grid

def draw(win, grid):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    pygame.display.update()

def get_neighbors(grid, spot):
    neighbors = []
    row, col = spot.row, spot.col
    if row > 0:
        neighbors.append(grid[row - 1][col])
    if row < ROWS - 1:
        neighbors.append(grid[row + 1][col])
    if col > 0:
        neighbors.append(grid[row][col - 1])
    if col < ROWS - 1:
        neighbors.append(grid[row][col + 1])
    return neighbors

def remove_walls(current, next):
    dx = current.col - next.col
    dy = current.row - next.row
    if dx == 1:  # next is left
        current.walls[3] = False
        next.walls[1] = False
    elif dx == -1:  # next is right
        current.walls[1] = False
        next.walls[3] = False
    elif dy == 1:  # next is above
        current.walls[0] = False
        next.walls[2] = False
    elif dy == -1:  # next is below
        current.walls[2] = False
        next.walls[0] = False


# Recursive Backtracking Maze Generation
def generate_maze(grid, draw, start):
    stack = []
    current = start
    current.visited = True
    stack.append(current)

    while stack:
        current = stack[-1]
        current.make_current()
        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        pygame.time.delay(delay)  # Animation delay

        #This is where the animation happens - we mark the current cell, draw, and then delay before moving on to the next step
        neighbors = [n for n in get_neighbors(grid, current) if not n.visited]      #Get unvisited neighbors
        if neighbors:
            next = random.choice(neighbors)
            next.visited = True
            remove_walls(current, next)
            stack.append(next)
        else:
            current.reset()
            stack.pop()

    # Reset colors after generation
    for row in grid:
        for spot in row:
            spot.reset()

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


#if the Maze is solved successfully, we reconstruct the path from the end to the start using the came_from dictionary, marking the path cells in bright yellow and adding a delay for animation.
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = came_from[current]
        current.make_path()
        draw()
        pygame.time.delay(delay * 3)  # Slower animation for path visibility

def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        pygame.time.delay(delay)

        if current != start:
            current.make_closed()

    return False

def main(win):
    grid = make_grid()
    start = grid[0][0]
    end = grid[ROWS - 1][ROWS - 1]
    maze_generated = False

    run = True
    while run:
        draw(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    # Reset grid
                    for row in grid:
                        for spot in row:
                            spot.reset()
                            spot.visited = False
                            spot.walls = [True, True, True, True]
                    generate_maze(grid, lambda: draw(win, grid), start)
                    start.make_start()
                    end.make_end()
                    maze_generated = True

                elif event.key == pygame.K_s and maze_generated:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    a_star(lambda: draw(win, grid), grid, start, end)


    pygame.quit()

if __name__ == "__main__":
    main(WIN)

#01001110 01101111 01100001 01101000 00100000 01001110 01100001 01100011 01101000 01110100 01101001 01100111 01100001 01101100 01101100 00100000 01111000 01000100