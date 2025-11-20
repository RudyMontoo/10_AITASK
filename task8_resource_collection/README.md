# Resource Collection Team Simulation

## 📋 Overview
A multi-agent cooperative system where two collector agents work together to gather resources scattered across a map. The agents use a shared task queue and distributed decision logic to efficiently collect all resources.

## 🎯 Problem Statement
Design two collector agents that:
- Share a task queue of available resources
- Use distributed decision logic for task assignment
- Collect resources cooperatively without conflicts
- Minimize total collection time
- Balance workload between agents

## 🛠️ Requirements

### Python Version
- Python 3.7 or higher

### Dependencies
```bash
pip install matplotlib numpy
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

## 🚀 How to Run

### Step 1: Install Dependencies
```bash
pip install matplotlib numpy
```

### Step 2: Run the Simulation
```bash
python resource_collection.py
```

### Step 3: Watch the Visualization
- Left panel shows the grid with:
  - **Yellow stars** = Available resources
  - **Green circles** = Collected resources
  - **Blue circle** = Agent 1
  - **Red circle** = Agent 2
- Right panel shows a bar chart:
  - Resources collected by each agent over time

## 🧠 How It Works

### 1. Environment Setup
- Creates a 12x12 grid
- Scatters 15 resources randomly
- Initializes 2 collector agents at opposite corners

### 2. Shared Task Queue
- All resources start in a shared queue
- Both agents can see all available resources
- No resource is assigned to multiple agents

### 3. Distributed Decision Logic
- Each agent independently chooses nearest resource
- If both agents target same resource, closest one gets it
- Conflict resolution prevents duplicate collection
- Dynamic task allocation as resources are collected

### 4. Path Planning (A*)
- Agents use A* to find shortest path to target resource
- Avoid collisions with other agent
- Replan when target is taken by other agent

### 5. Collection Mechanics
- Agent collects resource when reaching its position
- Resource removed from shared queue
- Agent immediately plans for next resource
- Continue until all resources collected

## 📊 Output Example

```
Starting Resource Collection Simulation...
==================================================
Total resources: 15
Agent 1 starting at: (0, 0)
Agent 2 starting at: (11, 11)

Step 12: Agent 1 collected resource at (3, 2)
Step 18: Agent 2 collected resource at (9, 8)
Step 25: Agent 1 collected resource at (5, 4)
...

==================================================
RESULTS:
  Total Time: 89 steps
  Total Resources: 15
  Agent 1: 8 resources
  Agent 2: 7 resources
  Efficiency: 16.85 resources/100 steps
  Balance: 53.3% / 46.7%
==================================================
```

### Chart Output
The simulation shows:
- **Bar chart**: Resources collected by each agent
- **Timeline**: Collection progress over time
- **Efficiency metrics**: Resources per step

## 🎨 Customization

### Change Grid Size
```python
GRID_SIZE = 15  # Line 165
```

### Change Number of Resources
```python
NUM_RESOURCES = 20  # Line 166
```

### Adjust Visualization Speed
```python
if steps % 5 == 0:  # Update every 5 steps (Line 237)
    # Change to steps % 1 for real-time
```

### Change Decision Logic
Modify `select_next_resource()` (Line 82) to:
- Prioritize high-value resources
- Consider agent workload balance
- Use different distance metrics
- Add resource priorities

## 🏆 Hackathon Features

### What's Implemented
✅ A* pathfinding to resources  
✅ Shared task queue system  
✅ Distributed decision logic  
✅ Conflict resolution  
✅ Collision avoidance  
✅ Real-time dual visualization  
✅ Performance metrics  
✅ Workload balance tracking  
✅ Single-file implementation (270 lines)

### Possible Extensions
- Add resource values (different point values)
- Implement carrying capacity (limited inventory)
- Add resource respawn mechanics
- Create resource clusters/hotspots
- Add obstacles between resources
- Implement communication costs
- Add energy/fuel constraints
- Create competitive mode (agents compete)
- Add 3+ collector agents
- Implement auction-based task allocation

## 📁 Project Structure

```
task8_resource_collection/
├── resource_collection.py    # Main simulation file
├── README.md                  # This file
└── requirements.txt           # Python dependencies
```

## 🐛 Troubleshooting

**Issue: Agents target same resource**
- This is handled by conflict resolution logic
- Closest agent gets the resource
- Other agent replans automatically

**Issue: Unbalanced collection**
- This can happen with random placement
- Try different random seeds
- Implement workload-aware decision logic

**Issue: Slow performance**
- Increase visualization update interval (line 237)
- Reduce grid size or number of resources

**Issue: Agents stuck**
- Check A* pathfinding logic
- Verify collision avoidance is working

## 📝 Algorithm Details

### Shared Task Queue
- **Structure**: Set of uncollected resource positions
- **Access**: Both agents read from same queue
- **Updates**: Resources removed when collected
- **Thread-safe**: Single-threaded simulation (no race conditions)

### Distributed Decision Logic
1. Each agent independently evaluates all available resources
2. Selects nearest resource using Manhattan distance
3. Plans path using A*
4. Moves toward target
5. If target collected by other agent, immediately replan
6. No central coordinator needed

### Conflict Resolution
- **Detection**: Both agents target same resource
- **Resolution**: Agent closer to resource gets it
- **Replanning**: Other agent selects new target
- **Efficiency**: Minimizes wasted movement

### A* Pathfinding
- **Heuristic**: Manhattan distance
- **Cost**: Number of steps
- **Collision Avoidance**: Excludes other agent's position
- **Dynamic**: Replans when needed

## 🎓 Learning Outcomes

This project demonstrates:
- Shared resource management
- Distributed decision making
- Conflict resolution strategies
- Task queue implementation
- Cooperative vs competitive dynamics
- Load balancing in multi-agent systems

## 📊 Performance Metrics

### Efficiency
- **Formula**: (Resources collected / Total steps) × 100
- **Goal**: Maximize resources per step
- **Factors**: Path planning, decision logic, conflicts

### Balance
- **Formula**: Resources per agent / Total resources
- **Goal**: ~50% / 50% for 2 agents
- **Factors**: Starting positions, resource distribution

### Total Time
- **Metric**: Steps to collect all resources
- **Goal**: Minimize total time
- **Optimal**: Approaches (Total distance / 2 agents)

## 🎮 Challenge Modes

### Easy Mode
- 10 resources
- 10x10 grid
- No obstacles

### Normal Mode (Default)
- 15 resources
- 12x12 grid
- No obstacles

### Hard Mode
- 20 resources
- 15x15 grid
- Add obstacles

### Expert Mode
- 25 resources
- 15x15 grid
- Add obstacles
- Add resource values (prioritization needed)
- Limited carrying capacity

## 📄 License

Free to use for educational and hackathon purposes.

---

**Collect them all!** 💎 Good luck with your hackathon!
