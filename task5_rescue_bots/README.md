# Rescue Bot Squad Simulation

## 📋 Overview
A multi-agent rescue system where two rescue bots navigate through a maze to find and rescue trapped victims. The bots use BFS (Breadth-First Search) for pathfinding and logic-based zone assignment for efficient rescue operations.

## 🎯 Problem Statement
Design two rescue bots that:
- Navigate through a maze with walls/obstacles
- Find and rescue trapped victims
- Use BFS for exploration and pathfinding
- Coordinate using zone-based assignment
- Minimize total rescue time

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
python rescue_simulation.py
```

### Step 3: Watch the Visualization
- Left panel shows the maze with:
  - **Black cells** = Walls/obstacles
  - **Red circles with !** = Victims needing rescue
  - **Green circles with ✓** = Rescued victims
  - **Blue hexagon** = Rescue Bot 1
  - **Cyan hexagon** = Rescue Bot 2
- Right panel shows:
  - **Bar chart** = Number of rescues by each bot

## 🧠 How It Works

### 1. Environment Setup
- Creates a 14x14 maze
- Generates random walls (15% density)
- Places 10 victims randomly
- Initializes 2 rescue bots at opposite corners

### 2. Zone Allocation (Logic-Based)
- Maze divided vertically into two zones
- Bot 1 assigned left zone
- Bot 2 assigned right zone
- Bots prioritize victims in their zone
- Can rescue in other zones if needed

### 3. BFS Pathfinding
- Bots use BFS to find shortest path to nearest victim
- Avoids walls and obstacles
- Guarantees shortest path in unweighted maze
- Efficient exploration

### 4. Rescue Process
1. Bot identifies nearest victim (prioritize own zone)
2. Uses BFS to plan path
3. Navigates through maze
4. Rescues victim upon arrival
5. Immediately plans for next victim

### 5. Coordination
- Zone-based assignment reduces conflicts
- Bots work independently in their zones
- Help in other zones when own zone is clear
- No collision (different zones)

## 📊 Output Example

```
Starting Rescue Bot Squad Simulation...
==================================================
Maze size: 14x14
Walls: 29
Victims: 10
Bot 1 zone: 98 cells
Bot 2 zone: 98 cells

Step 8: Bot 1 rescued victim at (3, 5)
Step 15: Bot 2 rescued victim at (11, 8)
Step 22: Bot 1 rescued victim at (5, 3)
Step 28: Bot 2 rescued victim at (10, 11)
...

==================================================
RESULTS:
  Total Time: 87 steps
  Victims Rescued: 10/10
  Bot 1: 5 rescues
  Bot 2: 5 rescues
  Success Rate: 100.0%
  Efficiency: 11.49 rescues/100 steps
  Status: SUCCESS
==================================================
```

### Visual Output
- **Maze view**: Real-time rescue operations
- **Bar chart**: Rescue performance comparison
- **Status indicators**: Clear victim status (! vs ✓)

## 🎨 Customization

### Change Maze Size
```python
MAZE_SIZE = 20  # Line 145
```

### Change Number of Victims
```python
NUM_VICTIMS = 15  # Line 146
```

### Adjust Wall Density
```python
WALL_DENSITY = 0.25  # 25% walls (Line 147)
```

### Visualization Speed
```python
if steps % 5 == 0:  # Update every 5 steps (Line 195)
    # Change to steps % 1 for real-time
```

## 🏆 Hackathon Features

### What's Implemented
✅ BFS pathfinding through maze  
✅ Logic-based zone assignment  
✅ Random maze generation  
✅ Victim rescue mechanics  
✅ Real-time visualization  
✅ Performance metrics  
✅ Success tracking  
✅ Single-file implementation (240 lines)

### Possible Extensions
- Add victim priorities (critical vs stable)
- Implement medical supplies (limited capacity)
- Add time limits (victims in danger)
- Create multi-floor mazes (3D)
- Add dynamic obstacles (collapsing walls)
- Implement communication between bots
- Add battery/energy constraints
- Create different victim types (injured, trapped)
- Implement 3+ rescue bots
- Add rescue difficulty levels
- Create evacuation routes
- Add hazard zones (fire, gas)

## 📁 Project Structure

```
task5_rescue_bots/
├── rescue_simulation.py    # Main simulation file
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## 🐛 Troubleshooting

**Issue: Bots can't reach victims**
- Check wall density (too high blocks paths)
- Verify BFS implementation
- Ensure victims not surrounded by walls

**Issue: Unbalanced rescues**
- This can happen with random victim placement
- Adjust zone boundaries
- Implement dynamic reallocation

**Issue: Slow performance**
- Reduce maze size
- Increase visualization update interval (line 195)
- Decrease wall density

**Issue: Bots stuck**
- Check for unreachable areas
- Verify BFS pathfinding logic

## 📝 Algorithm Details

### BFS (Breadth-First Search)
- **Strategy**: Explore level by level
- **Queue**: FIFO queue for frontier
- **Optimality**: Shortest path in unweighted graph
- **Complexity**: O(V + E) where V=vertices, E=edges
- **Use Case**: Perfect for maze navigation

### Zone-Based Assignment
- **Strategy**: Divide maze into regions
- **Method**: Vertical split for 2 bots
- **Priority**: Victims in own zone first
- **Flexibility**: Help in other zones when needed
- **Benefit**: Reduces travel distance and conflicts

### Maze Generation
- **Method**: Random wall placement
- **Density**: Configurable (default 15%)
- **Constraints**: Avoid start positions
- **Validation**: Ensure paths exist

## 🎓 Learning Outcomes

This project demonstrates:
- BFS pathfinding algorithm
- Maze navigation strategies
- Zone-based task allocation
- Emergency response coordination
- Real-time decision making
- Multi-agent rescue operations

## 📊 Performance Metrics

### Success Rate
- **Formula**: (Rescued / Total victims) × 100
- **Goal**: 100% success rate
- **Factors**: Maze complexity, bot coordination

### Efficiency
- **Formula**: (Rescues / Total steps) × 100
- **Goal**: Maximize rescues per step
- **Optimal**: Depends on maze layout

### Response Time
- **Metric**: Steps to first rescue
- **Goal**: Minimize initial response
- **Indicates**: Bot readiness

### Balance
- **Metric**: Rescues per bot
- **Goal**: Equal distribution
- **Ideal**: 50% / 50% for 2 bots

## 🚨 Rescue Scenarios

### Easy Mode
- 10x10 maze
- 5 victims
- 10% wall density
- Wide corridors

### Normal Mode (Default)
- 14x14 maze
- 10 victims
- 15% wall density
- Mixed corridors

### Hard Mode
- 18x18 maze
- 15 victims
- 20% wall density
- Narrow passages

### Extreme Mode
- 20x20 maze
- 20 victims
- 25% wall density
- Complex maze structure
- Add time limits

## 🔄 Comparison with Other Tasks

| Feature | Rescue Bots | Firefighters | Exploration |
|---------|-------------|--------------|-------------|
| Algorithm | BFS | BFS | BFS |
| Environment | Maze | Open grid | Open grid |
| Task | Rescue victims | Extinguish fires | Explore cells |
| Urgency | High | High | Low |
| Obstacles | Walls | None | None |

## 📄 License

Free to use for educational and hackathon purposes.

---

**Save lives!** 🚨🤖 Good luck with your hackathon!
