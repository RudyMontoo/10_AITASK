# Dual Drone Delivery Simulation

## 📋 Overview
A multi-agent delivery system where two drones cooperatively deliver packages to different locations. The system uses A* pathfinding for navigation and greedy algorithm for package assignment to minimize delivery time and path overlap.

## 🎯 Problem Statement
Design two delivery drones that:
- Deliver packages to different locations efficiently
- Use A* search for optimal pathfinding
- Assign packages using greedy algorithm
- Minimize total delivery time
- Minimize path overlap between drones

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
python drone_delivery.py
```

### Step 3: Watch the Visualization
- Left panel shows the grid with:
  - **Yellow squares** = Package pickup locations (P1, P2, etc.)
  - **Green circles** = Package delivery locations (D1, D2, etc.)
  - **Blue triangle** = Drone 1
  - **Red triangle** = Drone 2
  - **Brown box** = Drone carrying package
- Right panel shows:
  - **Heatmap** = Coverage frequency (darker = more visits)

## 🧠 How It Works

### 1. Environment Setup
- Creates a 14x14 grid
- Generates 8 random packages with pickup/delivery locations
- Initializes 2 drones at opposite corners

### 2. Greedy Package Assignment
- Each drone alternately picks nearest unassigned package
- Distance calculated using Manhattan distance to pickup location
- Ensures balanced workload distribution
- Simple but effective for small package counts

### 3. A* Pathfinding
- Drones use A* to find shortest path to pickup/delivery
- Manhattan distance heuristic
- Optimal path guaranteed
- Efficient navigation

### 4. Delivery Process
1. Drone navigates to pickup location
2. Picks up package
3. Navigates to delivery location
4. Delivers package
5. Moves to next assigned package

### 5. Coverage Tracking
- Every cell visited is tracked
- Heatmap shows visit frequency
- Identifies high-traffic areas
- Measures path overlap

## 📊 Output Example

```
Starting Dual Drone Delivery Simulation...
==================================================
Total packages: 8
Drone 1 assigned: 4 packages
Drone 2 assigned: 4 packages

Step 12: Drone 1 picked up package 3
Step 18: Drone 1 delivered package 3
Step 25: Drone 2 picked up package 5
Step 32: Drone 2 delivered package 5
...

==================================================
RESULTS:
  Total Time: 156 steps
  Packages Delivered: 8/8
  Drone 1: 4 packages
  Drone 2: 4 packages
  Coverage Overlap: 23 cells visited multiple times
  Efficiency: 5.13 packages/100 steps
==================================================
```

### Visual Output
- **Grid view**: Real-time package pickup/delivery
- **Heatmap**: Shows which areas are most traveled
- **Coverage analysis**: Identifies overlap zones

## 🎨 Customization

### Change Grid Size
```python
GRID_SIZE = 20  # Line 186
```

### Change Number of Packages
```python
NUM_PACKAGES = 12  # Line 187
```

### Adjust Visualization Speed
```python
if steps % 5 == 0:  # Update every 5 steps (Line 254)
    # Change to steps % 1 for real-time
```

### Use Hungarian Algorithm
Replace greedy assignment (Line 113) with Hungarian algorithm for optimal assignment:
```python
from scipy.optimize import linear_sum_assignment
# Implement cost matrix and optimal assignment
```

## 🏆 Hackathon Features

### What's Implemented
✅ A* pathfinding for optimal routes  
✅ Greedy package assignment  
✅ Pickup and delivery mechanics  
✅ Coverage heatmap visualization  
✅ Path overlap tracking  
✅ Real-time delivery status  
✅ Efficiency metrics  
✅ Single-file implementation (280 lines)

### Possible Extensions
- Implement Hungarian algorithm for optimal assignment
- Add package priorities (urgent deliveries)
- Implement battery/fuel constraints
- Add no-fly zones (obstacles)
- Create package weight limits
- Add time windows (deliver by certain time)
- Implement 3+ drones
- Add dynamic package requests (new packages during delivery)
- Create multi-depot scenarios
- Implement collision avoidance in air
- Add weather effects (wind, rain)
- Create 3D delivery (different altitudes)

## 📁 Project Structure

```
task6_drone_delivery/
├── drone_delivery.py    # Main simulation file
├── README.md            # This file
└── requirements.txt     # Python dependencies
```

## 🐛 Troubleshooting

**Issue: Unbalanced assignments**
- Greedy algorithm may not be perfectly balanced
- Try Hungarian algorithm for optimal assignment
- Adjust starting positions

**Issue: High path overlap**
- This is expected with greedy assignment
- Implement better assignment strategies
- Add path coordination logic

**Issue: Drones stuck**
- Check A* pathfinding
- Verify no unreachable locations

**Issue: Slow performance**
- Increase visualization update interval (line 254)
- Reduce grid size or package count

## 📝 Algorithm Details

### A* Pathfinding
- **Heuristic**: Manhattan distance (|x1-x2| + |y1-y2|)
- **Cost**: Number of steps
- **Optimality**: Guaranteed shortest path
- **Efficiency**: O(b^d) where b=branching factor, d=depth

### Greedy Assignment
- **Strategy**: Each drone picks nearest package alternately
- **Complexity**: O(n²) where n=number of packages
- **Advantage**: Simple, fast, good for small problems
- **Disadvantage**: Not optimal, may cause imbalance

### Hungarian Algorithm (Extension)
- **Strategy**: Optimal assignment minimizing total cost
- **Complexity**: O(n³)
- **Advantage**: Guaranteed optimal assignment
- **Disadvantage**: More complex, slower

## 🎓 Learning Outcomes

This project demonstrates:
- A* pathfinding algorithm
- Greedy vs optimal assignment strategies
- Multi-agent coordination
- Coverage analysis
- Heatmap visualization
- Delivery logistics optimization

## 📊 Performance Metrics

### Delivery Time
- **Metric**: Total steps to deliver all packages
- **Goal**: Minimize total time
- **Factors**: Assignment strategy, path efficiency

### Efficiency
- **Formula**: (Packages delivered / Total steps) × 100
- **Goal**: Maximize packages per step
- **Optimal**: Depends on package distribution

### Coverage Overlap
- **Metric**: Cells visited by multiple drones
- **Goal**: Minimize overlap
- **Indicates**: Path coordination quality

### Balance
- **Metric**: Packages per drone
- **Goal**: Equal distribution
- **Ideal**: 50% / 50% for 2 drones

## 🚁 Delivery Strategies

### Greedy (Implemented)
- Fast assignment
- Good for small problems
- May not be optimal

### Hungarian (Extension)
- Optimal assignment
- Better for larger problems
- More computational cost

### Auction-Based (Extension)
- Distributed decision making
- Good for dynamic scenarios
- Requires communication

### Cluster-Based (Extension)
- Group nearby packages
- Assign clusters to drones
- Reduces travel distance

## 🔄 Comparison with Other Tasks

| Feature | Drone Delivery | Resource Collection | Cleaning |
|---------|----------------|---------------------|----------|
| Algorithm | A* | A* | A* |
| Assignment | Greedy | Distributed | Proximity |
| Task | Pickup + Delivery | Collection | Cleaning |
| Metric | Delivery time | Collection rate | Coverage |
| Complexity | High (2 steps) | Medium | Low |

## 📄 License

Free to use for educational and hackathon purposes.

---

**Deliver with speed!** 🚁📦 Good luck with your hackathon!
