import os
os.environ['MPLBACKEND'] = 'Agg'

import numpy as np
import heapq

class PathGrid:
    def __init__(self, size=12):
        self.size = size
        self.agents = {}
        self.goals = {}
        self.obstacles = set()
        self.agent_paths = {}
        
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

class PathAgent:
    def __init__(self, agent_id, start_pos, goal_pos):
        self.id = agent_id
        self.pos = start_pos
        self.goal = goal_pos
        self.path = []
        self.reached_goal = False

def astar_with_collision_avoidance(start, goal, grid, reserved_positions, time_step=0):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    frontier = [(0, time_step, start)]
    came_from = {(time_step, start): None}
    cost = {(time_step, start): 0}
    
    while frontier:
        _, current_time, current_pos = heapq.heappop(frontier)
        
        if current_pos == goal:
            path = []
            state = (current_time, current_pos)
            while state:
                path.append(state[1])
                state = came_from.get(state)
            path.reverse()
            return path
        
        next_time = current_time + 1
        
        for next_pos in grid.get_neighbors(current_pos):
            if (next_time, next_pos) in reserved_positions:
                continue
            
            new_cost = cost[(current_time, current_pos)] + 1
            state = (next_time, next_pos)
            
            if state not in cost or new_cost < cost[state]:
                cost[state] = new_cost
                priority = new_cost + heuristic(next_pos, goal)
                heapq.heappush(frontier, (priority, next_time, next_pos))
                came_from[state] = (current_time, current_pos)
        
        if (next_time, current_pos) not in reserved_positions:
            new_cost = cost[(current_time, current_pos)] + 1
            state = (next_time, current_pos)
            
            if state not in cost or new_cost < cost[state]:
                cost[state] = new_cost
                priority = new_cost + heuristic(current_pos, goal)
                heapq.heappush(frontier, (priority, next_time, current_pos))
                came_from[state] = (current_time, current_pos)
    
    return []

def plan_paths_cooperatively(agents, grid):
    reserved_positions = set()
    
    sorted_agents = sorted(agents, 
                          key=lambda a: abs(a.goal[0]-a.pos[0]) + abs(a.goal[1]-a.pos[1]),
                          reverse=True)
    
    for agent in sorted_agents:
        path = astar_with_collision_avoidance(agent.pos, agent.goal, grid, 
                                              reserved_positions)
        
        if path:
            agent.path = path
            for time, pos in enumerate(path):
                reserved_positions.add((time, pos))
        else:
            agent.path = [agent.pos]
    
    return agents

GRID_SIZE = 12
grid = PathGrid(GRID_SIZE)

obstacles = [
    (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
    (7, 5), (7, 6), (7, 7), (7, 8), (7, 9)
]
grid.add_obstacles(obstacles)

agent1 = PathAgent(1, (1, 1), (10, 10))
agent2 = PathAgent(2, (10, 1), (1, 10))

agents = [agent1, agent2]

for agent in agents:
    grid.add_agent(agent.id, agent.pos, agent.goal)

agents = plan_paths_cooperatively(agents, grid)

step = 0
max_steps = max(len(agent.path) for agent in agents)

while step < max_steps:
    for agent in agents:
        if step < len(agent.path):
            new_pos = agent.path[step]
            grid.move_agent(agent.id, new_pos)
            agent.pos = new_pos
            
            if agent.pos == agent.goal:
                agent.reached_goal = True
    
    step += 1

total_steps = max(len(agent.path) for agent in agents)
print(f"Total Steps: {total_steps}")
