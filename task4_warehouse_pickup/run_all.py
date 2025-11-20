import os
os.environ['MPLBACKEND'] = 'Agg'

import random
import heapq

class WarehouseGrid:
    def __init__(self, size=12):
        self.size = size
        self.agents = {}
        self.items = {}
        self.dropoff_zones = []
        self.completed = {}
        
    def add_agent(self, agent_id, pos):
        self.agents[agent_id] = pos
    
    def add_item(self, item_id, pickup_pos):
        self.items[item_id] = pickup_pos
    
    def add_dropoff_zone(self, pos):
        self.dropoff_zones.append(pos)
    
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

class WarehouseAgent:
    def __init__(self, agent_id, start_pos):
        self.id = agent_id
        self.pos = start_pos
        self.path = []
        self.carrying_item = None
        self.completed_items = []
        self.total_distance = 0
        
    def move(self):
        if self.path:
            self.pos = self.path.pop(0)
            self.total_distance += 1
        return self.pos

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

def assign_nearest_item(agent, available_items, warehouse):
    if not available_items:
        return None
    
    nearest = min(available_items,
                 key=lambda item_id: abs(warehouse.items[item_id][0] - agent.pos[0]) + 
                                   abs(warehouse.items[item_id][1] - agent.pos[1]))
    return nearest

WAREHOUSE_SIZE = 12
NUM_ITEMS = 10

warehouse = WarehouseGrid(WAREHOUSE_SIZE)

dropoff_zones = [(0, 0), (WAREHOUSE_SIZE-1, WAREHOUSE_SIZE-1)]
for zone in dropoff_zones:
    warehouse.add_dropoff_zone(zone)

items = {}
for i in range(1, NUM_ITEMS + 1):
    x, y = random.randint(2, WAREHOUSE_SIZE-3), random.randint(2, WAREHOUSE_SIZE-3)
    while (x, y) in dropoff_zones:
        x, y = random.randint(2, WAREHOUSE_SIZE-3), random.randint(2, WAREHOUSE_SIZE-3)
    items[i] = (x, y)
    warehouse.add_item(i, (x, y))

agent1 = WarehouseAgent(1, dropoff_zones[0])
agent2 = WarehouseAgent(2, dropoff_zones[1])

warehouse.add_agent(1, agent1.pos)
warehouse.add_agent(2, agent2.pos)

agents = [agent1, agent2]

steps = 0
max_steps = 400

while steps < max_steps and len(warehouse.completed) < NUM_ITEMS:
    for agent in agents:
        if not agent.carrying_item and not agent.path:
            available = [item_id for item_id in warehouse.items.keys()
                       if item_id not in warehouse.completed.keys()]
            
            for other_agent in agents:
                if (other_agent.id != agent.id and 
                    other_agent.carrying_item in available):
                    available.remove(other_agent.carrying_item)
            
            if available:
                nearest_item = assign_nearest_item(agent, available, warehouse)
                if nearest_item:
                    pickup_pos = warehouse.items[nearest_item]
                    path = astar(agent.pos, pickup_pos, warehouse)
                    if path:
                        agent.path = path[1:]
                        agent.carrying_item = nearest_item
        
        elif agent.carrying_item and not agent.path:
            nearest_dropoff = min(warehouse.dropoff_zones,
                                key=lambda d: abs(d[0]-agent.pos[0]) + abs(d[1]-agent.pos[1]))
            path = astar(agent.pos, nearest_dropoff, warehouse)
            if path:
                agent.path = path[1:]
        
        new_pos = agent.move()
        warehouse.move_agent(agent.id, new_pos)
        
        if agent.carrying_item and agent.pos in warehouse.dropoff_zones:
            if agent.carrying_item in warehouse.items:
                warehouse.completed[agent.carrying_item] = agent.id
                agent.completed_items.append(agent.carrying_item)
                del warehouse.items[agent.carrying_item]
                agent.carrying_item = None
    
    steps += 1

print(f"Total Steps: {steps}")
