"""
Rescue Bot Squad - Simple Implementation
Two rescue bots find and rescue trapped victims in a maze using BFS
"""
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from collections import deque

# ============= ENVIRONMENT =============
class MazeGrid:
    def __init__(self, size=14):
        self.size = size
        self.bots = {}
        self.walls = set()
        self.victims = set()
        self.rescued = {}  # victim_pos -> bot_id
        
    def add_bot(self, bot_id, pos):
        self.bots[bot_id] = pos
    
    def add_walls(self, wall_list):
        self.walls = set(wall_list)
    
    def add_victims(self, victim_list):
        self.victims = set(victim_list)
    
    def move_bot(self, bot_id, pos):
        if self.is_valid(pos):
            self.bots[bot_id] = pos
            return True
        return False
    
    def is_valid(self, pos):
        x, y = pos
        return (0 <= x < self.size and 0 <= y < self.size and 
                pos not in self.walls)
    
    def rescue_victim(self, pos, bot_id):
        if pos in self.victims:
            self.victims.remove(pos)
            self.rescued[pos] = bot_id
            return True
        return False
    
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
class RescueBot:
    def __init__(self, bot_id, start_pos):
        self.id = bot_id
        self.pos = start_pos
        self.path = []
        self.rescued_victims = []
        self.assigned_zone = None
    
    def assign_zone(self, zone):
        self.assigned_zone = zone
    
    def move(self):
        if self.path:
            self.pos = self.path.pop(0)
        return self.pos

# ============= BFS PATHFINDING =============
def bfs_to_victim(start, victims, maze, avoid=None):
    """BFS to find nearest victim"""
    if avoid is None:
        avoid = set()
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        if current in victims:
            return path
        
        for next_pos in maze.get_neighbors(current):
            if next_pos not in visited and next_pos not in avoid:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    
    return []

# ============= ZONE ALLOCATION =============
def allocate_rescue_zones(maze_size, num_bots=2):
    """Divide maze into rescue zones"""
    zones = [set() for _ in range(num_bots)]
    
    mid = maze_size // 2
    
    for x in range(maze_size):
        for y in range(maze_size):
            if x < mid:
                zones[0].add((x, y))
            else:
                zones[1].add((x, y))
    
    return zones

# ============= MAZE GENERATION =============
def generate_maze_walls(size, density=0.2):
    """Generate random maze walls"""
    walls = set()
    num_walls = int(size * size * density)
    
    while len(walls) < num_walls:
        x, y = random.randint(1, size-2), random.randint(1, size-2)
        if (x, y) not in [(0, 0), (size-1, size-1)]:
            walls.add((x, y))
    
    return walls

# ============= VISUALIZATION =============
def visualize_rescue(maze, bots, step, total_victims):
    plt.clf()
    fig = plt.gcf()
    fig.set_size_inches(12, 6)
    
    # Main maze view
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_xlim(0, maze.size)
    ax1.set_ylim(0, maze.size)
    ax1.set_aspect('equal')
    
    # Grid lines
    for i in range(maze.size + 1):
        ax1.axvline(i, color='gray', linewidth=0.5)
        ax1.axhline(i, color='gray', linewidth=0.5)
    
    # Draw walls (black)
    for x, y in maze.walls:
        rect = patches.Rectangle((x, y), 1, 1, facecolor='black', alpha=0.8)
        ax1.add_patch(rect)
    
    # Draw rescued victims (green)
    for pos, bot_id in maze.rescued.items():
        x, y = pos
        circle = patches.Circle((x + 0.5, y + 0.5), 0.3, 
                               facecolor='lightgreen', edgecolor='green', 
                               linewidth=2, alpha=0.6)
        ax1.add_patch(circle)
        ax1.text(x + 0.5, y + 0.5, '✓', ha='center', va='center', 
                fontsize=14, color='green', fontweight='bold')
    
    # Draw victims needing rescue (red)
    for x, y in maze.victims:
        circle = patches.Circle((x + 0.5, y + 0.5), 0.3, 
                               facecolor='red', edgecolor='darkred', 
                               linewidth=2, alpha=0.8)
        ax1.add_patch(circle)
        ax1.text(x + 0.5, y + 0.5, '!', ha='center', va='center', 
                fontsize=14, color='white', fontweight='bold')
    
    # Draw rescue bots
    colors = ['blue', 'cyan']
    for idx, bot in enumerate(bots):
        x, y = bot.pos
        color = colors[idx % len(colors)]
        
        # Bot body (hexagon)
        hexagon = patches.RegularPolygon((x + 0.5, y + 0.5), 6, radius=0.35,
                                        facecolor=color, edgecolor='white', 
                                        linewidth=2, alpha=0.9, zorder=10)
        ax1.add_patch(hexagon)
        ax1.text(x + 0.5, y + 0.5, str(bot.id), ha='center', va='center',
                color='white', fontweight='bold', fontsize=10, zorder=11)
    
    rescued_count = len(maze.rescued)
    ax1.set_title(f'Step {step} | Rescued: {rescued_count}/{total_victims}')
    
    # Statistics bar chart
    ax2 = plt.subplot(1, 2, 2)
    
    bot_ids = [bot.id for bot in bots]
    rescues = [len(bot.rescued_victims) for bot in bots]
    colors_bar = ['blue', 'cyan']
    
    bars = ax2.bar(bot_ids, rescues, color=colors_bar, alpha=0.7, 
                   edgecolor='black', linewidth=2)
    
    for bar, count in zip(bars, rescues):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    ax2.set_xlabel('Bot ID', fontsize=12)
    ax2.set_ylabel('Victims Rescued', fontsize=12)
    ax2.set_title('Rescue Performance', fontsize=14)
    ax2.set_ylim(0, total_victims + 2)
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_xticks(bot_ids)
    
    plt.tight_layout()
    plt.pause(0.05)

