import os
os.environ['MPLBACKEND'] = 'Agg'

class PaintingGrid:
    def __init__(self, size=12):
        self.size = size
        self.agents = {}
        self.painted = {}
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
    
    def paint_cell(self, pos, agent_id):
        if pos not in self.painted:
            self.painted[pos] = agent_id
            return True
        return False
    
    def is_painted(self, pos):
        return pos in self.painted
    
    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            new_pos = (nx, ny)
            if self.is_valid(new_pos):
                neighbors.append(new_pos)
        return neighbors

class PaintingRobot:
    def __init__(self, agent_id, start_pos):
        self.id = agent_id
        self.pos = start_pos
        self.painted_cells = set()
        self.assigned_region = None
    
    def assign_region(self, region):
        self.assigned_region = region

def allocate_regions(grid_size, num_robots=4):
    regions = [set() for _ in range(num_robots)]
    mid_x = grid_size // 2
    mid_y = grid_size // 2
    
    for x in range(grid_size):
        for y in range(grid_size):
            if x < mid_x and y < mid_y:
                regions[0].add((x, y))
            elif x >= mid_x and y < mid_y:
                regions[1].add((x, y))
            elif x < mid_x and y >= mid_y:
                regions[2].add((x, y))
            else:
                regions[3].add((x, y))
    
    return regions

GRID_SIZE = 16

grid = PaintingGrid(GRID_SIZE)

obstacles = []
mid = GRID_SIZE // 2
for i in range(4, 12):
    if i != mid:
        obstacles.append((mid - 1, i))
        obstacles.append((mid, i))

grid.add_obstacles(obstacles)

regions = allocate_regions(GRID_SIZE, 4)

for region in regions:
    region -= grid.obstacles

robot1 = PaintingRobot(1, (0, 0))
robot2 = PaintingRobot(2, (GRID_SIZE - 1, 0))
robot3 = PaintingRobot(3, (0, GRID_SIZE - 1))
robot4 = PaintingRobot(4, (GRID_SIZE - 1, GRID_SIZE - 1))

robot1.assign_region(regions[0])
robot2.assign_region(regions[1])
robot3.assign_region(regions[2])
robot4.assign_region(regions[3])

grid.add_agent(1, robot1.pos)
grid.add_agent(2, robot2.pos)
grid.add_agent(3, robot3.pos)
grid.add_agent(4, robot4.pos)

robots = [robot1, robot2, robot3, robot4]

total_cells = GRID_SIZE * GRID_SIZE

steps = 0
max_steps = 300

stacks = [[robot.pos] for robot in robots]

while steps < max_steps:
    all_done = True
    
    for idx, robot in enumerate(robots):
        unpainted_in_region = robot.assigned_region - robot.painted_cells
        
        if unpainted_in_region:
            all_done = False
            
            if stacks[idx]:
                current = stacks[idx][-1]
                
                if current in robot.assigned_region and not grid.is_painted(current):
                    grid.paint_cell(current, robot.id)
                    robot.painted_cells.add(current)
                    grid.move_agent(robot.id, current)
                
                found_neighbor = False
                for neighbor in grid.get_neighbors(current):
                    if neighbor in robot.assigned_region and not grid.is_painted(neighbor):
                        stacks[idx].append(neighbor)
                        found_neighbor = True
                        break
                
                if not found_neighbor:
                    stacks[idx].pop()
                    if stacks[idx]:
                        grid.move_agent(robot.id, stacks[idx][-1])
    
    steps += 1
    
    if all_done or len(grid.painted) >= total_cells:
        break

painted_count = len(grid.painted)
paintable_cells = total_cells - len(grid.obstacles)
coverage = (painted_count / paintable_cells) * 100

print(f"Total Steps: {steps}")
print(f"Total Cells: {total_cells}")
print(f"Obstacles: {len(grid.obstacles)}")
print(f"Paintable Cells: {paintable_cells}")
print(f"Robot 1: {len(robot1.painted_cells)} cells")
print(f"Robot 2: {len(robot2.painted_cells)} cells")
print(f"Robot 3: {len(robot3.painted_cells)} cells")
print(f"Robot 4: {len(robot4.painted_cells)} cells")
print(f"Coverage: {coverage:.1f}%")
