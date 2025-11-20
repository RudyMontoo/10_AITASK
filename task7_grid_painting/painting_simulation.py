"""
Grid Painting Agents - Simple Implementation
Two painting robots paint cells without overlapping using DFS
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ============= ENVIRONMENT =============
class PaintingGrid:
    def __init__(self, size=12):
        self.size = size
        self.agents = {}
        self.painted = {}  # cell -> agent_id
        
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
        """Paint cell with agent's color"""
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

# ============= AGENT =============
class PaintingRobot:
    def __init__(self, agent_id, start_pos):
        self.id = agent_id
        self.pos = start_pos
        self.painted_cells = set()
        self.assigned_region = None
    
    def assign_region(self, region):
        """Assign region (set of cells) to paint"""
        self.assigned_region = region

# ============= REGION ALLOCATION =============
def allocate_regions(grid_size, num_robots=2):
    """Divide grid into non-overlapping regions"""
    regions = [set() for _ in range(num_robots)]
    
    # Vertical split for 2 robots
    mid = grid_size // 2
    
    for x in range(grid_size):
        for y in range(grid_size):
            if x < mid:
                regions[0].add((x, y))
            else:
                regions[1].add((x, y))
    
    return regions

# ============= DFS PAINTING =============
def dfs_paint(robot, grid, current_pos):
    """DFS traversal to paint all cells in region"""
    # Paint current cell
    if current_pos in robot.assigned_region and not grid.is_painted(current_pos):
        grid.paint_cell(current_pos, robot.id)
        robot.painted_cells.add(current_pos)
        grid.move_agent(robot.id, current_pos)
        return current_pos
    
    # Find unpainted neighbor in region
    for neighbor in grid.get_neighbors(current_pos):
        if neighbor in robot.assigned_region and not grid.is_painted(neighbor):
            return neighbor
    
    return None

# ============= VISUALIZATION =============
def visualize_painting(grid, robots, step, total_cells):
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
    
    # Draw painted cells
    colors = ['blue', 'red', 'green', 'orange']
    for pos, agent_id in grid.painted.items():
        x, y = pos
        color = colors[(agent_id - 1) % len(colors)]
        rect = patches.Rectangle((x, y), 1, 1, facecolor=color, alpha=0.6)
        ax1.add_patch(rect)
    
    # Draw robots
    for idx, robot in enumerate(robots):
        x, y = robot.pos
        color = colors[idx % len(colors)]
        circle = patches.Circle((x + 0.5, y + 0.5), 0.35, 
                               color=color, alpha=0.9, zorder=10, edgecolor='white', linewidth=2)
        ax1.add_patch(circle)
        ax1.text(x + 0.5, y + 0.5, str(robot.id), ha='center', va='center', 
                color='white', fontweight='bold', zorder=11)
    
    painted_count = len(grid.painted)
    coverage = (painted_count / total_cells) * 100
    ax1.set_title(f'Step {step} | Painted: {painted_count}/{total_cells} ({coverage:.1f}%)')
    
    # Pie chart showing coverage by each robot
    ax2 = plt.subplot(1, 2, 2)
    
    robot_counts = [len(robot.painted_cells) for robot in robots]
    robot_labels = [f'Robot {robot.id}\n{count} cells' for robot, count in zip(robots, robot_counts)]
    colors_pie = [colors[i % len(colors)] for i in range(len(robots))]
    
    if sum(robot_counts) > 0:
        wedges, texts, autotexts = ax2.pie(robot_counts, labels=robot_labels, colors=colors_pie,
                                           autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
        for autotext in autotexts:
            autotext.set_color('white')
    
    ax2.set_title('Paint Coverage by Robot', fontsize=14)
    
    plt.tight_layout()
    plt.pause(0.05)

# ============= MAIN SIMULATION =============
def run_painting():
    print("Starting Grid Painting Simulation...")
    print("=" * 50)
    
    # Setup
    GRID_SIZE = 12
    
    grid = PaintingGrid(GRID_SIZE)
    
    # Allocate regions
    regions = allocate_regions(GRID_SIZE, 2)
    
    # Initialize robots at region boundaries
    robot1 = PaintingRobot(1, (0, 0))
    robot2 = PaintingRobot(2, (GRID_SIZE // 2, 0))
    
    robot1.assign_region(regions[0])
    robot2.assign_region(regions[1])
    
    grid.add_agent(1, robot1.pos)
    grid.add_agent(2, robot2.pos)
    
    robots = [robot1, robot2]
    
    total_cells = GRID_SIZE * GRID_SIZE
    
    print(f"Grid size: {GRID_SIZE}x{GRID_SIZE} ({total_cells} cells)")
    print(f"Robot 1 region: {len(regions[0])} cells")
    print(f"Robot 2 region: {len(regions[1])} cells")
    
    # Simulation
    plt.figure(figsize=(12, 6))
    steps = 0
    max_steps = 300
    
    # DFS stacks for each robot
    stacks = [[robot.pos] for robot in robots]
    
    while steps < max_steps:
        print(f"\n--- Step {steps} ---")
        all_done = True
        
        for idx, robot in enumerate(robots):
            # Check if robot has unpainted cells in region
            unpainted_in_region = robot.assigned_region - robot.painted_cells
            
            if unpainted_in_region:
                all_done = False
                
                # DFS painting
                if stacks[idx]:
                    current = stacks[idx][-1]
                    
                    # Paint current cell
                    if current in robot.assigned_region and not grid.is_painted(current):
                        grid.paint_cell(current, robot.id)
                        robot.painted_cells.add(current)
                        grid.move_agent(robot.id, current)
                        print(f"Robot {robot.id}: Painted cell at {current}")
                    
                    # Find unpainted neighbor
                    found_neighbor = False
                    for neighbor in grid.get_neighbors(current):
                        if neighbor in robot.assigned_region and not grid.is_painted(neighbor):
                            stacks[idx].append(neighbor)
                            found_neighbor = True
                            break
                    
                    # Backtrack if no unpainted neighbors
                    if not found_neighbor:
                        stacks[idx].pop()
                        if stacks[idx]:
                            grid.move_agent(robot.id, stacks[idx][-1])
        
        # Visualize
        if steps % 3 == 0:
            visualize_painting(grid, robots, steps, total_cells)
        
        steps += 1
        
        # Check if all cells painted
        if all_done or len(grid.painted) >= total_cells:
            break
    
    # Final results
    painted_count = len(grid.painted)
    coverage = (painted_count / total_cells) * 100
    efficiency = (painted_count / steps) * 100 if steps > 0 else 0
    
    # Check for overlaps (should be zero)
    overlaps = 0
    for robot in robots:
        for other_robot in robots:
            if robot.id != other_robot.id:
                overlaps += len(robot.painted_cells & other_robot.painted_cells)
    
    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"  Total Time: {steps} steps")
    print(f"  Total Cells: {total_cells}")
    print(f"  Robot 1: {len(robot1.painted_cells)} cells ({len(robot1.painted_cells)/total_cells*100:.1f}%)")
    print(f"  Robot 2: {len(robot2.painted_cells)} cells ({len(robot2.painted_cells)/total_cells*100:.1f}%)")
    print(f"  Coverage: {coverage:.1f}%")
    print(f"  Efficiency: {efficiency:.2f} cells/100 steps")
    print(f"  No Overlaps: {'✓' if overlaps == 0 else '✗ (' + str(overlaps) + ')'}")
    print(f"{'='*50}")
    
    # Final visualization
    visualize_painting(grid, robots, steps, total_cells)
    plt.show()

if __name__ == "__main__":
    run_painting()
