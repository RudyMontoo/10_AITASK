# Cooperative Firefighters Simulation

## 📋 Overview
A multi-agent cooperative system where two firefighter agents work together to extinguish fires in a grid environment. The simulation includes realistic fire spreading mechanics where fires can grow and spread to adjacent cells over time.

## 🎯 Problem Statement
Design two firefighter agents that:
- Extinguish fires in different zones efficiently
- Coordinate to prevent fire spread
- Use BFS for pathfinding to nearest fires
- Prioritize fires in their assigned zones
- Work cooperatively to handle spreading fires

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
python firefighter_simulation.py
```

### Step 3: Watch the Visualization
- Left panel shows the grid with:
  - **Red/Orange cells** = Active fires (with intensity numbers)
  - **Gray cells** = Extinguished fires
  - **Blue circle** = Firefighter 1
  - **Cyan circle** = Firefighter 2
- Right panel shows a graph of:
  - **Red line** = Active fires over time
  - **Green line** = Extinguished fires over time

## 🧠 How It Works

### 1. Environment Setup
- Creates a 12x12 grid
- Places 8 initial fires randomly
- Initializes 2 firefighter agents at opposite corners

### 2. Fire Mechanics
- **Fire Intensity**: Fires grow stronger over time (shown as numbers)
- **Fire Spread**: Every 5 steps, fires can spread to adjacent cells (30% probability)
- **Challenge**: Agents must extinguish fires faster than they spread

### 3. Zone Allocation
- Grid divided vertically into two zones
- Each agent prioritizes fires in their zone
- Can help in other zones if their zone is clear

### 4. Path Planning (BFS)
- Agents use BFS to find shortest path to nearest fire
- Prioritize fires in assigned zone
- Avoid collisions with other agent

### 5. Coordination
- Agents move step-by-step toward fires
- Extinguish fire when they reach it
- Dynamically replan as new fires appear
- Work together to contain spreading fires

## 📊 Output Example

```
Starting Cooperative Firefighters Simulation...
==================================================
Initial fires: 8
Agent 1 zone: 72 cells
Agent 2 zone: 72 cells
Step 5: 2 new fires spread!
Step 10: 1 new fires spread!

==================================================
RESULTS:
  Total Time: 87 steps
  Total Fires: 11
  Extinguished: 11
  Still Burning: 0
  Agent 1: 5 fires
  Agent 2: 6 fires
  Success Rate: 100.0%
  Status: SUCCESS
==================================================
```

### Graph Output
The simulation shows a real-time graph with:
- **X-axis**: Time steps
- **Y-axis**: Number of fires
- **Red area**: Active fires (should decrease)
- **Green area**: Extinguished fires (should increase)

## 🎨 Customization

### Change Grid Size
```python
GRID_SIZE = 15  # Line 177
```

### Change Initial Fires
```python
NUM_INITIAL_FIRES = 12  # Line 178
```

### Adjust Fire Spread Rate
```python
FIRE_SPREAD_INTERVAL = 3  # Spread every 3 steps (Line 179)
grid.spread_prob = 0.5  # 50% spread probability (Line 17)
```

### Visualization Speed
```python
if steps % 3 == 0:  # Update every 3 steps (Line 254)
    # Change to steps % 1 for real-time
```

## 🏆 Hackathon Features

### What's Implemented
✅ BFS pathfinding to nearest fire  
✅ Fire spread simulation (realistic)  
✅ Zone-based task allocation  
✅ Fire intensity tracking  
✅ Collision avoidance  
✅ Real-time dual visualization (grid + graph)  
✅ Performance metrics  
✅ Single-file implementation (280 lines)

### Possible Extensions
- Add water/resource management (limited water supply)
- Implement fire prediction (AI predicts spread)
- Add obstacles/buildings that block movement
- Priority fires (save important buildings)
- 3+ firefighter agents
- Wind direction affecting fire spread
- Different fire types (intensity, spread rate)
- Rescue missions (save people while fighting fires)

## 📁 Project Structure

```
task9_firefighters/
├── firefighter_simulation.py    # Main simulation file
├── README.md                     # This file
└── requirements.txt              # Python dependencies
```

## 🐛 Troubleshooting

**Issue: Fires spread too fast**
- Reduce `spread_prob` (line 17): `self.spread_prob = 0.2`
- Increase `FIRE_SPREAD_INTERVAL` (line 179)

**Issue: Agents can't keep up**
- Reduce initial fires
- Decrease fire spread probability
- Add more agents

**Issue: Simulation too slow**
- Increase visualization update interval (line 254)
- Reduce grid size

**Issue: Graph not showing**
- Make sure matplotlib is installed
- Check if window is behind other windows

## 📝 Algorithm Details

### BFS Pathfinding
- **Goal**: Find shortest path to nearest fire
- **Priority**: Fires in assigned zone first
- **Collision Avoidance**: Excludes other agent's position
- **Dynamic**: Replans when fire is extinguished

### Fire Spread Simulation
- **Mechanism**: Each fire can spread to 4 adjacent cells
- **Probability**: 30% chance per neighbor per spread cycle
- **Intensity**: Fires grow stronger over time (affects visualization)
- **Realism**: Simulates how real fires spread

### Zone Allocation
- **Strategy**: Vertical split for 2 agents
- **Flexibility**: Agents help in other zones when needed
- **Balance**: Approximately equal area per agent

### Cooperative Strategy
1. Each agent patrols their zone
2. Prioritize fires in own zone
3. Help with fires in other zones if own zone is clear
4. Avoid collisions while moving
5. Dynamically adapt to new fires

## 🎓 Learning Outcomes

This project demonstrates:
- Multi-agent coordination under pressure
- Dynamic task allocation
- BFS pathfinding
- Simulation of spreading phenomena
- Real-time data visualization
- Emergency response strategies

## 🔥 Challenge Modes

### Easy Mode
- 5 initial fires
- Spread interval: 10 steps
- Spread probability: 20%

### Normal Mode (Default)
- 8 initial fires
- Spread interval: 5 steps
- Spread probability: 30%

### Hard Mode
- 12 initial fires
- Spread interval: 3 steps
- Spread probability: 40%

### Extreme Mode
- 15 initial fires
- Spread interval: 2 steps
- Spread probability: 50%
- Add obstacles!

## 📄 License

Free to use for educational and hackathon purposes.

---

**Fight the fires!** 🔥🚒 Good luck with your hackathon!
