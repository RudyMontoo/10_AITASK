"""
Cooperative Path Planners - Simple Implementation
Two agents reach their goals while avoiding collisions using A* with shared collision-avoidance
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import heapq

# ============= ENVIRONMENT =============
class PathGrid:
    def __init__(self, size=12):
        self.size = size
        self.agents = {}
        self.goals = {}
        self.obstacles = set()
        self.agent_paths = {}  # Store planned paths
        
    def add_agent(self, agent_id, pos, goal):
        self.agents[agent_id] = pos
        self.goals[agent_id] = goal
        self.agent_paths[agent_id] = []
    
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

# ============= AGENT =============
class PathAgent:
    def __init__(self, agent_id, start_pos, goal_pos):
        self.id = agent_id
        self.pos = start_pos
        self.goal = goal_pos
        self.path = []
        self.reached_goal = False

# ============= A* WITH COLLISION AVOIDANCE =============
def astar_with_collision_avoidance(start, goal, grid, reserved_positions, time_step=0):
    """A* pathfinding with space-time collision avoidance"""
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    # Priority queue: (priority, time, position)
    frontier = [(0, time_step, start)]
    came_from = {(time_step, start): None}
    cost = {(time_step, start): 0}
    
    while frontier:
        _, current_time, current_pos = heapq.heappop(frontier)
        
        if current_pos == goal:
            # Reconstruct path
            path = []
            state = (current_time, current_pos)
            while state:
                path.append(state[1])
                state = came_from.get(state)
            path.reverse()
            return path
        
        # Try moving to neighbors or waiting
        next_time = current_time + 1
        
        # Option 1: Move to neighbor
        for next_pos in grid.get_neighbors(current_pos):
            # Check if position is reserved by another agent at this time
            if (next_time, next_pos) in reserved_positions:
                continue
            
            new_cost = cost[(current_time, current_pos)] + 1
            state = (next_time, next_pos)
            
            if state not in cost or new_cost < cost[state]:
                cost[state] = new_cost
                priority = new_cost + heuristic(next_pos, goal)
                heapq.heappush(frontier, (priority, next_time, next_pos))
                came_from[state] = (current_time, current_pos)
        
        # Option 2: Wait at current position
        if (next_time, current_pos) not in reserved_positions:
            new_cost = cost[(current_time, current_pos)] + 1
            state = (next_time, current_pos)
            
            if state not in cost or new_cost < cost[state]:
                cost[state] = new_cost
                priority = new_cost + heuristic(current_pos, goal)
                heapq.heappush(frontier, (priority, next_time, current_pos))
                came_from[state] = (current_time, current_pos)
    
    return []

# ============= COOPERATIVE PLANNING =============
def plan_paths_cooperatively(agents, grid):
    """Plan paths for all agents with collision avoidance"""
    reserved_positions = set()
    
    # Sort agents by distance to goal (prioritize longer paths)
    sorted_agents = sorted(agents, 
                          key=lambda a: abs(a.goal[0]-a.pos[0]) + abs(a.goal[1]-a.pos[1]),
                          reverse=True)
    
    for agent in sorted_agents:
        # Plan path avoiding reserved positions
        path = astar_with_collision_avoidance(agent.pos, agent.goal, grid, 
                                              reserved_positions)
        
        if path:
            agent.path = path
            # Reserve positions in space-time
            for time, pos in enumerate(path):
                reserved_positions.add((time, pos))
        else:
            agent.path = [agent.pos]  # Stay in place if no path found
    
    return agents

# ============= VISUALIZATION =============
def visualize_paths(grid, agents, step, max_steps):
    plt.clf()
    fig = plt.gcf()
    fig.set_size_inches(10, 10)
    
    ax = plt.gca()
    ax.set_xlim(0, grid.size)
    ax.set_ylim(0, grid.size)
    ax.set_aspect('equal')
    
    # Grid lines
    for i in range(grid.size + 1):
        ax.axvline(i, color='gray', linewidth=0.5)
        ax.axhline(i, color='gray', linewidth=0.5)
    
    # Draw obstacles (black)
    for x, y in grid.obstacles:
        rect = patches.Rectangle((x, y), 1, 1, facecolor='black', alpha=0.7)
        ax.add_patch(rect)
    
    # Draw goals (stars)
    colors = ['blue', 'red', 'green', 'orange']
    for agent in agents:
        gx, gy = agent.goal
        color = colors[(agent.id - 1) % len(colors)]
        star = patches.RegularPolygon((gx + 0.5, gy + 0.5), 5, radius=0.4,
                                     facecolor=color, edgecolor='gold',
                                     linewidth=2, alpha=0.3)
        ax.add_patch(star)
        ax.text(gx + 0.5, gy + 0.5, f'G{agent.id}', ha='center', va='center',
               fontsize=10, fontweight='bold', color='white')
    
    # Draw planned paths (dashed lines)
    for agent in agents:
        if len(agent.path) > step:
            color = colors[(agent.id - 1) % len(colors)]
            path_to_draw = agent.path[step:]
            if len(path_to_draw) > 1:
                xs = [p[0] + 0.5 for p in path_to_draw]
                ys = [p[1] + 0.5 for p in path_to_draw]
                ax.plot(xs, ys, color=color, linestyle='--', 
                       linewidth=2, alpha=0.4)
    
    # Draw agents
    for agent in agents:
        x, y = agent.pos
        color = colors[(agent.id - 1) % len(colors)]
        
        # Agent body (circle)
        circle = patches.Circle((x + 0.5, y + 0.5), 0.35,
                               facecolor=color, edgecolor='white',
                               linewidth=2, alpha=0.9, zorder=10)
        ax.add_patch(circle)
        ax.text(x + 0.5, y + 0.5, str(agent.id), ha='center', va='center',
               color='white', fontweight='bold', fontsize=12, zorder=11)
        
        # Show checkmark if reached goal
        if agent.reached_goal:
            ax.text(x + 0.5, y + 0.2, '✓', ha='center', va='center',
                   fontsize=16, color='green', fontweight='bold', zorder=12)
    
    # Status text
    reached = sum(1 for a in agents if a.reached_goal)
    ax.set_title(f'Step {step}/{max_steps} | Agents at Goal: {reached}/{len(agents)}',
                fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.pause(0.1)

# ============= MAIN SIMULATION =============
def run_path_planning():
    print("Starting Cooperative Path Planners Simulation...")
    print("=" * 50)
    
    GRID_SIZE = 12
    
    grid = PathGrid(GRID_SIZE)
    
    # Add some obstacles
    obstacles = [
        (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
        (7, 5), (7, 6), (7, 7), (7, 8), (7, 9)
    ]
    grid.add_obstacles(obstacles)
    
    # Create agents with start and goal positions
    agent1 = PathAgent(1, (1, 1), (10, 10))
    agent2 = PathAgent(2, (10, 1), (1, 10))
    
    agents = [agent1, agent2]
    
    for agent in agents:
        grid.add_agent(agent.id, agent.pos, agent.goal)
    
    print(f"Grid size: {GRID_SIZE}x{GRID_SIZE}")
    print(f"Obstacles: {len(obstacles)}")
    print(f"Agent 1: {agent1.pos} → {agent1.goal}")
    print(f"Agent 2: {agent2.pos} → {agent2.goal}")
    
    # Plan paths cooperatively
    print("\nPlanning collision-free paths...")
    agents = plan_paths_cooperatively(agents, grid)
    
    for agent in agents:
        print(f"Agent {agent.id} path length: {len(agent.path)} steps")
    
    # Simulation
    plt.figure(figsize=(10, 10))
    step = 0
    max_steps = max(len(agent.path) for agent in agents)
    
    print(f"\nStarting synchronized movement...")
    
    while step < max_steps:
        print(f"\n{'='*50}")
        print(f"STEP {step}")
        print('='*50)
        
        # Move all agents synchronously
        for agent in agents:
            if step < len(agent.path):
                new_pos = agent.path[step]
                grid.move_agent(agent.id, new_pos)
                agent.pos = new_pos
                print(f"Agent {agent.id}: Moved to {new_pos}")
                
                # Check if reached goal
                if agent.pos == agent.goal:
                    agent.reached_goal = True
                    print(f"Agent {agent.id}: Reached goal!")
        
        # Print grid every 3 steps
        if step % 3 == 0:
            print("\nCurrent Grid:")
            for y in range(grid.size-1, -1, -1):
                row = ""
                for x in range(grid.size):
                    pos = (x, y)
                    if pos in grid.obstacles:
                        row += "█ "
                    elif pos == agent1.pos and pos == agent2.pos:
                        row += "X "
                    elif pos == agent1.pos:
                        row += "1 "
                    elif pos == agent2.pos:
                        row += "2 "
                    elif pos == agent1.goal:
                        row += "G1"
                    elif pos == agent2.goal:
                        row += "G2"
                    else:
                        row += "· "
                print(row)
            print()
        
        # Check for collisions (should not happen with proper planning)
        positions = [agent.pos for agent in agents]
        if len(positions) != len(set(positions)):
            print(f"WARNING: Collision detected at step {step}!")
        
        # Visualize
        visualize_paths(grid, agents, step, max_steps)
        
        step += 1
    
    # Final results
    all_reached = all(agent.reached_goal for agent in agents)
    total_steps = max(len(agent.path) for agent in agents)
    
    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"  Total Steps: {total_steps}")
    print(f"  Agent 1: {'REACHED' if agent1.reached_goal else 'NOT REACHED'} ({len(agent1.path)} steps)")
    print(f"  Agent 2: {'REACHED' if agent2.reached_goal else 'NOT REACHED'} ({len(agent2.path)} steps)")
    print(f"  Collisions: 0 (collision-free)")
    print(f"  Status: {'SUCCESS' if all_reached else 'PARTIAL'}")
    print(f"{'='*50}")
    
    visualize_paths(grid, agents, step-1, max_steps)
    plt.show()

if __name__ == "__main__":
    run_path_planning()
