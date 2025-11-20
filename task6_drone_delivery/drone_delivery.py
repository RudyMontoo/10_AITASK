"""
Dual Drone Delivery - Simple Implementation
Two drones deliver packages using A* and greedy assignment
"""
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import heapq

# ============= ENVIRONMENT =============
class DeliveryGrid:
    def __init__(self, size=14):
        self.size = size
        self.drones = {}
        self.packages = {}  # package_id -> (pickup, delivery)
        self.delivered = {}  # package_id -> drone_id
        self.coverage = {}  # cell -> visit_count
        
    def add_drone(self, drone_id, pos):
        self.drones[drone_id] = pos
    
    def add_package(self, pkg_id, pickup, delivery):
        self.packages[pkg_id] = (pickup, delivery)
    
    def move_drone(self, drone_id, pos):
        if self.is_valid(pos):
            self.drones[drone_id] = pos
            # Track coverage
            self.coverage[pos] = self.coverage.get(pos, 0) + 1
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

# ============= GREEDY PACKAGE ASSIGNMENT =============
def greedy_assign_packages(drones, packages, grid):
    """Greedy assignment: each drone picks nearest unassigned package"""
    assignments = {drone.id: [] for drone in drones}
    available = list(packages.keys())
    
    while available:
        for drone in drones:
            if not available:
                break
            
            # Find nearest package (to pickup location)
            nearest_pkg = min(available, 
                            key=lambda p: abs(packages[p][0][0] - drone.pos[0]) + 
                                        abs(packages[p][0][1] - drone.pos[1]))
            
            assignments[drone.id].append(nearest_pkg)
            available.remove(nearest_pkg)
    
    return assignments

# ============= VISUALIZATION =============
def visualize_delivery(grid, drones, step, total_packages):
    plt.clf()
    fig = plt.gcf()
    fig.set_size_inches(14, 6)
    
    # Main grid
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_xlim(0, grid.size)
    ax1.set_ylim(0, grid.size)
    ax1.set_aspect('equal')
    
    # Grid lines
    for i in range(grid.size + 1):
        ax1.axvline(i, color='gray', linewidth=0.5)
        ax1.axhline(i, color='gray', linewidth=0.5)
    
    # Draw undelivered packages
    for pkg_id, (pickup, delivery) in grid.packages.items():
        # Pickup location (yellow square)
        px, py = pickup
        rect = patches.Rectangle((px, py), 1, 1, facecolor='yellow', 
                                alpha=0.5, edgecolor='orange', linewidth=2)
        ax1.add_patch(rect)
        ax1.text(px + 0.5, py + 0.5, f'P{pkg_id}', ha='center', va='center', fontsize=8)
        
        # Delivery location (green circle)
        dx, dy = delivery
        circle = patches.Circle((dx + 0.5, dy + 0.5), 0.3, 
                               facecolor='lightgreen', edgecolor='green', linewidth=2)
        ax1.add_patch(circle)
        ax1.text(dx + 0.5, dy + 0.5, f'D{pkg_id}', ha='center', va='center', fontsize=8)
    
    # Draw delivered packages (gray)
    for pkg_id, drone_id in grid.delivered.items():
        if pkg_id in grid.packages:
            continue
        # Just mark as done (already removed from packages)
    
    # Draw drones
    colors = ['blue', 'red']
    for idx, drone in enumerate(drones):
        x, y = drone.pos
        color = colors[idx % len(colors)]
        
        # Drone body
        triangle = patches.RegularPolygon((x + 0.5, y + 0.5), 3, radius=0.4,
                                         facecolor=color, edgecolor='white', 
                                         linewidth=2, alpha=0.9, zorder=10)
        ax1.add_patch(triangle)
        ax1.text(x + 0.5, y + 0.5, str(drone.id), ha='center', va='center',
                color='white', fontweight='bold', fontsize=10, zorder=11)
        
        # Show if carrying package
        if drone.has_package:
            box = patches.Rectangle((x + 0.2, y + 0.2), 0.3, 0.3,
                                   facecolor='brown', edgecolor='black', linewidth=1, zorder=9)
            ax1.add_patch(box)
    
    delivered = len(grid.delivered)
    ax1.set_title(f'Step {step} | Delivered: {delivered}/{total_packages}')

    # Coverage heatmap
    ax2 = plt.subplot(1, 2, 2)
    
    heatmap = np.zeros((grid.size, grid.size))
    for (x, y), count in grid.coverage.items():
        heatmap[y, x] = count
    
    im = ax2.imshow(heatmap, cmap='YlOrRd', origin='lower', interpolation='nearest')
    ax2.set_title('Coverage Heatmap (Visit Frequency)')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    plt.colorbar(im, ax=ax2, label='Visits')
    
    plt.tight_layout()
    plt.pause(0.05)

