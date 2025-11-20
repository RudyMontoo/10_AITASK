import os
os.environ['MPLBACKEND'] = 'Agg'

import random
from collections import deque

class ExplorationGrid:
    def __init__(self, size=15):
        self.size = size
        self.agents = {}
        self.explored = set()
        self.obstacles = set()
    
    def add_agent(self, agent_id, pos):
        self.agents[agent_id] = pos
    
    def add_obstacles(self, obstacle_list):
        self.obstacles = set(obstacle_list)
    
    def move_agent(self, agent_id, pos):
        if self.is_valid(pos):
            self.agents[agent_id] = pos
            return True
        return False
    
    def is_valid(self, pos):
        x, y = pos
        return (0 <= x < self.size and 0 <= y < self.size and 
                pos not in self.obstacles)
    
    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            new_pos = (nx, ny)
            if self.is_valid(new_pos):
                neighbors.append(new_pos)
        return neighbors
    
    def mark_explored(self, pos):
        self.explored.add(pos)

class ExplorerAgent:
    def __init__(self, agent_id, start_pos):
        self.id = agent_id
        self.pos = start_pos
        self.path = []
        self.explored = set()
        self.assigned_region = None
    
    def assign_region(self, region):
        self.assigned_region = region
    
    def move(self):
        if self.path:
            self.pos = self.path.pop(0)
        return self.pos
    
    def explore(self):
        self.explored.add(self.pos)


def bfs_nearest_unexplored(start, unexplored, grid, avoid=None):
    if avoid is None:
        avoid = set()
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        if current in unexplored and current != start:
            return path
        
        for next_pos in grid.get_neighbors(current):
            if next_pos not in visited and next_pos not in avoid:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    
    return []

def partition_grid(grid_size, num_agents=2):
    regions = [set() for _ in range(num_agents)]
    mid = grid_size // 2
    
    for x in range(grid_size):
        for y in range(grid_size):
            if x < mid:
                regions[0].add((x, y))
            else:
                regions[1].add((x, y))
    
    return regions

GRID_SIZE = 15
NUM_OBSTACLES = 20

grid = ExplorationGrid(GRID_SIZE)

obstacles = set()
while len(obstacles) < NUM_OBSTACLES:
    x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    if (x, y) not in [(0, 0), (GRID_SIZE-1, GRID_SIZE-1)]:
        obstacles.add((x, y))

grid.add_obstacles(obstacles)

agent1 = ExplorerAgent(1, (0, 0))
agent2 = ExplorerAgent(2, (GRID_SIZE-1, GRID_SIZE-1))

grid.add_agent(1, agent1.pos)
grid.add_agent(2, agent2.pos)

agents = [agent1, agent2]

regions = partition_grid(GRID_SIZE, 2)

regions[0] -= obstacles
regions[1] -= obstacles

agent1.assign_region(regions[0])
agent2.assign_region(regions[1])

agent1.explore()
agent2.explore()
grid.mark_explored(agent1.pos)
grid.mark_explored(agent2.pos)

steps = 0
max_steps = 500

total_explorable = GRID_SIZE * GRID_SIZE - len(obstacles)

while steps < max_steps:
    for agent in agents:
        if not agent.path:
            unexplored = agent.assigned_region - grid.explored
            if unexplored:
                path = bfs_nearest_unexplored(agent.pos, unexplored, grid, {agent2.pos if agent.id == 1 else agent1.pos})
                if path:
                    agent.path = path[1:]
        
        new_pos = agent.move()
        grid.move_agent(agent.id, new_pos)
        
        agent.explore()
        grid.mark_explored(agent.pos)
    
    steps += 1
    
    if len(grid.explored) >= total_explorable:
        break

explored_pct = (len(grid.explored) / total_explorable) * 100

print(f"Total Steps: {steps}")
print(f"Cells Explored: {len(grid.explored)}/{total_explorable}")
print(f"Agent 1: {len(agent1.explored)} cells")
print(f"Agent 2: {len(agent2.explored)} cells")
print(f"Coverage: {explored_pct:.1f}%")
