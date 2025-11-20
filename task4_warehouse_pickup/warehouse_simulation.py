"""
Warehouse Pickup Team - Simple Implementation
Two agents pick and drop items cooperatively using proximity-based assignment
"""
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import heapq

# ============= ENVIRONMENT =============
class WarehouseGrid:
    def __init__(self, size=12):
        self.size = size
        self.agents = {}
        self.items = {}  # item_id -> pickup_location
        self.dropoff_zones = []
        self.completed = {}  # item_id -> agent_id
        
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

# ============= AGENT =============
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

# ============= A* PATHFINDING =============
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

# ============= PROXIMITY-BASED ASSIGNMENT =============
def assign_nearest_item(agent, available_items, warehouse):
    """Assign nearest available item to agent"""
    if not available_items:
        return None
    
    nearest = min(available_items,
                 key=lambda item_id: abs(warehouse.items[item_id][0] - agent.pos[0]) + 
                                   abs(warehouse.items[item_id][1] - agent.pos[1]))
    return nearest

# ============= VISUALIZATION =============
def visualize_warehouse(warehouse, agents, step, total_items):
    plt.clf()
    fig = plt.gcf()
    fig.set_size_inches(12, 6)
    
    # Main warehouse view
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_xlim(0, warehouse.size)
    ax1.set_ylim(0, warehouse.size)
    ax1.set_aspect('equal')
    
    # Grid lines
    for i in range(warehouse.size + 1):
        ax1.axvline(i, color='gray', linewidth=0.5)
        ax1.axhline(i, color='gray', linewidth=0.5)
    
    # Draw dropoff zones (green squares)
    for x, y in warehouse.dropoff_zones:
        rect = patches.Rectangle((x, y), 1, 1, facecolor='lightgreen',
                                edgecolor='green', linewidth=2, alpha=0.4)
        ax1.add_patch(rect)
        ax1.text(x + 0.5, y + 0.5, 'DROP', ha='center', va='center',
                fontsize=8, fontweight='bold', color='green')
    
    # Draw items to pickup (brown boxes)
    for item_id, (x, y) in warehouse.items.items():
        rect = patches.Rectangle((x + 0.2, y + 0.2), 0.6, 0.6,
                                facecolor='brown', edgecolor='black', linewidth=2)
        ax1.add_patch(rect)
        ax1.text(x + 0.5, y + 0.5, str(item_id), ha='center', va='center',
                fontsize=8, color='white', fontweight='bold')
    
    # Draw agents
    colors = ['blue', 'red']
    for idx, agent in enumerate(agents):
        x, y = agent.pos
        color = colors[idx % len(colors)]
        
        # Agent body (square)
        rect = patches.Rectangle((x + 0.15, y + 0.15), 0.7, 0.7,
                                facecolor=color, edgecolor='white',
                                linewidth=2, alpha=0.9, zorder=10)
        ax1.add_patch(rect)
        ax1.text(x + 0.5, y + 0.5, str(agent.id), ha='center', va='center',
                color='white', fontweight='bold', fontsize=12, zorder=11)
        
        # Show if carrying item
        if agent.carrying_item:
            box = patches.Rectangle((x + 0.6, y + 0.6), 0.3, 0.3,
                                   facecolor='brown', edgecolor='black',
                                   linewidth=1, zorder=12)
            ax1.add_patch(box)
    
    completed = len(warehouse.completed)
    ax1.set_title(f'Step {step} | Completed: {completed}/{total_items}')
    
    # Statistics table
    ax2 = plt.subplot(1, 2, 2)
    ax2.axis('off')
    
    # Create table data
    table_data = [
        ['Metric', 'Agent 1', 'Agent 2', 'Total'],
        ['Items Completed', str(len(agents[0].completed_items)), 
         str(len(agents[1].completed_items)), str(completed)],
        ['Distance Traveled', str(agents[0].total_distance),
         str(agents[1].total_distance), 
         str(agents[0].total_distance + agents[1].total_distance)],
        ['Efficiency', 
         f'{len(agents[0].completed_items)/(agents[0].total_distance+1):.2f}',
         f'{len(agents[1].completed_items)/(agents[1].total_distance+1):.2f}',
         f'{completed/(agents[0].total_distance + agents[1].total_distance + 1):.2f}']
    ]
    
    table = ax2.table(cellText=table_data, cellLoc='center', loc='center',
                     colWidths=[0.3, 0.2, 0.2, 0.2])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style header row
    for i in range(4):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, 4):
        for j in range(4):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f0f0f0')
    
    ax2.set_title('Performance Metrics', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.pause(0.05)

# ============= MAIN SIMULATION =============
def run_warehouse():
    print("Starting Warehouse Pickup Team Simulation...")
    print("=" * 50)
    
    WAREHOUSE_SIZE = 12
    NUM_ITEMS = 10
    
    warehouse = WarehouseGrid(WAREHOUSE_SIZE)
    
    # Create dropoff zones (corners)
    dropoff_zones = [(0, 0), (WAREHOUSE_SIZE-1, WAREHOUSE_SIZE-1)]
    for zone in dropoff_zones:
        warehouse.add_dropoff_zone(zone)
    
    # Create random items
    items = {}
    for i in range(1, NUM_ITEMS + 1):
        x, y = random.randint(2, WAREHOUSE_SIZE-3), random.randint(2, WAREHOUSE_SIZE-3)
        while (x, y) in dropoff_zones:
            x, y = random.randint(2, WAREHOUSE_SIZE-3), random.randint(2, WAREHOUSE_SIZE-3)
        items[i] = (x, y)
        warehouse.add_item(i, (x, y))
    
    # Initialize agents at dropoff zones
    agent1 = WarehouseAgent(1, dropoff_zones[0])
    agent2 = WarehouseAgent(2, dropoff_zones[1])
    
    warehouse.add_agent(1, agent1.pos)
    warehouse.add_agent(2, agent2.pos)
    
    agents = [agent1, agent2]
    
    print(f"Warehouse size: {WAREHOUSE_SIZE}x{WAREHOUSE_SIZE}")
    print(f"Items to pickup: {NUM_ITEMS}")
    print(f"Dropoff zones: {len(dropoff_zones)}")
    
    # Simulation
    plt.figure(figsize=(12, 6))
    steps = 0
    max_steps = 400
    
    while steps < max_steps and len(warehouse.completed) < NUM_ITEMS:
        if steps % 10 == 0:
            print(f"\n{'='*50}")
            print(f"STEP {steps}")
            print('='*50)
        
        for agent in agents:
            # If not carrying and no path, assign nearest item
            if not agent.carrying_item and not agent.path:
                available = [item_id for item_id in warehouse.items.keys()
                           if item_id not in warehouse.completed.keys()]
                
                # Remove items being targeted by other agents
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
            
            # If carrying and no path, go to nearest dropoff
            elif agent.carrying_item and not agent.path:
                nearest_dropoff = min(warehouse.dropoff_zones,
                                    key=lambda d: abs(d[0]-agent.pos[0]) + abs(d[1]-agent.pos[1]))
                path = astar(agent.pos, nearest_dropoff, warehouse)
                if path:
                    agent.path = path[1:]
            
            # Move agent
            new_pos = agent.move()
            warehouse.move_agent(agent.id, new_pos)
            if (steps % 10 == 0) and (agent.path or agent.carrying_item):
                status = f"carrying item {agent.carrying_item}" if agent.carrying_item else "moving"
                print(f"Agent {agent.id}: Moved to {new_pos} ({status})")
            
            # Check pickup
            if agent.carrying_item and agent.carrying_item in warehouse.items:
                pickup_pos = warehouse.items[agent.carrying_item]
                if agent.pos == pickup_pos:
                    print(f"Step {steps}: Agent {agent.id} picked up item {agent.carrying_item}")
            
            # Check dropoff
            if agent.carrying_item and agent.pos in warehouse.dropoff_zones:
                if agent.carrying_item in warehouse.items:
                    warehouse.completed[agent.carrying_item] = agent.id
                    agent.completed_items.append(agent.carrying_item)
                    del warehouse.items[agent.carrying_item]
                    print(f"Step {steps}: Agent {agent.id} dropped off item {agent.carrying_item}")
                    agent.carrying_item = None
        
        # Visualize
        if steps % 5 == 0:
            visualize_warehouse(warehouse, agents, steps, NUM_ITEMS)
        
        steps += 1
    
    # Final results
    total_completed = len(warehouse.completed)
    total_distance = sum(agent.total_distance for agent in agents)
    overall_efficiency = (total_completed / total_distance) if total_distance > 0 else 0
    
    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"  Total Time: {steps} steps")
    print(f"  Items Completed: {total_completed}/{NUM_ITEMS}")
    print(f"  Agent 1: {len(agent1.completed_items)} items, {agent1.total_distance} distance")
    print(f"  Agent 2: {len(agent2.completed_items)} items, {agent2.total_distance} distance")
    print(f"  Total Distance: {total_distance}")
    print(f"  Overall Efficiency: {overall_efficiency:.3f} items/step")
    print(f"  Status: {'SUCCESS' if total_completed == NUM_ITEMS else 'PARTIAL'}")
    print(f"{'='*50}")
    
    visualize_warehouse(warehouse, agents, steps, NUM_ITEMS)
    plt.show()

if __name__ == "__main__":
    run_warehouse()
