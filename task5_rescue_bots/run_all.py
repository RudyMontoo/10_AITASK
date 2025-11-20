import os
os.environ['MPLBACKEND'] = 'Agg'

import random
from collections import deque

class MazeGrid:
    def __init__(self, size=14):
        self.size = size
        self.bots = {}
        self.walls = set()
        self.victims = set()
        self.rescued = {}
        
    def add_bot(self, bot_id, pos):
        self.bots[bot_id] = pos
    
    def add_walls(self, wall_list):
        self.walls = set(wall_list)
    
    def add_victims(self, victim_list):
        self.victims = set(victim_list)
    
    def move_bot(self, bot_id, pos):
        if self.is_valid(pos):
            self.bots[bot_id] = pos
            return True
        return False
    
    def is_valid(self, pos):
        x, y = pos
        return (0 <= x < self.size and 0 <= y < self.size and 
                pos not in self.walls)
    
    def rescue_victim(self, pos, bot_id):
        if pos in self.victims:
            self.victims.remove(pos)
            self.rescued[pos] = bot_id
            return True
        return False
    
    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            new_pos = (nx, ny)
            if self.is_valid(new_pos):
                neighbors.append(new_pos)
        return neighbors

class RescueBot:
    def __init__(self, bot_id, start_pos):
        self.id = bot_id
        self.pos = start_pos
        self.path = []
        self.rescued_victims = []
        self.assigned_zone = None
    
    def assign_zone(self, zone):
        self.assigned_zone = zone
    
    def move(self):
        if self.path:
            self.pos = self.path.pop(0)
        return self.pos

def bfs_to_victim(start, victims, maze, avoid=None):
    if avoid is None:
        avoid = set()
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        if current in victims:
            return path
        
        for next_pos in maze.get_neighbors(current):
            if next_pos not in visited and next_pos not in avoid:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    
    return []

def allocate_rescue_zones(maze_size, num_bots=2):
    zones = [set() for _ in range(num_bots)]
    mid = maze_size // 2
    
    for x in range(maze_size):
        for y in range(maze_size):
            if x < mid:
                zones[0].add((x, y))
            else:
                zones[1].add((x, y))
    
    return zones

def generate_maze_walls(size, density=0.2):
    walls = set()
    num_walls = int(size * size * density)
    
    while len(walls) < num_walls:
        x, y = random.randint(1, size-2), random.randint(1, size-2)
        if (x, y) not in [(0, 0), (size-1, size-1)]:
            walls.add((x, y))
    
    return walls

MAZE_SIZE = 14
NUM_VICTIMS = 10
WALL_DENSITY = 0.15

maze = MazeGrid(MAZE_SIZE)

walls = generate_maze_walls(MAZE_SIZE, WALL_DENSITY)
maze.add_walls(walls)

victims = set()
while len(victims) < NUM_VICTIMS:
    x, y = random.randint(1, MAZE_SIZE-2), random.randint(1, MAZE_SIZE-2)
    if ((x, y) not in walls and 
        (x, y) not in [(0, 0), (MAZE_SIZE-1, MAZE_SIZE-1)]):
        victims.add((x, y))

maze.add_victims(victims)

bot1 = RescueBot(1, (0, 0))
bot2 = RescueBot(2, (MAZE_SIZE-1, MAZE_SIZE-1))

maze.add_bot(1, bot1.pos)
maze.add_bot(2, bot2.pos)

bots = [bot1, bot2]

zones = allocate_rescue_zones(MAZE_SIZE, 2)
bot1.assign_zone(zones[0])
bot2.assign_zone(zones[1])

steps = 0
max_steps = 400

while steps < max_steps and len(maze.victims) > 0:
    for bot in bots:
        if not bot.path:
            zone_victims = maze.victims & bot.assigned_zone
            target_victims = zone_victims if zone_victims else maze.victims
            
            if target_victims:
                path = bfs_to_victim(bot.pos, target_victims, maze)
                if path:
                    bot.path = path[1:]
        
        new_pos = bot.move()
        maze.move_bot(bot.id, new_pos)
        
        if maze.rescue_victim(bot.pos, bot.id):
            bot.rescued_victims.append(bot.pos)
    
    steps += 1

total_rescued = len(maze.rescued)
print(f"Total Steps: {steps}")
print(f"Victims Rescued: {total_rescued}/{NUM_VICTIMS}")
print(f"Bot 1: {len(bot1.rescued_victims)} rescues")
print(f"Bot 2: {len(bot2.rescued_victims)} rescues")