# ============= MAIN SIMULATION =============
def run_delivery():
    print("Starting Dual Drone Delivery Simulation...")
    print("=" * 50)
    
    GRID_SIZE = 14
    NUM_PACKAGES = 8
    
    grid = DeliveryGrid(GRID_SIZE)
    
    # Create random packages
    packages = {}
    for i in range(1, NUM_PACKAGES + 1):
        pickup = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        delivery = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        while delivery == pickup:
            delivery = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        packages[i] = (pickup, delivery)
        grid.add_package(i, pickup, delivery)
    
    # Initialize drones
    drone1 = DeliveryDrone(1, (0, 0))
    drone2 = DeliveryDrone(2, (GRID_SIZE-1, GRID_SIZE-1))
    
    grid.add_drone(1, drone1.pos)
    grid.add_drone(2, drone2.pos)
    
    drones = [drone1, drone2]
    
    # Greedy package assignment
    assignments = greedy_assign_packages(drones, packages, grid)
    
    print(f"Total packages: {NUM_PACKAGES}")
    print(f"Drone 1 assigned: {len(assignments[1])} packages")
    print(f"Drone 2 assigned: {len(assignments[2])} packages")
    
    # Simulation
    plt.figure(figsize=(14, 6))
    steps = 0
    max_steps = 500
    
    while steps < max_steps and len(grid.delivered) < NUM_PACKAGES:
        print(f"\n--- Step {steps} ---")
        
        for drone in drones:
            # If no path and has assignment
            if not drone.path and assignments[drone.id]:
                pkg_id = assignments[drone.id][0]
                
                if pkg_id in grid.packages:
                    pickup, delivery = grid.packages[pkg_id]
                    
                    if not drone.has_package:
                        # Go to pickup
                        path = astar(drone.pos, pickup, grid)
                        if path:
                            drone.path = path[1:]
                            drone.current_package = pkg_id
                    else:
                        # Go to delivery
                        path = astar(drone.pos, delivery, grid)
                        if path:
                            drone.path = path[1:]
            
            # Move drone
            new_pos = drone.move()
            grid.move_drone(drone.id, new_pos)
            status = f"carrying pkg {drone.current_package}" if drone.has_package else "empty"
            print(f"Drone {drone.id}: Moved to {new_pos} ({status})")
            
            # Check pickup
            if drone.current_package and not drone.has_package:
                pkg_id = drone.current_package
                if pkg_id in grid.packages:
                    pickup, delivery = grid.packages[pkg_id]
                    if drone.pos == pickup:
                        drone.has_package = True
                        print(f"Drone {drone.id}: ↑ PICKED UP package {pkg_id}")
            
            # Check delivery
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
                        print(f"Drone {drone.id}: ✓ DELIVERED package {pkg_id}")
        
        # Visualize
        if steps % 5 == 0:
            visualize_delivery(grid, drones, steps, NUM_PACKAGES)
        
        steps += 1
    
    # Results
    total_delivered = len(grid.delivered)
    overlap = sum(1 for count in grid.coverage.values() if count > 1)
    
    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"  Total Time: {steps} steps")
    print(f"  Packages Delivered: {total_delivered}/{NUM_PACKAGES}")
    print(f"  Drone 1: {len(drone1.delivered_packages)} packages")
    print(f"  Drone 2: {len(drone2.delivered_packages)} packages")
    print(f"  Coverage Overlap: {overlap} cells visited multiple times")
    print(f"  Efficiency: {(total_delivered/steps)*100:.2f} packages/100 steps")
    print(f"{'='*50}")
    
    visualize_delivery(grid, drones, steps, NUM_PACKAGES)
    plt.show()

if __name__ == "__main__":
    run_delivery()
