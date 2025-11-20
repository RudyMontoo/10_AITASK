"""
Cooperative Firefighters - Simple Implementation
Two firefighter agents extinguish fires cooperatively with fire spread simulation
"""
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from collections import deque

# ============= ENVIRONMENT =============
class FireGrid:
    def __init__(self, size=12):
        self.size = size
        self.agents = {}
        self.fires = set()
        self.extinguished = set()
        self.fire_intensity = {}  # Track fire age/intensity
        self.spread_prob = 0.3  # Probability of fire spreading
        
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
        """Extinguish fire at position"""
        if pos in self.fires:
            self.fires.remove(pos)
            self.extinguished.add(pos)
            if pos in self.fire_intensity:
                del self.fire_intensity[pos]
            return True
        return False
    
    def spread_fires(self):
        """Simulate fire spreading to adjacent cells"""
        new_fires = []
        
        for fire_pos in list(self.fires):
            # Increase fire intensity
            self.fire_intensity[fire_pos] = self.fire_intensity.get(fire_pos, 1) + 1
            
            # Try to spread to neighbors
            for neighbor in self.get_neighbors(fire_pos):
                if (neighbor not in self.fires and 
                    neighbor not in self.extinguished and
                    random.random() < self.spread_prob):
                    new_fires.append(neighbor)
        
        # Add new fires
        for pos in new_fires:
            self.add_fire(pos)
        
        return len(new_fires)

# ============= AGENT =============
class FirefighterAgent:
    def __init__(self, agent_id, start_pos):
        self.id = agent_id
        self.pos = start_pos
        self.path = []
        self.extinguished = set()
        self.assigned_zone = None
    
    def assign_zone(self, zone):
        """Assign a zone (set of cells) to patrol"""
        self.assigned_zone = zone
    
    def move(self):
        if self.path:
            self.pos = self.path.pop(0)
        return self.pos

# ============= PATHFINDING (BFS) =============
def bfs_to_fire(start, fires, grid, avoid=None):
    """Find shortest path to nearest fire"""
    if avoid is None:
        avoid = set()
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        # Found a fire
        if current in fires:
            return path
        
        for next_pos in grid.get_neighbors(current):
            if next_pos not in visited and next_pos not in avoid:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    
    return []

# ============= ZONE ALLOCATION =============
def allocate_zones(grid_size, num_agents=2):
    """Divide grid into zones for each agent"""
    zones = [set() for _ in range(num_agents)]
    
    # Vertical split for 2 agents
    mid = grid_size // 2
    
    for x in range(grid_size):
        for y in range(grid_size):
            if x < mid:
                zones[0].add((x, y))
            else:
                zones[1].add((x, y))
    
    return zones

# ============= VISUALIZATION =============
def visualize_firefighting(grid, agents, step, initial_fires, stats):
    plt.clf()
    fig = plt.gcf()
    fig.set_size_inches(12, 6)
    
    # Main grid visualization
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_xlim(0, grid.size)
    ax1.set_ylim(0, grid.size)
    ax1.set_aspect('equal')
    
    # Grid lines
    for i in range(grid.size + 1):
        ax1.axvline(i, color='gray', linewidth=0.5)
        ax1.axhline(i, color='gray', linewidth=0.5)
    
    # Draw extinguished fires (gray)
    for x, y in grid.extinguished:
        rect = patches.Rectangle((x, y), 1, 1, facecolor='gray', alpha=0.3)
        ax1.add_patch(rect)
    
    # Draw active fires (red/orange based on intensity)
    for x, y in grid.fires:
        intensity = grid.fire_intensity.get((x, y), 1)
        alpha = min(0.5 + intensity * 0.1, 1.0)
        color = 'red' if intensity > 2 else 'orange'
        rect = patches.Rectangle((x, y), 1, 1, facecolor=color, alpha=alpha)
        ax1.add_patch(rect)
        ax1.text(x + 0.5, y + 0.5, str(intensity), ha='center', va='center', 
                color='white', fontsize=8, fontweight='bold')
    
    # Draw agents
    colors = ['blue', 'cyan']
    for idx, (agent_id, pos) in enumerate(grid.agents.items()):
        x, y = pos
        circle = patches.Circle((x + 0.5, y + 0.5), 0.35, 
                               color=colors[idx], alpha=0.9, zorder=10)
        ax1.add_patch(circle)
        ax1.text(x + 0.5, y + 0.5, str(agent_id), ha='center', va='center', 
                color='white', fontweight='bold', zorder=11)
    
    active_fires = len(grid.fires)
    extinguished_fires = len(grid.extinguished)
    ax1.set_title(f'Step {step} | Active: {active_fires} | Extinguished: {extinguished_fires}/{initial_fires}')
    
    # Statistics graph
    ax2 = plt.subplot(1, 2, 2)
    steps = list(range(len(stats['active_fires'])))
    ax2.plot(steps, stats['active_fires'], 'r-', label='Active Fires', linewidth=2)
    ax2.plot(steps, stats['extinguished'], 'g-', label='Extinguished', linewidth=2)
    ax2.fill_between(steps, stats['active_fires'], alpha=0.3, color='red')
    ax2.fill_between(steps, stats['extinguished'], alpha=0.3, color='green')
    ax2.set_xlabel('Time Steps')
    ax2.set_ylabel('Number of Fires')
    ax2.set_title('Fire Extinguishing Progress')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.pause(0.05)

