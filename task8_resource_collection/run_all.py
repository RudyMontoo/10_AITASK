import os
os.environ['MPLBACKEND'] = 'Agg'

import random
import heapq

class ResourceGrid:
    def __init__(self, size=12):
        self.size = size
        self.agents = {}
        self.resources = set()
        self.collected = {}
        
    def add_agent(self, agent_id, pos):
        self.agents[agent_id] = pos
    
    def add_resources(self, resource_list):
        self.resources = set(resource_list)
    
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
    
    def collect_resource(self, pos, agent_id):
        if pos in self.resources:
            self.resources.remove(pos)
            if agent_id not in self.collected:
                self.collected[agent_id] = []
            self.collected[agent_id].append(pos)
            return True
        return False

class CollectorAgent:
    def __init__(self, agent_id, start_pos):
        self.id = agent_id
        self.pos = start_pos
        self.path = []
        self.collected = []
        self.target = None
    
    def move(self):
        if self.path:
            self.pos = self.path.pop(0)
        return self.pos
    
    def select_next_resource(self, available_resources):
        if not available_resources:
            return None
        
        nearest = min(available_resources, 
                     key=lambda r: abs(r[0] - self.pos[0]) + abs(r[1] - self.pos[1]))
        return nearest

def astar(start, goal, grid, avoid=None):
    if avoid is None:
        avoid = set()
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    frontier = [(0, start)]
    came_from = {start: None}
    cost = {start: 0}
    
    while frontier:
        _, current = heapq.heappop(frontier)
        
        if current == goal:
            break
        
        for next_pos in grid.get_neighbors(current):
            if next_pos in avoid:
                continue
            
            new_cost = cost[current] + 1
            if next_pos not in cost or new_cost < cost[next_pos]:
                cost[next_pos] = new_cost
                priority = new_cost + heuristic(next_pos, goal)
                heapq.heappush(frontier, (priority, next_pos))
                came_from[next_pos] = current
    
    if goal not in came_from:
        return []
    
    path = []
    current = goal
    while current:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

GRID_SIZE = 12
NUM_RESOURCES = 15

grid = ResourceGrid(GRID_SIZE)

resources = set()
while len(resources) < NUM_RESOURCES:
    x, y = random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)
    if (x, y) not in [(0, 0), (GRID_SIZE-1, GRID_SIZE-1)]:
        resources.add((x, y))

grid.add_resources(resources)

agent1 = CollectorAgent(1, (0, 0))
agent2 = CollectorAgent(2, (GRID_SIZE-1, GRID_SIZE-1))
agent3 = CollectorAgent(3, (0, GRID_SIZE-1))
agent4 = CollectorAgent(4, (GRID_SIZE-1, 0))

grid.add_agent(1, agent1.pos)
grid.add_agent(2, agent2.pos)
grid.add_agent(3, agent3.pos)
grid.add_agent(4, agent4.pos)

agents = [agent1, agent2, agent3, agent4]

steps = 0
max_steps = 300

while steps < max_steps and len(grid.resources) > 0:
    for agent in agents:
        if not agent.path or agent.target not in grid.resources:
            agent.target = agent.select_next_resource(grid.resources)
            if agent.target:
                other_positions = {a.pos for a in agents if a.id != agent.id}
                path = astar(agent.pos, agent.target, grid, other_positions)
                if path:
                    agent.path = path[1:]
        
        new_pos = agent.move()
        grid.move_agent(agent.id, new_pos)
        
        if grid.collect_resource(agent.pos, agent.id):
            agent.collected.append(agent.pos)
    
    steps += 1

total_collected = sum(len(c) for c in grid.collected.values())
print(f"Total Steps: {steps}")
print(f"Resources Collected: {total_collected}/{NUM_RESOURCES}")
print(f"Agent 1: {len(agent1.collected)} resources")
print(f"Agent 2: {len(agent2.collected)} resources")
print(f"Agent 3: {len(agent3.collected)} resources")
print(f"Agent 4: {len(agent4.collected)} resources")
