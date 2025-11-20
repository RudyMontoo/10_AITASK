"""
Map Exploration Partners - Simple Implementation
Two agents explore unknown regions cooperatively
"""
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ============= ENVIRONMENT =============
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

# ============= AGENT =============
class ExplorerAgent:
    def __init__(self, agent_id, start_pos):
        self.id = agent_id
        self.pos = start_pos
        self.path = []
        self.explored = set()
        self.assigned_region = None
    
    def assign_region(self, region):
        """Assign a region (set of cells) to explore"""
        self.assigned_region = region
    
    def move(self):
        if self.path:
            self.pos = self.path.pop(0)
        return self.pos
    
    def explore(self):
        """Mark current position as explored"""
        self.explored.add(self.pos)

# ============= PATHFINDING (BFS for exploration) =============
def bfs_nearest_unexplored(start, unexplored, grid, avoid=None):
    """Find path to nearest unexplored cell"""
    if avoid is None:
        avoid = set()
    
    from collections import deque
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        # Found unexplored cell
        if current in unexplored and current != start:
            return path
        
        for next_pos in grid.get_neighbors(current):
            if next_pos not in visited and next_pos not in avoid:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    
    return []

# ============= REGION PARTITIONING =============
def partition_grid(grid_size, num_agents=2):
    """Divide grid into regions for each agent"""
    regions = [set() for _ in range(num_agents)]
    
    # Simple vertical split for 2 agents
    mid = grid_size // 2
    
    for x in range(grid_size):
        for y in range(grid_size):
            if x < mid:
                regions[0].add((x, y))
            else:
                regions[1].add((x, y))
    
    return regions

# ============= VISUALIZATION =============
def visualize_exploration(grid, agents, step, total_cells):
    plt.clf()
    
    # Create heatmap data
    heatmap = np.zeros((grid.size, grid.size))
    
    # Mark explored cells
    for x, y in grid.explored:
        heatmap[y, x] = 1
    
    # Mark obstacles
    for x, y in grid.obstacles:
        heatmap[y, x] = -1
    
    # Display heatmap
    plt.imshow(heatmap, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, alpha=0.7)
    
    # Grid lines
    for i in range(grid.size + 1):
        plt.axvline(i - 0.5, color='gray', linewidth=0.5)
        plt.axhline(i - 0.5, color='gray', linewidth=0.5)
    
    # Draw agents
    colors = ['blue', 'red', 'green', 'orange']
    for idx, (agent_id, pos) in enumerate(grid.agents.items()):
        x, y = pos
        circle = patches.Circle((x, y), 0.3, color=colors[idx], alpha=0.9, zorder=10)
        plt.gca().add_patch(circle)
        plt.text(x, y, str(agent_id), ha='center', va='center', 
                color='white', fontweight='bold', zorder=11)
    
    explored_pct = (len(grid.explored) / total_cells) * 100
    plt.title(f'Step {step} | Explored: {len(grid.explored)}/{total_cells} ({explored_pct:.1f}%)')
    plt.xlim(-0.5, grid.size - 0.5)
    plt.ylim(-0.5, grid.size - 0.5)
    plt.gca().set_aspect('equal')
    
    plt.pause(0.05)

def create_heatmap(grid, agent1, agent2):
    """Create final exploration heatmap"""
    plt.figure(figsize=(12, 5))
    
    # Subplot 1: Agent 1 exploration
    plt.subplot(1, 3, 1)
    heatmap1 = np.zeros((grid.size, grid.size))
    for x, y in agent1.explored:
        heatmap1[y, x] = 1
    plt.imshow(heatmap1, cmap='Blues', origin='lower')
    plt.title(f'Agent 1: {len(agent1.explored)} cells')
    plt.colorbar()
    
    # Subplot 2: Agent 2 exploration
    plt.subplot(1, 3, 2)
    heatmap2 = np.zeros((grid.size, grid.size))
    for x, y in agent2.explored:
        heatmap2[y, x] = 1
    plt.imshow(heatmap2, cmap='Reds', origin='lower')
    plt.title(f'Agent 2: {len(agent2.explored)} cells')
    plt.colorbar()
    
    # Subplot 3: Combined exploration
    plt.subplot(1, 3, 3)
    heatmap_combined = np.zeros((grid.size, grid.size))
    for x, y in grid.explored:
        heatmap_combined[y, x] = 1
    for x, y in grid.obstacles:
        heatmap_combined[y, x] = -1
    plt.imshow(heatmap_combined, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1)
    plt.title(f'Combined: {len(grid.explored)} cells')
    plt.colorbar()
    
    plt.tight_layout()
    plt.show()