# ============= MAIN SIMULATION =============
def run_firefighting():
    print("Starting Cooperative Firefighters Simulation...")
    print("=" * 50)
    
    # Setup
    GRID_SIZE = 12
    NUM_INITIAL_FIRES = 8
    FIRE_SPREAD_INTERVAL = 5  # Fires spread every N steps
    
    grid = FireGrid(GRID_SIZE)
    
    # Create initial fires
    initial_fires = set()
    while len(initial_fires) < NUM_INITIAL_FIRES:
        x, y = random.randint(2, GRID_SIZE-3), random.randint(2, GRID_SIZE-3)
        if (x, y) not in [(0, 0), (GRID_SIZE-1, GRID_SIZE-1)]:
            initial_fires.add((x, y))
    
    for fire_pos in initial_fires:
        grid.add_fire(fire_pos)
    
    # Initialize agents
    agent1 = FirefighterAgent(1, (0, 0))
    agent2 = FirefighterAgent(2, (GRID_SIZE-1, GRID_SIZE-1))
    
    grid.add_agent(1, agent1.pos)
    grid.add_agent(2, agent2.pos)
    
    # Allocate zones
    zones = allocate_zones(GRID_SIZE, 2)
    agent1.assign_zone(zones[0])
    agent2.assign_zone(zones[1])
    
    print(f"Initial fires: {len(initial_fires)}")
    print(f"Agent 1 zone: {len(zones[0])} cells")
    print(f"Agent 2 zone: {len(zones[1])} cells")
    
    # Statistics tracking
    stats = {
        'active_fires': [],
        'extinguished': [],
        'new_fires': []
    }
    
    # Simulation
    plt.figure(figsize=(12, 6))
    steps = 0
    max_steps = 300
    total_fires_created = len(initial_fires)
    
    while steps < max_steps and len(grid.fires) > 0:
        print(f"\n--- Step {steps} ---")
        
        # Fire spreading
        if steps % FIRE_SPREAD_INTERVAL == 0 and steps > 0:
            new_fires = grid.spread_fires()
            if new_fires > 0:
                total_fires_created += new_fires
                print(f"Step {steps}: {new_fires} new fires spread!")
        
        # Agent 1 planning - prioritize fires in own zone, then any fire
        if not agent1.path:
            zone_fires = grid.fires & agent1.assigned_zone
            target_fires = zone_fires if zone_fires else grid.fires
            
            if target_fires:
                path = bfs_to_fire(agent1.pos, target_fires, grid, {agent2.pos})
                if path:
                    agent1.path = path[1:]
        
        # Agent 2 planning
        if not agent2.path:
            zone_fires = grid.fires & agent2.assigned_zone
            target_fires = zone_fires if zone_fires else grid.fires
            
            if target_fires:
                path = bfs_to_fire(agent2.pos, target_fires, grid, {agent1.pos})
                if path:
                    agent2.path = path[1:]
        
        # Move agents
        new_pos1 = agent1.move()
        new_pos2 = agent2.move()
        
        grid.move_agent(1, new_pos1)
        grid.move_agent(2, new_pos2)
        
        print(f"Agent 1: Moved to {new_pos1}")
        print(f"Agent 2: Moved to {new_pos2}")
        
        # Extinguish fires
        if grid.extinguish_fire(agent1.pos):
            agent1.extinguished.add(agent1.pos)
            print(f"Agent 1: ✓ EXTINGUISHED fire at {agent1.pos}")
        
        if grid.extinguish_fire(agent2.pos):
            agent2.extinguished.add(agent2.pos)
            print(f"Agent 2: ✓ EXTINGUISHED fire at {agent2.pos}")
        
        # Track statistics
        stats['active_fires'].append(len(grid.fires))
        stats['extinguished'].append(len(grid.extinguished))
        
        # Visualize
        if steps % 3 == 0:
            visualize_firefighting(grid, [agent1, agent2], steps, 
                                  total_fires_created, stats)
        
        steps += 1
    
    # Final results
    success = len(grid.fires) == 0
    extinguish_rate = (len(grid.extinguished) / total_fires_created) * 100
    
    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"  Total Time: {steps} steps")
    print(f"  Total Fires: {total_fires_created}")
    print(f"  Extinguished: {len(grid.extinguished)}")
    print(f"  Still Burning: {len(grid.fires)}")
    print(f"  Agent 1: {len(agent1.extinguished)} fires")
    print(f"  Agent 2: {len(agent2.extinguished)} fires")
    print(f"  Success Rate: {extinguish_rate:.1f}%")
    print(f"  Status: {'SUCCESS' if success else 'PARTIAL'}")
    print(f"{'='*50}")
    
    # Final visualization
    visualize_firefighting(grid, [agent1, agent2], steps, 
                          total_fires_created, stats)
    plt.show()

if __name__ == "__main__":
    run_firefighting()
