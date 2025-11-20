"""
Resource Collection Team - Simple Implementation
Two collector agents gather resources cooperatively using shared task queue
"""
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import heapq

# ============= ENVIRONMENT =============
class ResourceGrid:
    def __init__(self, size=12):
        self.size = size
        self.agents = {}
        self.resources = set()  # Shared task queue
        self.collected = {}  # Track who collected what
        
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
        """Collect resource at position"""
        if pos in self.resources:
            self.resources.remove(pos)
            if agent_id not in self.collected:
                self.collected[agent_id] = []
            self.collected[agent_id].append(pos)
            return True
        return False

# ============= AGENT =============
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
        """Distributed decision: select nearest resource"""
        if not available_resources:
            return None
        
        # Find nearest resource using Manhattan distance
        nearest = min(available_resources, 
                     key=lambda r: abs(r[0] - self.pos[0]) + abs(r[1] - self.pos[1]))
        return nearest

# ============= PATHFINDING (A*) =============
def astar(start, goal, grid, avoid=None):
    """A* pathfinding to resource"""
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

# ============= VISUALIZATION =============
def visualize_collection(grid, agents, step, total_resources, collection_history):
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
    
    # Draw collected resources (green circles)
    for agent_id, resources in grid.collected.items():
        for x, y in resources:
            circle = patches.Circle((x + 0.5, y + 0.5), 0.2, 
                                   facecolor='lightgreen', edgecolor='green', 
                                   linewidth=2, alpha=0.5)
            ax1.add_patch(circle)
    
    # Draw available resources (yellow stars)
    for x, y in grid.resources:
        star = patches.RegularPolygon((x + 0.5, y + 0.5), 5, radius=0.3,
                                     facecolor='yellow', edgecolor='orange',
                                     linewidth=2, alpha=0.9)
        ax1.add_patch(star)
    
    # Draw agents
    colors = ['blue', 'red']
    for idx, agent in enumerate(agents):
        x, y = agent.pos
        circle = patches.Circle((x + 0.5, y + 0.5), 0.35, 
                               color=colors[idx], alpha=0.9, zorder=10)
        ax1.add_patch(circle)
        ax1.text(x + 0.5, y + 0.5, str(agent.id), ha='center', va='center', 
                color='white', fontweight='bold', zorder=11)
        
        # Draw path to target
        if agent.target and agent.target in grid.resources:
            tx, ty = agent.target
            ax1.plot([x + 0.5, tx + 0.5], [y + 0.5, ty + 0.5], 
                    color=colors[idx], linestyle='--', alpha=0.3, linewidth=2)
    
    collected = sum(len(r) for r in grid.collected.values())
    ax1.set_title(f'Step {step} | Collected: {collected}/{total_resources}')
    
    # Collection statistics bar chart
    ax2 = plt.subplot(1, 2, 2)
    
    agent_ids = [agent.id for agent in agents]
    collections = [len(grid.collected.get(agent.id, [])) for agent in agents]
    colors_bar = ['blue', 'red']
    
    bars = ax2.bar(agent_ids, collections, color=colors_bar, alpha=0.7, edgecolor='black', linewidth=2)
    
    # Add value labels on bars
    for bar, count in zip(bars, collections):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}', ha='center', va='bottom', fontweight='bold')
    
    ax2.set_xlabel('Agent ID', fontsize=12)
    ax2.set_ylabel('Resources Collected', fontsize=12)
    ax2.set_title('Collection Performance', fontsize=14)
    ax2.set_ylim(0, total_resources + 2)
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_xticks(agent_ids)
    
    plt.tight_layout()
    plt.pause(0.05)

# ============= MAIN SIMULATION =============
def run_collection():
    print("Starting Resource Collection Simulation...")
    print("=" * 50)
    
    # Setup
    GRID_SIZE = 12
    NUM_RESOURCES = 15
    
    grid = ResourceGrid(GRID_SIZE)
    
    # Create random resources
    resources = set()
    while len(resources) < NUM_RESOURCES:
        x, y = random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)
        if (x, y) not in [(0, 0), (GRID_SIZE-1, GRID_SIZE-1)]:
            resources.add((x, y))
    
    grid.add_resources(resources)
    
    # Initialize agents
    agent1 = CollectorAgent(1, (0, 0))
    agent2 = CollectorAgent(2, (GRID_SIZE-1, GRID_SIZE-1))
    
    grid.add_agent(1, agent1.pos)
    grid.add_agent(2, agent2.pos)
    
    agents = [agent1, agent2]
    
    print(f"Total resources: {NUM_RESOURCES}")
    print(f"Agent 1 starting at: {agent1.pos}")
    print(f"Agent 2 starting at: {agent2.pos}")
    
    # Collection history for visualization
    collection_history = []
    
    # Simulation
    plt.figure(figsize=(12, 6))
    steps = 0
    max_steps = 300
    
    while steps < max_steps and len(grid.resources) > 0:
        print(f"\n--- Step {steps} ---")
        
        # Agent 1 decision logic
        if not agent1.path or agent1.target not in grid.resources:
            agent1.target = agent1.select_next_resource(grid.resources)
            if agent1.target:
                path = astar(agent1.pos, agent1.target, grid, {agent2.pos})
                if path:
                    agent1.path = path[1:]
        
        # Agent 2 decision logic
        if not agent2.path or agent2.target not in grid.resources:
            agent2.target = agent2.select_next_resource(grid.resources)
            if agent2.target:
                path = astar(agent2.pos, agent2.target, grid, {agent1.pos})
                if path:
                    agent2.path = path[1:]
        
        # Move agents
        new_pos1 = agent1.move()
        new_pos2 = agent2.move()
        
        grid.move_agent(1, new_pos1)
        grid.move_agent(2, new_pos2)
        
        print(f"Agent 1: Moved to {new_pos1}")
        print(f"Agent 2: Moved to {new_pos2}")
        
        # Collect resources
        if grid.collect_resource(agent1.pos, 1):
            agent1.collected.append(agent1.pos)
            print(f"Agent 1: ✓ COLLECTED resource at {agent1.pos}")
        
        if grid.collect_resource(agent2.pos, 2):
            agent2.collected.append(agent2.pos)
            print(f"Agent 2: ✓ COLLECTED resource at {agent2.pos}")
        
        # Track history
        collection_history.append({
            'step': steps,
            'agent1': len(agent1.collected),
            'agent2': len(agent2.collected)
        })
        
        # Visualize
        if steps % 5 == 0:
            visualize_collection(grid, agents, steps, NUM_RESOURCES, collection_history)
        
        steps += 1
    
    # Final results
    total_collected = len(agent1.collected) + len(agent2.collected)
    efficiency = (total_collected / steps) * 100 if steps > 0 else 0
    balance1 = (len(agent1.collected) / total_collected * 100) if total_collected > 0 else 0
    balance2 = (len(agent2.collected) / total_collected * 100) if total_collected > 0 else 0
    
    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"  Total Time: {steps} steps")
    print(f"  Total Resources: {NUM_RESOURCES}")
    print(f"  Agent 1: {len(agent1.collected)} resources")
    print(f"  Agent 2: {len(agent2.collected)} resources")
    print(f"  Efficiency: {efficiency:.2f} resources/100 steps")
    print(f"  Balance: {balance1:.1f}% / {balance2:.1f}%")
    print(f"{'='*50}")
    
    # Final visualization
    visualize_collection(grid, agents, steps, NUM_RESOURCES, collection_history)
    plt.show()

if __name__ == "__main__":
    run_collection()
