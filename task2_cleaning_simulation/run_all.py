import os
os.environ['MPLBACKEND'] = 'Agg'

from environment.grid import GridEnvironment
from agents.cleaning_agent import CleaningAgent
from algorithms.astar import astar
from utils.metrics import calculate_efficiency
import random

def divide_tasks(dirty_cells, agent1_pos, agent2_pos):
    agent1_tasks = []
    agent2_tasks = []
    
    for cell in dirty_cells:
        dist1 = abs(cell[0] - agent1_pos[0]) + abs(cell[1] - agent1_pos[1])
        dist2 = abs(cell[0] - agent2_pos[0]) + abs(cell[1] - agent2_pos[1])
        
        if dist1 <= dist2:
            agent1_tasks.append(cell)
        else:
            agent2_tasks.append(cell)
    
    return agent1_tasks, agent2_tasks

width, height = 10, 10
env = GridEnvironment(width, height)

num_dirty = 20
dirty_cells = set()
while len(dirty_cells) < num_dirty:
    x, y = random.randint(0, width-1), random.randint(0, height-1)
    dirty_cells.add((x, y))

agent1 = CleaningAgent(1, (0, 0))
agent2 = CleaningAgent(2, (width-1, height-1))

env.add_agent(1, agent1.position)
env.add_agent(2, agent2.position)

tasks1, tasks2 = divide_tasks(dirty_cells, agent1.position, agent2.position)
agent1.assign_cells(tasks1)
agent2.assign_cells(tasks2)

steps = 0
max_steps = 200

while (dirty_cells - agent1.cleaned_cells - agent2.cleaned_cells) and steps < max_steps:
    if not agent1.has_path():
        remaining = [c for c in tasks1 if c not in agent1.cleaned_cells]
        if remaining:
            target = min(remaining, key=lambda c: abs(c[0]-agent1.position[0]) + abs(c[1]-agent1.position[1]))
            path = astar(agent1.position, target, env, {agent2.position})
            if path:
                agent1.set_path(path[1:])
    
    if not agent2.has_path():
        remaining = [c for c in tasks2 if c not in agent2.cleaned_cells]
        if remaining:
            target = min(remaining, key=lambda c: abs(c[0]-agent2.position[0]) + abs(c[1]-agent2.position[1]))
            path = astar(agent2.position, target, env, {agent1.position})
            if path:
                agent2.set_path(path[1:])
    
    new_pos1 = agent1.move()
    new_pos2 = agent2.move()
    
    env.move_agent(1, new_pos1)
    env.move_agent(2, new_pos2)
    
    if agent1.position in dirty_cells:
        agent1.clean_current_cell()
    if agent2.position in dirty_cells:
        agent2.clean_current_cell()
    
    steps += 1

print(f"Total Steps: {steps}")
