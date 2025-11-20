# Cleaning Crew Coordination Simulation

## 📋 Overview
A multi-agent cooperative system where two cleaning bots work together to clean a dirty grid environment efficiently. The bots use A* pathfinding and coordinate to avoid collisions while maximizing cleaning efficiency.

## 🎯 Problem Statement
Design two cleaning bots that:
- Divide cleaning tasks intelligently based on proximity
- Plan non-overlapping paths using A* algorithm
- Avoid collisions with each other
- Clean all dirty cells efficiently

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
python cleaning_simulation.py
```

### Step 3: Watch the Visualization
- A window will open showing the grid
- **Brown cells** = Dirty (need cleaning)
- **Green cells** = Cleaned
- **Blue circle** = Bot 1
- **Red circle** = Bot 2
- Watch as both bots coordinate to clean all cells

## 🧠 How It Works

### 1. Environment Setup
- Creates a 10x10 grid
- Randomly places 20 dirty cells
- Initializes 2 bots at opposite corners

### 2. Task Division
- Calculates Manhattan distance from each bot to each dirty cell
- Assigns each cell to the closest bot
- Ensures balanced workload

### 3. Path Planning (A* Algorithm)
- Each bot finds the shortest path to its next target
- Avoids the other bot's current position
- Uses Manhattan distance as heuristic

### 4. Coordination
- Bots move step-by-step
- Clean cells when they reach them
- Replan paths dynamically
- Avoid collisions

### 5. Metrics
- Total steps taken
- Cells cleaned by each bot
- Overall efficiency score

## 📊 Output Example

```
Starting Cleaning Crew Simulation...
==================================================
Bot 1: 11 tasks | Bot 2: 9 tasks

==================================================
RESULTS:
  Total Steps: 32
  Cells Cleaned: 20/20
  Bot 1: 11 cells
  Bot 2: 9 cells
  Efficiency: 100.0%
==================================================
```

## 🎨 Customization

### Change Grid Size
```python
GRID_SIZE = 15  # Line 165
```

### Change Number of Dirty Cells
```python
NUM_DIRTY = 30  # Line 166
```

### Adjust Visualization Speed
```python
if steps % 5 == 0:  # Update every 5 steps (Line 223)
    # Change to steps % 1 for real-time
```

## 🏆 Hackathon Features

### What's Implemented
✅ A* pathfinding algorithm  
✅ Proximity-based task allocation  
✅ Collision avoidance  
✅ Real-time visualization  
✅ Efficiency metrics  
✅ Single-file implementation (250 lines)

### Possible Extensions
- Add obstacles/walls to the grid
- Implement battery management (recharge stations)
- Add 3+ bots for larger grids
- Dynamic task reallocation
- Communication protocol between bots
- Priority zones (some areas need cleaning first)

## 📁 Project Structure

```
.
├── cleaning_simulation.py    # Main simulation file (all-in-one)
├── README.md                  # This file
└── requirements.txt           # Python dependencies
```

## 🐛 Troubleshooting

**Issue: No visualization window appears**
- Make sure matplotlib is installed: `pip install matplotlib`
- Try running with: `python -i cleaning_simulation.py`

**Issue: Bots get stuck**
- This shouldn't happen with A*, but if it does, restart the simulation
- The random dirty cell placement might create edge cases

**Issue: Import errors**
- Ensure you're running from the project directory
- Check Python version: `python --version`

## 📝 Algorithm Details

### A* Pathfinding
- **Heuristic**: Manhattan distance (|x1-x2| + |y1-y2|)
- **Cost**: Number of steps taken
- **Priority**: cost + heuristic
- **Collision Avoidance**: Excludes other bot's position from valid moves

### Task Allocation
- **Strategy**: Greedy proximity-based assignment
- **Metric**: Manhattan distance to each dirty cell
- **Result**: Balanced workload between bots

## 🎓 Learning Outcomes

This project demonstrates:
- Multi-agent coordination
- Pathfinding algorithms (A*)
- Task allocation strategies
- Real-time visualization
- Cooperative robotics concepts

## 📄 License

Free to use for educational and hackathon purposes.

---

**Ready for your hackathon!** 🚀 Good luck!
