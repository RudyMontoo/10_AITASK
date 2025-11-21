"""
Cleaning Crew Coordination - Simple Implementation
Two bots clean a grid cooperatively
"""
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import deque

# ============= ENVIRONMENT =============
class Grid:
    def __init__(self, size=10):
        self.size = size
        self.agents = {}
    
    def add_agent(self, agent_id, pos):
        self.agents[agent_id] = pos
    
    def move_agent(self, agent_id, pos):
        if 0 <= pos[0] < self.size and 0 <= pos[1] < self.size:
            self.agents[agent_id] = pos
            return True
        return False
    
    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                neighbors.append((nx, ny))
        return neighbors

# ============= AGENT =============
class CleaningBot:
    def __init__(self, bot_id, start_pos):
        self.id = bot_id
        self.pos = start_pos
        self.path = []
        self.cleaned = set()
        self.tasks = []
    
    def assign_tasks(self, cells):
        self.tasks = list(cells)
    
    def move(self):
        if self.path:
            self.pos = self.path.pop(0)
        return self.pos
    
    def clean(self):
        self.cleaned.add(self.pos)

# ============= PATHFINDING (A*) =============
def astar(start, goal, grid, avoid=None):
    if avoid is None:
        avoid = set()
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    frontier = [(0, start)]
    came_from = {start: None}
    cost = {start: 0}
    
    while frontier:
        frontier.sort()
        _, current = frontier.pop(0)
        
        if current == goal:
            break
        
        for next_pos in grid.get_neighbors(current):
            if next_pos in avoid:
                continue
            
            new_cost = cost[current] + 1
            if next_pos not in cost or new_cost < cost[next_pos]:
                cost[next_pos] = new_cost
                priority = new_cost + heuristic(next_pos, goal)
                frontier.append((priority, next_pos))
                came_from[next_pos] = current
    
    # Reconstruct path
    if goal not in came_from:
        return []
    
    path = []
    current = goal
    while current:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# ============= TASK ALLOCATION =============
def divide_tasks(dirty_cells, pos1, pos2):
    """Divide tasks based on proximity"""
    tasks1, tasks2 = [], []
    
    for cell in dirty_cells:
        dist1 = abs(cell[0] - pos1[0]) + abs(cell[1] - pos1[1])
        dist2 = abs(cell[0] - pos2[0]) + abs(cell[1] - pos2[1])
        
        if dist1 <= dist2:
            tasks1.append(cell)
        else:
            tasks2.append(cell)
    
    return tasks1, tasks2

# ============= VISUALIZATION =============
def visualize(grid, dirty, cleaned, step, total):
    plt.clf()
    plt.xlim(0, grid.size)
    plt.ylim(0, grid.size)
    plt.gca().set_aspect('equal')
    plt.title(f'Step {step} | Cleaned: {len(cleaned)}/{total}')
    
    # Grid lines
    for i in range(grid.size + 1):
        plt.axvline(i, color='gray', linewidth=0.5)
        plt.axhline(i, color='gray', linewidth=0.5)
    
    # Dirty cells (brown)
    for x, y in dirty:
        rect = patches.Rectangle((x, y), 1, 1, facecolor='brown', alpha=0.5)
        plt.gca().add_patch(rect)
    
    # Cleaned cells (green)
    for x, y in cleaned:
        rect = patches.Rectangle((x, y), 1, 1, facecolor='lightgreen', alpha=0.5)
        plt.gca().add_patch(rect)
    
    # Agents
    colors = ['blue', 'red']
    for idx, (agent_id, pos) in enumerate(grid.agents.items()):
        x, y = pos
        circle = patches.Circle((x + 0.5, y + 0.5), 0.3, color=colors[idx], alpha=0.8)
        plt.gca().add_patch(circle)
        plt.text(x + 0.5, y + 0.5, str(agent_id), ha='center', va='center', 
                color='white', fontweight='bold')
    
    plt.pause(0.05)