# ============= MAIN SIMULATION =============
def run_exploration():
    print("Starting Map Exploration Simulation...")
    print("=" * 50)
    
    # Setup
    GRID_SIZE = 15
    NUM_OBSTACLES = 20
    
    grid = ExplorationGrid(GRID_SIZE)
    
    # Create random obstacles
    obstacles = set()
    while len(obstacles) < NUM_OBSTACLES:
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if (x, y) not in [(0, 0), (GRID_SIZE-1, GRID_SIZE-1)]:
            obstacles.add((x, y))
    
    grid.add_obstacles(obstacles)
    
    # Initialize agents
    agent1 = ExplorerAgent(1, (0, 0))
    agent2 = ExplorerAgent(2, (GRID_SIZE-1, GRID_SIZE-1))
    
    grid.add_agent(1, agent1.pos)
    grid.add_agent(2, agent2.pos)
    
    # Partition grid
    regions = partition_grid(GRID_SIZE, 2)
    
    # Remove obstacles from regions
    regions[0] -= obstacles
    regions[1] -= obstacles
    
    agent1.assign_region(regions[0])
    agent2.assign_region(regions[1])
    
    print(f"Agent 1 region: {len(regions[0])} cells")
    print(f"Agent 2 region: {len(regions[1])} cells")
    print(f"Obstacles: {len(obstacles)}")
    
    # Mark starting positions as explored
    agent1.explore()
    agent2.explore()
    grid.mark_explored(agent1.pos)
    grid.mark_explored(agent2.pos)
    
    # Simulation
    plt.figure(figsize=(10, 10))
    steps = 0
    max_steps = 500
    
    total_explorable = GRID_SIZE * GRID_SIZE - len(obstacles)
    
    while steps < max_steps:
        print(f"\n--- Step {steps} ---")
        
        # Agent 1 planning
        if not agent1.path:
            unexplored = agent1.assigned_region - grid.explored
            if unexplored:
                path = bfs_nearest_unexplored(agent1.pos, unexplored, grid, {agent2.pos})
                if path:
                    agent1.path = path[1:]
        
        # Agent 2 planning
        if not agent2.path:
            unexplored = agent2.assigned_region - grid.explored
            if unexplored:
                path = bfs_nearest_unexplored(agent2.pos, unexplored, grid, {agent1.pos})
                if path:
                    agent2.path = path[1:]
        
        # Move agents
        new_pos1 = agent1.move()
        new_pos2 = agent2.move()
        
        grid.move_agent(1, new_pos1)
        grid.move_agent(2, new_pos2)
        
        print(f"Agent 1: Moved to {new_pos1}")
        print(f"Agent 2: Moved to {new_pos2}")
        
        # Explore
        agent1.explore()
        agent2.explore()
        grid.mark_explored(agent1.pos)
        grid.mark_explored(agent2.pos)
        
        if agent1.pos not in agent1.explored or agent2.pos not in agent2.explored:
            if agent1.pos not in agent1.explored:
                print(f"Agent 1: Explored new cell at {agent1.pos}")
            if agent2.pos not in agent2.explored:
                print(f"Agent 2: Explored new cell at {agent2.pos}")
        
        # Visualize every 10 steps
        if steps % 10 == 0:
            visualize_exploration(grid, [agent1, agent2], steps, total_explorable)
        
        steps += 1
        
        # Check if fully explored
        if len(grid.explored) >= total_explorable:
            break
    
    # Final results
    explored_pct = (len(grid.explored) / total_explorable) * 100
    efficiency = (total_explorable / steps) * 100 if steps > 0 else 0
    
    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"  Total Steps: {steps}")
    print(f"  Cells Explored: {len(grid.explored)}/{total_explorable}")
    print(f"  Agent 1: {len(agent1.explored)} cells")
    print(f"  Agent 2: {len(agent2.explored)} cells")
    print(f"  Coverage: {explored_pct:.1f}%")
    print(f"  Efficiency: {efficiency:.2f} cells/step")
    print(f"{'='*50}")
    
    # Show final heatmap
    visualize_exploration(grid, [agent1, agent2], steps, total_explorable)
    plt.pause(1)
    create_heatmap(grid, agent1, agent2)

if __name__ == "__main__":
    run_exploration()
