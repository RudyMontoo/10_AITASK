# Cooperative Path Planners Simulation

## 📋 Overview
A multi-agent path planning system where two agents must reach their respective goals while avoiding collisions with each other and obstacles. The system uses A* pathfinding with space-time collision avoidance for synchronized, collision-free movement.

## 🎯 Problem Statement
Design two path planning agents that:
- Navigate to their individual goal positions
- Avoid collisions with each other
- Navigate around obstacles
- Use A* with shared collision-avoidance logic
- Move synchronously in coordinated fashion

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
python path_planning.py
```

### Step 3: Watch the Visualization
- Grid shows:
  - **Black cells** = Obstacles
  - **Colored stars** = Goal positions (G1, G2)
  - **Colored circles** = Agents (1, 2)
  - **Dashed lines** = Planned paths ahead
  - **Green checkmark** = Agent reached goal
- Animation shows synchronized movement step-by-step

## 🧠 How It Works

### 1. Environment Setup
- Creates a 12x12 grid
- Places obstacles in the middle
- Agent 1: (1,1) → (10,10) (diagonal)
- Agent 2: (10,1) → (1,10) (crossing paths!)

### 2. Space-Time A* Planning
- Traditional A* finds shortest path
- Space-time A* adds time dimension
- Each position reserved at specific time
- Prevents collisions by design

### 3. Cooperative Planning
- Agents plan sequentially
- Priority given to longer paths
- Each agent reserves space-time positions
- Later agents plan around reservations

### 4. Collision Avoidance Strategies
- **Spatial**: Avoid same position at same time
- **Temporal**: Wait if position is reserved
- **Predictive**: Plan considers future positions
- **Guaranteed**: Zero collisions by design

### 5. Synchronized Movement
- All agents move simultaneously each step
- Follow pre-planned collision-free paths
- Smooth, coordinated motion
- Deterministic execution

## 📊 Output Example

```
Starting Cooperative Path Planners Simulation...
==================================================
Grid size: 12x12
Obstacles: 10
Agent 1: (1, 1) → (10, 10)
Agent 2: (10, 1) → (1, 10)

Planning collision-free paths...
Agent 1 path length: 18 steps
Agent 2 path length: 19 steps

Starting synchronized movement...

==================================================
RESULTS:
  Total Steps: 19
  Agent 1: REACHED (18 steps)
  Agent 2: REACHED (19 steps)
  Collisions: 0 (collision-free)
  Status: SUCCESS
==================================================
```

### Visual Output
- **Grid animation**: Shows agents moving synchronously
- **Path visualization**: Dashed lines show planned routes
- **Goal indicators**: Stars mark destinations
- **Status updates**: Real-time progress tracking

## 🎨 Customization

### Change Grid Size
```python
GRID_SIZE = 15  # Line 137
```

### Change Start/Goal Positions
```python
agent1 = PathAgent(1, (0, 0), (11, 11))  # Line 148
agent2 = PathAgent(2, (11, 0), (0, 11))  # Line 149
```

### Add More Obstacles
```python
obstacles = [(5,5), (6,5), (7,5), ...]  # Line 141
```

### Adjust Animation Speed
```python
plt.pause(0.1)  # Line 193 - decrease for faster
```

## 🏆 Hackathon Features

### What's Implemented
✅ A* pathfinding with space-time collision avoidance  
✅ Cooperative path planning  
✅ Synchronized movement  
✅ Obstacle avoidance  
✅ Grid animation  
✅ Path visualization  
✅ Collision detection  
✅ Single-file implementation (220 lines)

### Possible Extensions
- Add 3+ agents
- Implement dynamic replanning (moving obstacles)
- Add agent priorities (emergency vehicles)
- Create different movement speeds
- Implement communication delays
- Add uncertainty (sensor noise)
- Create 3D pathfinding
- Implement swarm coordination
- Add energy constraints
- Create competitive scenarios
- Implement formation control
- Add dynamic goals (moving targets)

## 📁 Project Structure

```
task3_path_planners/
├── path_planning.py    # Main simulation file
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## 🐛 Troubleshooting

**Issue: Agents collide**
- This shouldn't happen with proper space-time planning
- Check reservation logic (line 56-60)
- Verify cooperative planning (line 78-95)

**Issue: No path found**
- Too many obstacles blocking paths
- Reduce obstacle density
- Check start/goal positions are reachable

**Issue: Agents wait unnecessarily**
- This is normal for collision avoidance
- Agent may wait for other agent to pass
- Indicates proper coordination

**Issue: Slow planning**
- Space-time A* is computationally expensive
- Reduce grid size
- Limit planning horizon

## 📝 Algorithm Details

### Space-Time A*
- **State**: (time, position) instead of just position
- **Heuristic**: Manhattan distance (spatial only)
- **Cost**: Time steps taken
- **Reservation**: Each (time, position) reserved by one agent
- **Waiting**: Agent can stay at position if needed

### Cooperative Planning
- **Priority**: Longer paths planned first
- **Sequential**: Agents plan one at a time
- **Reservation**: Earlier agents reserve space-time
- **Adaptation**: Later agents plan around reservations

### Collision Types Prevented
1. **Vertex collision**: Same position, same time
2. **Edge collision**: Agents swap positions
3. **Following collision**: Agent catches up to another

## 🎓 Learning Outcomes

This project demonstrates:
- Space-time pathfinding
- Multi-agent coordination
- Collision avoidance strategies
- Cooperative planning
- Synchronized execution
- A* algorithm variants

## 📊 Performance Metrics

### Path Length
- **Metric**: Steps to reach goal
- **Goal**: Minimize path length
- **Trade-off**: May increase to avoid collisions

### Planning Time
- **Metric**: Time to compute paths
- **Complexity**: O(n × b^d) where n=agents
- **Trade-off**: Better paths vs faster planning

### Collisions
- **Metric**: Number of collisions
- **Goal**: Zero collisions
- **Guarantee**: Space-time planning ensures this

### Efficiency
- **Metric**: Path length vs optimal
- **Formula**: Actual length / Shortest path length
- **Goal**: Close to 1.0 (optimal)

## 🚦 Coordination Strategies

### Prioritized Planning (Implemented)
- Agents plan sequentially
- Simple and fast
- May not be globally optimal

### Conflict-Based Search (Extension)
- Find conflicts and resolve
- Optimal solution
- More computationally expensive

### Velocity Obstacles (Extension)
- Continuous space planning
- Real-time replanning
- Good for dynamic environments

### Potential Fields (Extension)
- Attractive force to goal
- Repulsive force from agents
- Reactive coordination

## 🔄 Comparison with Other Tasks

| Feature | Path Planners | Cleaning | Exploration |
|---------|---------------|----------|-------------|
| Algorithm | Space-Time A* | A* | BFS |
| Coordination | Cooperative | Independent | Zone-based |
| Collision | Avoided | Avoided | Avoided |
| Planning | Pre-planned | Dynamic | Dynamic |
| Movement | Synchronized | Asynchronous | Asynchronous |

## 💡 Advanced Concepts

### Space-Time Planning
- Adds time as dimension
- Prevents future collisions
- Enables waiting strategies
- Guarantees collision-free paths

### Reservation System
- Each agent reserves positions
- Other agents respect reservations
- Enables decentralized execution
- Scales to many agents

### Synchronized Execution
- All agents move together
- Predictable behavior
- Easy to verify correctness
- Suitable for real-time systems

## 📄 License

Free to use for educational and hackathon purposes.

---

**Plan your paths!** 🛤️🤖 Good luck with your hackathon!