# ============= MAIN SIMULATION =============
def run_simulation():
    print("Starting Cleaning Crew Simulation...")
    print("=" * 50)
    
    # Setup
    GRID_SIZE = 10
    NUM_DIRTY = 20
    
    grid = Grid(GRID_SIZE)
    
    # Create dirty cells
    dirty_cells = set()
    while len(dirty_cells) < NUM_DIRTY:
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        dirty_cells.add((x, y))
    
    # Initialize bots
    bot1 = CleaningBot(1, (0, 0))
    bot2 = CleaningBot(2, (GRID_SIZE-1, GRID_SIZE-1))
    
    grid.add_agent(1, bot1.pos)
    grid.add_agent(2, bot2.pos)
    
    # Divide tasks
    tasks1, tasks2 = divide_tasks(dirty_cells, bot1.pos, bot2.pos)
    bot1.assign_tasks(tasks1)
    bot2.assign_tasks(tasks2)
    
    print(f"Bot 1: {len(tasks1)} tasks | Bot 2: {len(tasks2)} tasks")
    
    # Simulation
    plt.figure(figsize=(8, 8))
    steps = 0
    max_steps = 300
    
    while steps < max_steps:
        # Plan paths if needed
        if not bot1.path and bot1.tasks:
            remaining = [c for c in bot1.tasks if c not in bot1.cleaned]
            if remaining:
                target = min(remaining, key=lambda c: abs(c[0]-bot1.pos[0]) + abs(c[1]-bot1.pos[1]))
                path = astar(bot1.pos, target, grid, {bot2.pos})
                if path:
                    bot1.path = path[1:]
        
        if not bot2.path and bot2.tasks:
            remaining = [c for c in bot2.tasks if c not in bot2.cleaned]
            if remaining:
                target = min(remaining, key=lambda c: abs(c[0]-bot2.pos[0]) + abs(c[1]-bot2.pos[1]))
                path = astar(bot2.pos, target, grid, {bot1.pos})
                if path:
                    bot2.path = path[1:]
        
        # Move bots
        new_pos1 = bot1.move()
        new_pos2 = bot2.move()
        
        if steps % 5 == 0:
            print(f"Bot 1: Moved to {new_pos1}")
            print(f"Bot 2: Moved to {new_pos2}")
        
        grid.move_agent(1, new_pos1)
        grid.move_agent(2, new_pos2)
        
        # Clean
        if bot1.pos in dirty_cells:
            bot1.clean()
            if steps % 5 == 0:
                print(f"Bot 1: Cleaned cell at {bot1.pos}")
        if bot2.pos in dirty_cells:
            bot2.clean()
            if steps % 5 == 0:
                print(f"Bot 2: Cleaned cell at {bot2.pos}")
        
        # Print grid every 5 steps
        if steps % 5 == 0:
            cleaned = bot1.cleaned | bot2.cleaned
            remaining_dirty = dirty_cells - cleaned
            print("\nCurrent Grid:")
            for y in range(grid.size-1, -1, -1):
                row = ""
                for x in range(grid.size):
                    pos = (x, y)
                    if pos == bot1.pos and pos == bot2.pos:
                        row += "X "
                    elif pos == bot1.pos:
                        row += "1 "
                    elif pos == bot2.pos:
                        row += "2 "
                    elif pos in cleaned:
                        row += "C "
                    elif pos in remaining_dirty:
                        row += "D "
                    else:
                        row += "· "
                print(row)
            print(f"Cleaned: {len(cleaned)}/{len(dirty_cells)}")
            print()
        
        # Visualize
        cleaned = bot1.cleaned | bot2.cleaned
        remaining_dirty = dirty_cells - cleaned
        
        if steps % 5 == 0:  # Update every 5 steps for speed
            visualize(grid, remaining_dirty, cleaned, steps, len(dirty_cells))
        
        steps += 1
        
        # Check if done
        if not remaining_dirty:
            break
    
    # Final results
    total_cleaned = len(bot1.cleaned | bot2.cleaned)
    efficiency = (total_cleaned / len(dirty_cells)) * 100
    
    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"  Total Steps: {steps}")
    print(f"  Cells Cleaned: {total_cleaned}/{len(dirty_cells)}")
    print(f"  Bot 1: {len(bot1.cleaned)} cells")
    print(f"  Bot 2: {len(bot2.cleaned)} cells")
    print(f"  Efficiency: {efficiency:.1f}%")
    print(f"{'='*50}")
    
    visualize(grid, set(), bot1.cleaned | bot2.cleaned, steps, len(dirty_cells))
    plt.show()

if __name__ == "__main__":
    run_simulation()
