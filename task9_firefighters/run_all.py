import os
os.environ['MPLBACKEND'] = 'Agg'

import random
from collections import deque

class FireGrid:
    def __init__(self, size=12):
        self.size = size
        self.agents = {}
        self.fires = set()
        self.extinguished = set()
        self.fire_intensity = {}
        self.spread_prob = 0.3
        
    def add_agent(self, agent_id, pos):
        self.agents[agent_id] = pos
    
    def add_fire(self, pos):
        self.fires.add(pos)
        self.fire_intensity[pos] = 1
    
    def move_agent(self, agent_id, pos):
        if self.is_valid(pos):
            self.agents[agent_id] = pos
            return True
        return False
    
    def is_valid(self, pos):
        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size
    
    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            new_pos = (nx, ny)
            if self.is_valid(new_pos):
                neighbors.append(new_pos)
        return neighbors
    
    def extinguish_fire(self, pos):
        if pos in self.fires:
            self.fires.remove(pos)
            self.extinguished.add(pos)
            if pos in self.fire_intensity:
                del self.fire_intensity[pos]
            return True
        return False
    
    def spread_fires(self):
        new_fires = []
        
        for fire_pos in list(self.fires):
            self.fire_intensity[fire_pos] = self.fire_intensity.get(fire_pos, 1) + 1
            
            for neighbor in self.get_neighbors(fire_pos):
                if (neighbor not in self.fires and 
                    neighbor not in self.extinguished and
                    random.random() < self.spread_prob):
                    new_fires.append(neighbor)
        
        for pos in new_fires:
            self.add_fire(pos)
        
        return len(new_fires)

class FirefighterAgent:
    def __init__(self, agent_id, start_pos):
        self.id = agent_id
        self.pos = start_pos
        self.path = []
        self.extinguished = set()
        self.assigned_zone = None
    
    def assign_zone(self, zone):
        self.assigned_zone = zone
    
    def move(self):
        if self.path:
            self.pos = self.path.pop(0)
        return self.pos

def bfs_to_fire(start, fires, grid, avoid=None):
    if avoid is None:
        avoid = set()
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        if current in fires:
            return path
        
        for next_pos in grid.get_neighbors(current):
            if next_pos not in visited and next_pos not in avoid:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    
    return []

def allocate_zones(grid_size, num_agents=2):
    zones = [set() for _ in range(num_agents)]
    mid = grid_size // 2
    
    for x in range(grid_size):
        for y in range(grid_size):
            if x < mid:
                zones[0].add((x, y))
            else:
                zones[1].add((x, y))
    
    return zones

GRID_SIZE = 12
NUM_INITIAL_FIRES = 8
FIRE_SPREAD_INTERVAL = 5

grid = FireGrid(GRID_SIZE)

initial_fires = set()
while len(initial_fires) < NUM_INITIAL_FIRES:
    x, y = random.randint(2, GRID_SIZE-3), random.randint(2, GRID_SIZE-3)
    if (x, y) not in [(0, 0), (GRID_SIZE-1, GRID_SIZE-1)]:
        initial_fires.add((x, y))

for fire_pos in initial_fires:
    grid.add_fire(fire_pos)

agent1 = FirefighterAgent(1, (0, 0))
agent2 = FirefighterAgent(2, (GRID_SIZE-1, GRID_SIZE-1))

grid.add_agent(1, agent1.pos)
grid.add_agent(2, agent2.pos)

agents = [agent1, agent2]

zones = allocate_zones(GRID_SIZE, 2)
agent1.assign_zone(zones[0])
agent2.assign_zone(zones[1])

steps = 0
max_steps = 300
total_fires_created = len(initial_fires)

while steps < max_steps and len(grid.fires) > 0:
    if steps % FIRE_SPREAD_INTERVAL == 0 and steps > 0:
        new_fires = grid.spread_fires()
        if new_fires > 0:
            total_fires_created += new_fires
    
    for agent in agents:
        if not agent.path:
            zone_fires = grid.fires & agent.assigned_zone
            target_fires = zone_fires if zone_fires else grid.fires
            
            if target_fires:
                path = bfs_to_fire(agent.pos, target_fires, grid)
                if path:
                    agent.path = path[1:]
        
        new_pos = agent.move()
        grid.move_agent(agent.id, new_pos)
        
        if grid.extinguish_fire(agent.pos):
            agent.extinguished.add(agent.pos)
    
    steps += 1

total_extinguished = len(grid.extinguished)
success = len(grid.fires) == 0

print(f"Total Steps: {steps}")
print(f"Total Fires: {total_fires_created}")
print(f"Extinguished: {total_extinguished}")
print(f"Still Burning: {len(grid.fires)}")
print(f"Agent 1: {len(agent1.extinguished)} fires")
print(f"Agent 2: {len(agent2.extinguished)} fires")
print(f"Status: {'SUCCESS' if success else 'PARTIAL'}")
