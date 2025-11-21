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
def allocate_regions(grid_size, num_robots=4):
    """Divide grid into non-overlapping regions (quadrants for 4 robots)"""
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
    
    # Draw obstacles (black)
    for x, y in grid.obstacles:
        rect = patches.Rectangle((x, y), 1, 1, facecolor='black', alpha=0.8)
        ax1.add_patch(rect)
    
    # Draw painted cells with vibrant colors
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    for pos, agent_id in grid.painted.items():
        x, y = pos
        color = colors[(agent_id - 1) % len(colors)]
        rect = patches.Rectangle((x, y), 1, 1, facecolor=color, alpha=0.7, edgecolor='white', linewidth=0.5)
        ax1.add_patch(rect)
    
    # Draw robots with bold colors
    for robot in robots:
        x, y = robot.pos
        color = colors[(robot.id - 1) % len(colors)]
        circle = patches.Circle((x + 0.5, y + 0.5), 0.4, 
                               color=color, alpha=1.0, zorder=10, edgecolor='white', linewidth=3)
        ax1.add_patch(circle)
        ax1.text(x + 0.5, y + 0.5, str(robot.id), ha='center', va='center', 
                color='white', fontweight='bold', fontsize=12, zorder=11)
    
    painted_count = len(grid.painted)
    paintable_cells = total_cells - len(grid.obstacles)
    coverage = (painted_count / paintable_cells) * 100
    ax1.set_title(f'Step {step} | Painted: {painted_count}/{paintable_cells} ({coverage:.1f}%)')
    
    # Dynamic bar chart showing coverage by each robot (grows from 0)
    ax2 = plt.subplot(1, 2, 2)
    ax2.clear()
    
    robot_counts = [len(robot.painted_cells) for robot in robots]
    robot_ids = [robot.id for robot in robots]
    colors_bar = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    
    # Set fixed y-axis limit so bars grow upward
    max_cells_per_robot = paintable_cells // len(robots) + 20
    ax2.set_ylim(0, max_cells_per_robot)
    
    bars = ax2.bar(robot_ids, robot_counts, color=colors_bar[:len(robots)], 
                   alpha=0.8, edgecolor='white', linewidth=2)
    
    # Add count labels on top of bars
    for bar, count in zip(bars, robot_counts):
        height = bar.get_height()
        if height > 0:
            ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{count}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    ax2.set_xlabel('Robot ID', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Cells Painted', fontsize=12, fontweight='bold')
    ax2.set_title('Paint Coverage by Robot (Live)', fontsize=14, fontweight='bold')
    ax2.set_xticks(robot_ids)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.pause(0.05)

# ============= MAIN SIMULATION =============
def run_painting():
    print("Starting Grid Painting Simulation...")
    print("=" * 50)
    
    # Setup
    GRID_SIZE = 16
    
    grid = PaintingGrid(GRID_SIZE)
    
    # Add obstacles (walls in the middle)
    obstacles = []
    mid = GRID_SIZE // 2
    for i in range(4, 12):
        if i != mid:
            obstacles.append((mid - 1, i))
            obstacles.append((mid, i))
    
    grid.add_obstacles(obstacles)
    
    # Allocate regions (4 quadrants)
    regions = allocate_regions(GRID_SIZE, 4)
    
    # Remove obstacles from regions
    for region in regions:
        region -= grid.obstacles
    
    # Initialize 4 robots at corners
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
    
    print(f"Grid size: {GRID_SIZE}x{GRID_SIZE} ({total_cells} cells)")
    print(f"Obstacles: {len(obstacles)} cells")
    print(f"Paintable cells: {total_cells - len(obstacles)}")
    print(f"Robot 1 region: {len(regions[0])} cells")
    print(f"Robot 2 region: {len(regions[1])} cells")
    print(f"Robot 3 region: {len(regions[2])} cells")
    print(f"Robot 4 region: {len(regions[3])} cells")
    
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
    
    paintable_cells = total_cells - len(grid.obstacles)
    coverage = (painted_count / paintable_cells) * 100
    
    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"  Total Time: {steps} steps")
    print(f"  Total Cells: {total_cells}")
    print(f"  Obstacles: {len(grid.obstacles)}")
    print(f"  Paintable Cells: {paintable_cells}")
    print(f"  Robot 1: {len(robot1.painted_cells)} cells")
    print(f"  Robot 2: {len(robot2.painted_cells)} cells")
    print(f"  Robot 3: {len(robot3.painted_cells)} cells")
    print(f"  Robot 4: {len(robot4.painted_cells)} cells")
    print(f"  Coverage: {coverage:.1f}%")
    print(f"  Efficiency: {efficiency:.2f} cells/100 steps")
    print(f"  No Overlaps: {'✓' if overlaps == 0 else '✗ (' + str(overlaps) + ')'}")
    print(f"{'='*50}")
    
    # Final visualization
    visualize_painting(grid, robots, steps, total_cells)
    plt.show()

if __name__ == "__main__":
    run_painting()
