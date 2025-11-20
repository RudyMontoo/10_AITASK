import os
os.environ['MPLBACKEND'] = 'Agg'

class PaintingGrid:
    def __init__(self, size=12):
        self.size = size
        self.agents = {}
        self.painted = {}
        
    def add_agent(self, agent_id, pos):
        self.agents[agent_id] = pos
    
    def move_agent(self, agent_id, pos):
        if self.is_valid(pos):
            self.agents[agent_id] = pos
            return True
        return False
    
    def is_valid(self, pos):
        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size
    
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

def allocate_regions(grid_size, num_robots=2):
    regions = [set() for _ in range(num_robots)]
    mid = grid_size // 2
    
    for x in range(grid_size):
        for y in range(grid_size):
            if x < mid:
                regions[0].add((x, y))
            else:
                regions[1].add((x, y))
    
    return regions

GRID_SIZE = 12

grid = PaintingGrid(GRID_SIZE)

regions = allocate_regions(GRID_SIZE, 2)

robot1 = PaintingRobot(1, (0, 0))
robot2 = PaintingRobot(2, (GRID_SIZE // 2, 0))

robot1.assign_region(regions[0])
robot2.assign_region(regions[1])

grid.add_agent(1, robot1.pos)
grid.add_agent(2, robot2.pos)

robots = [robot1, robot2]

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
coverage = (painted_count / total_cells) * 100

print(f"Total Steps: {steps}")
print(f"Total Cells: {total_cells}")
print(f"Robot 1: {len(robot1.painted_cells)} cells")
print(f"Robot 2: {len(robot2.painted_cells)} cells")
print(f"Coverage: {coverage:.1f}%")