# ============= MAIN SIMULATION =============
def run_rescue():
    print("Starting Rescue Bot Squad Simulation...")
    print("=" * 50)
    
    MAZE_SIZE = 14
    NUM_VICTIMS = 10
    WALL_DENSITY = 0.15
    
    maze = MazeGrid(MAZE_SIZE)
    
    # Generate maze walls
    walls = generate_maze_walls(MAZE_SIZE, WALL_DENSITY)
    maze.add_walls(walls)
    
    # Place victims randomly (not on walls or start positions)
    victims = set()
    while len(victims) < NUM_VICTIMS:
        x, y = random.randint(1, MAZE_SIZE-2), random.randint(1, MAZE_SIZE-2)
        if ((x, y) not in walls and 
            (x, y) not in [(0, 0), (MAZE_SIZE-1, MAZE_SIZE-1)]):
            victims.add((x, y))
    
    maze.add_victims(victims)
    
    # Initialize rescue bots
    bot1 = RescueBot(1, (0, 0))
    bot2 = RescueBot(2, (MAZE_SIZE-1, MAZE_SIZE-1))
    
    maze.add_bot(1, bot1.pos)
    maze.add_bot(2, bot2.pos)
    
    bots = [bot1, bot2]
    
    # Allocate rescue zones
    zones = allocate_rescue_zones(MAZE_SIZE, 2)
    bot1.assign_zone(zones[0])
    bot2.assign_zone(zones[1])
    
    print(f"Maze size: {MAZE_SIZE}x{MAZE_SIZE}")
    print(f"Walls: {len(walls)}")
    print(f"Victims: {NUM_VICTIMS}")
    print(f"Bot 1 zone: {len(zones[0])} cells")
    print(f"Bot 2 zone: {len(zones[1])} cells")
    
    # Simulation
    plt.figure(figsize=(12, 6))
    steps = 0
    max_steps = 400
    
    while steps < max_steps and len(maze.victims) > 0:
        print(f"\n{'='*50}")
        print(f"STEP {steps}")
        print('='*50)
        
        for bot in bots:
            # Plan path to nearest victim
            if not bot.path:
                # Prioritize victims in assigned zone
                zone_victims = maze.victims & bot.assigned_zone
                target_victims = zone_victims if zone_victims else maze.victims
                
                if target_victims:
                    path = bfs_to_victim(bot.pos, target_victims, maze)
                    if path:
                        bot.path = path[1:]
            
            # Move bot
            new_pos = bot.move()
            maze.move_bot(bot.id, new_pos)
            print(f"Bot {bot.id}: Moved to {new_pos}")
            
            # Rescue victim
            if maze.rescue_victim(bot.pos, bot.id):
                bot.rescued_victims.append(bot.pos)
                print(f"Bot {bot.id}: ✓ RESCUED victim at {bot.pos}")
        
        # Print maze every 5 steps
        if steps % 5 == 0:
            print("\nCurrent Maze:")
            for y in range(maze.size-1, -1, -1):
                row = ""
                for x in range(maze.size):
                    pos = (x, y)
                    if pos in maze.walls:
                        row += "█ "
                    elif pos == bot1.pos and pos == bot2.pos:
                        row += "X "
                    elif pos == bot1.pos:
                        row += "1 "
                    elif pos == bot2.pos:
                        row += "2 "
                    elif pos in maze.victims:
                        row += "V "
                    elif pos in maze.rescued:
                        row += "✓ "
                    else:
                        row += "· "
                print(row)
            print(f"Victims remaining: {len(maze.victims)}")
            print()
        
        # Visualize
        if steps % 5 == 0:
            visualize_rescue(maze, bots, steps, NUM_VICTIMS)
        
        steps += 1
    
    # Final results
    total_rescued = len(maze.rescued)
    success_rate = (total_rescued / NUM_VICTIMS) * 100
    efficiency = (total_rescued / steps) * 100 if steps > 0 else 0
    
    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"  Total Time: {steps} steps")
    print(f"  Victims Rescued: {total_rescued}/{NUM_VICTIMS}")
    print(f"  Bot 1: {len(bot1.rescued_victims)} rescues")
    print(f"  Bot 2: {len(bot2.rescued_victims)} rescues")
    print(f"  Success Rate: {success_rate:.1f}%")
    print(f"  Efficiency: {efficiency:.2f} rescues/100 steps")
    print(f"  Status: {'SUCCESS' if total_rescued == NUM_VICTIMS else 'PARTIAL'}")
    print(f"{'='*50}")
    
    visualize_rescue(maze, bots, steps, NUM_VICTIMS)
    plt.show()

if __name__ == "__main__":
    run_rescue()
