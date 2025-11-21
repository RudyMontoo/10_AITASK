import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import heapq


# ============= ENVIRONMENT =============
class ResourceGrid:
    def __init__(self, size=30):
        self.size = size
        self.agents = {}
        self.resources = set()
        self.collected = {}

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
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            new_pos = (nx, ny)
            if self.is_valid(new_pos):
                neighbors.append(new_pos)
        return neighbors

    def collect_resource(self, pos, agent_id):
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
        if not available_resources:
            return None

        nearest = min(available_resources,
                      key=lambda r: abs(r[0] - self.pos[0]) + abs(r[1] - self.pos[1]))
        return nearest


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


# ============= VISUALIZATION =============
def visualize_collection(grid, agents, step, total_resources, collection_history):
    plt.clf()
    fig = plt.gcf()
    fig.set_size_inches(12, 6)

    ax1 = plt.subplot(1, 2, 1)
    ax1.set_xlim(0, grid.size)
    ax1.set_ylim(0, grid.size)
    ax1.set_aspect('equal')

    for i in range(grid.size + 1):
        ax1.axvline(i, color='gray', linewidth=0.5)
        ax1.axhline(i, color='gray', linewidth=0.5)

    for agent_id, resources in grid.collected.items():
        for x, y in resources:
            circle = patches.Circle((x + 0.5, y + 0.5), 0.2,
                                    facecolor='lightgreen', edgecolor='green',
                                    linewidth=2, alpha=0.5)
            ax1.add_patch(circle)

    for x, y in grid.resources:
        star = patches.RegularPolygon((x + 0.5, y + 0.5), 5, radius=0.3,
                                      facecolor='yellow', edgecolor='orange',
                                      linewidth=2, alpha=0.9)
        ax1.add_patch(star)

    colors = ['blue', 'red', 'green', 'purple']
    for idx, agent in enumerate(agents):
        x, y = agent.pos
        circle = patches.Circle((x + 0.5, y + 0.5), 0.35,
                                color=colors[idx], alpha=0.9, zorder=10)
        ax1.add_patch(circle)
        ax1.text(x + 0.5, y + 0.5, str(agent.id), ha='center', va='center',
                 color='white', fontweight='bold', zorder=11)

    collected = sum(len(r) for r in grid.collected.values())
    ax1.set_title(f'Step {step} | Collected: {collected}/{total_resources}')

    ax2 = plt.subplot(1, 2, 2)

    agent_ids = [agent.id for agent in agents]
    collections = [len(grid.collected.get(agent.id, [])) for agent in agents]
    colors_bar = ['blue', 'red', 'green', 'purple']

    bars = ax2.bar(agent_ids, collections, color=colors_bar, alpha=0.7, edgecolor='black', linewidth=2)

    for bar, count in zip(bars, collections):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2., height,
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

    GRID_SIZE = 30
    NUM_RESOURCES = 80

    grid = ResourceGrid(GRID_SIZE)

    resources = set()
    while len(resources) < NUM_RESOURCES:
        x, y = random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2)
        resources.add((x, y))

    grid.add_resources(resources)

    agent1 = CollectorAgent(1, (0, 0))
    agent2 = CollectorAgent(2, (GRID_SIZE - 1, GRID_SIZE - 1))
    agent3 = CollectorAgent(3, (0, GRID_SIZE - 1))
    agent4 = CollectorAgent(4, (GRID_SIZE - 1, 0))

    grid.add_agent(1, agent1.pos)
    grid.add_agent(2, agent2.pos)
    grid.add_agent(3, agent3.pos)
    grid.add_agent(4, agent4.pos)

    agents = [agent1, agent2, agent3, agent4]

    print(f"Total resources: {NUM_RESOURCES}")

    plt.figure(figsize=(12, 6))
    steps = 0
    max_steps = 600

    while steps < max_steps and len(grid.resources) > 0:

        # Decision logic for all agents
        for agent in agents:
            avoid_positions = {a.pos for a in agents if a.id != agent.id}
            if not agent.path or agent.target not in grid.resources:
                agent.target = agent.select_next_resource(grid.resources)
                if agent.target:
                    path = astar(agent.pos, agent.target, grid, avoid_positions)
                    if path:
                        agent.path = path[1:]

        # Move all agents
        for agent in agents:
            new_pos = agent.move()
            grid.move_agent(agent.id, new_pos)

        # Collect resources
        for agent in agents:
            if grid.collect_resource(agent.pos, agent.id):
                agent.collected.append(agent.pos)

        if steps % 5 == 0:
            visualize_collection(grid, agents, steps, NUM_RESOURCES, [])

        steps += 1

    print(f"\n{'=' * 50}")
    print("Final Results:")
    for agent in agents:
        print(f"  Agent {agent.id}: {len(agent.collected)} collected")
    print(f"{'=' * 50}")

    visualize_collection(grid, agents, steps, NUM_RESOURCES, [])
    plt.show()


if __name__ == "__main__":
    run_collection()
