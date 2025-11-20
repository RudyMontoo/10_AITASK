# Map Exploration Partners Simulation

## 📋 Overview
A multi-agent cooperative system where two explorer agents work together to map unknown regions. The agents divide the exploration area using grid partitioning and efficiently explore all accessible cells while avoiding obstacles.

## 🎯 Problem Statement
Design two exploration agents that:
- Divide unexplored regions using grid partitioning logic
- Explore unknown areas cooperatively
- Avoid obstacles and collisions
- Maximize exploration efficiency

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
python exploration_simulation.py
```

### Step 3: Watch the Visualization
- A window will open showing the exploration grid
- **Green cells** = Explored
- **Red cells** = Obstacles
- **White/Yellow cells** = Unexplored
- **Blue circle** = Agent 1
- **Red circle** = Agent 2
- Watch as both agents explore their assigned regions

## 🧠 How It Works

### 1. Environment Setup
- Creates a 15x15 grid
- Randomly places 20 obstacles
- Initializes 2 agents at opposite corners

### 2. Grid Partitioning
- Divides grid vertically into two regions
- Agent 1 gets left half
- Agent 2 gets right half
- Ensures balanced exploration workload

### 3. Path Planning (BFS)
- Each agent uses BFS to find nearest unexplored cell in their region
- Avoids obstacles and other agent's position
- Explores systematically

### 4. Coordination
- Agents explore their assigned regions
- Mark cells as explored when visited
- Avoid collisions with each other
- Continue until all accessible cells explored

### 5. Metrics
- Total steps taken
- Cells explored by each agent
- Coverage percentage
- Exploration efficiency (cells/step)

## 📊 Output Example

```
Starting Map Exploration Simulation...
==================================================
Agent 1 region: 105 cells
Agent 2 region: 110 cells
Obstacles: 20

==================================================
RESULTS:
  Total Steps: 234
  Cells Explored: 205/205
  Agent 1: 103 cells
  Agent 2: 108 cells
  Coverage: 100.0%
  Efficiency: 0.88 cells/step
==================================================
```

### Heatmap Output
The simulation generates a 3-panel heatmap showing:
1. **Agent 1's exploration** (blue heatmap)
2. **Agent 2's exploration** (red heatmap)
3. **Combined exploration** (green = explored, red = obstacles)

## 🎨 Customization

### Change Grid Size
```python
GRID_SIZE = 20  # Line 189
```

### Change Number of Obstacles
```python
NUM_OBSTACLES = 30  # Line 190
```

### Adjust Visualization Speed
```python
if steps % 10 == 0:  # Update every 10 steps (Line 249)
    # Change to steps % 1 for real-time
```

### Change Partitioning Strategy
Modify the `partition_grid()` function (Line 93) to:
- Horizontal split
- Quadrant division (for 4 agents)
- Checkerboard pattern
- Distance-based allocation

## 🏆 Hackathon Features

### What's Implemented
✅ BFS pathfinding for exploration  
✅ Grid partitioning for task division  
✅ Collision avoidance  
✅ Real-time visualization  
✅ Exploration heatmap  
✅ Efficiency metrics  
✅ Single-file implementation (300 lines)

### Possible Extensions
- Add 3+ agents for larger grids
- Dynamic region reallocation
- Communication between agents (share discovered obstacles)
- Priority zones (explore certain areas first)
- Energy/battery constraints
- Unknown obstacle discovery (fog of war)
- Different partitioning strategies

## 📁 Project Structure

```
task3_map_exploration/
├── exploration_simulation.py    # Main simulation file
├── README.md                     # This file
└── requirements.txt              # Python dependencies
```

## 🐛 Troubleshooting

**Issue: No visualization window appears**
- Make sure matplotlib is installed: `pip install matplotlib`
- Try running with: `python -i exploration_simulation.py`

**Issue: Agents stuck or not exploring**
- Check if obstacles are blocking paths
- Restart simulation for different random obstacle placement

**Issue: Slow performance**
- Reduce grid size
- Increase visualization update interval (line 249)

## 📝 Algorithm Details

### BFS Exploration
- **Strategy**: Find nearest unexplored cell in assigned region
- **Queue**: FIFO queue for breadth-first search
- **Collision Avoidance**: Excludes other agent's position
- **Termination**: When all accessible cells explored

### Grid Partitioning
- **Strategy**: Vertical split for 2 agents
- **Balance**: Approximately equal cells per agent
- **Flexibility**: Easy to extend to more agents or different patterns

### Exploration Efficiency
- **Metric**: (Total explorable cells / Total steps) × 100
- **Goal**: Minimize redundant movement
- **Optimization**: Region-based assignment reduces overlap

## 🎓 Learning Outcomes

This project demonstrates:
- Multi-agent exploration strategies
- Grid partitioning algorithms
- BFS pathfinding
- Cooperative task allocation
- Heatmap visualization
- Spatial coverage optimization

## 🔄 Comparison with Cleaning Crew

| Feature | Cleaning Crew | Map Exploration |
|---------|---------------|-----------------|
| Algorithm | A* (goal-directed) | BFS (exploration) |
| Task | Clean specific cells | Explore all cells |
| Allocation | Proximity-based | Region-based |
| Visualization | Dirty/Clean cells | Heatmap coverage |
| Metric | Cleaning efficiency | Exploration coverage |

## 📄 License

Free to use for educational and hackathon purposes.

---

**Ready to explore!** 🗺️ Good luck with your hackathon!
