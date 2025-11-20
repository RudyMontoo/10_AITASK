import os
os.environ['MPLBACKEND'] = 'Agg'

import random
import heapq

class DeliveryGrid:
    def __init__(self, size=14):
        self.size = size
        self.drones = {}
        self.packages = {}
        self.delivered = {}
        
    def add_drone(self, drone_id, pos):
        self.drones[drone_id] = pos
    
    def add_package(self, pkg_id, pickup, delivery):
        self.packages[pkg_id] = (pickup, delivery)
    
    def move_drone(self, drone_id, pos):
        if self.is_valid(pos):
            self.drones[drone_id] = pos
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

class DeliveryDrone:
    def __init__(self, drone_id, start_pos):
        self.id = drone_id
        self.pos = start_pos
        self.path = []
        self.current_package = None
        self.has_package = False
        self.delivered_packages = []
        
    def move(self):
        if self.path:
            self.pos = self.path.pop(0)
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

def greedy_assign_packages(drones, packages, grid):
    assignments = {drone.id: [] for drone in drones}
    available = list(packages.keys())
    
    while available:
        for drone in drones:
            if not available:
                break
            
            nearest_pkg = min(available, 
                            key=lambda p: abs(packages[p][0][0] - drone.pos[0]) + 
                                        abs(packages[p][0][1] - drone.pos[1]))
            
            assignments[drone.id].append(nearest_pkg)
            available.remove(nearest_pkg)
    
    return assignments

GRID_SIZE = 14
NUM_PACKAGES = 8

grid = DeliveryGrid(GRID_SIZE)

packages = {}
for i in range(1, NUM_PACKAGES + 1):
    pickup = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    delivery = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    while delivery == pickup:
        delivery = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    packages[i] = (pickup, delivery)
    grid.add_package(i, pickup, delivery)

drone1 = DeliveryDrone(1, (0, 0))
drone2 = DeliveryDrone(2, (GRID_SIZE-1, GRID_SIZE-1))

grid.add_drone(1, drone1.pos)
grid.add_drone(2, drone2.pos)

drones = [drone1, drone2]

assignments = greedy_assign_packages(drones, packages, grid)

steps = 0
max_steps = 500

while steps < max_steps and len(grid.delivered) < NUM_PACKAGES:
    for drone in drones:
        if not drone.path and assignments[drone.id]:
            pkg_id = assignments[drone.id][0]
            
            if pkg_id in grid.packages:
                pickup, delivery = grid.packages[pkg_id]
                
                if not drone.has_package:
                    path = astar(drone.pos, pickup, grid)
                    if path:
                        drone.path = path[1:]
                        drone.current_package = pkg_id
                else:
                    path = astar(drone.pos, delivery, grid)
                    if path:
                        drone.path = path[1:]
        
        new_pos = drone.move()
        grid.move_drone(drone.id, new_pos)
        
        if drone.current_package and not drone.has_package:
            pkg_id = drone.current_package
            if pkg_id in grid.packages:
                pickup, delivery = grid.packages[pkg_id]
                if drone.pos == pickup:
                    drone.has_package = True
        
        if drone.has_package and drone.current_package:
            pkg_id = drone.current_package
            if pkg_id in grid.packages:
                pickup, delivery = grid.packages[pkg_id]
                if drone.pos == delivery:
                    grid.delivered[pkg_id] = drone.id
                    drone.delivered_packages.append(pkg_id)
                    drone.has_package = False
                    drone.current_package = None
                    assignments[drone.id].pop(0)
                    del grid.packages[pkg_id]
    
    steps += 1

total_delivered = len(grid.delivered)
print(f"Total Steps: {steps}")
print(f"Packages Delivered: {total_delivered}/{NUM_PACKAGES}")
print(f"Drone 1: {len(drone1.delivered_packages)} packages")
print(f"Drone 2: {len(drone2.delivered_packages)} packages")
