# Grid Painting Agents Simulation

## 📋 Overview
A multi-agent cooperative system where two painting robots work together to paint all cells in a grid without overlapping. Each robot paints cells in its assigned region using DFS (Depth-First Search) traversal for efficient coverage.

## 🎯 Problem Statement
Design two painting robots that:
- Paint all cells in a grid without overlapping
- Use DFS or rule-based task allocation
- Coordinate to avoid painting same cells
- Minimize total painting time
- Create distinct color patterns for each robot

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
python painting_simulation.py
```

### Step 3: Watch the Visualization
- Left panel shows the grid with:
  - **Blue cells** = Painted by Robot 1
  - **Red cells** = Painted by Robot 2
  - **White cells** = Unpainted
  - **Blue circle** = Robot 1 position
  - **Red circle** = Robot 2 position
- Right panel shows a pie chart:
  - Coverage percentage by each robot

## 🧠 How It Works

### 1. Environment Setup
- Creates a 12x12 grid (144 cells)
- Divides grid into two regions (left/right)
- Initializes 2 painting robots at region boundaries

### 2. Region Allocation (Rule-Based)
- **Robot 1**: Left half of grid (vertical split)
- **Robot 2**: Right half of grid
- No overlap between regions
- Balanced workload

### 3. DFS Painting Strategy
- Each robot uses DFS to traverse its region
- Paints current cell before moving
- Explores unvisited neighbors systematically
- Ensures complete coverage with no gaps

### 4. Path Planning
- DFS naturally creates efficient painting paths
- Robots follow depth-first traversal pattern
- Minimizes backtracking
- Creates distinctive painting patterns

### 5. Coordination
- Strict region boundaries prevent overlap
- No collision possible (separate regions)
- Independent operation (no communication needed)
- Parallel painting for efficiency

## 📊 Output Example

```
Starting Grid Painting Simulation...
==================================================
Grid size: 12x12 (144 cells)
Robot 1 region: 72 cells
Robot 2 region: 72 cells

Step 10: Robot 1 painted 10 cells
Step 10: Robot 2 painted 10 cells
Step 50: Robot 1 painted 50 cells
Step 50: Robot 2 painted 50 cells

==================================================
RESULTS:
  Total Time: 72 steps
  Total Cells: 144
  Robot 1: 72 cells (50.0%)
  Robot 2: 72 cells (50.0%)
  Coverage: 100.0%
  Efficiency: 200.00 cells/100 steps
  No Overlaps: ✓
==================================================
```

### Visual Output
The simulation shows:
- **Color-coded grid**: Blue and red regions clearly separated
- **Pie chart**: 50/50 split showing balanced workload
- **DFS patterns**: Visible depth-first traversal paths

## 🎨 Customization

### Change Grid Size
```python
GRID_SIZE = 16  # Line 138
```

### Change Region Division
Modify `allocate_regions()` (Line 60) to:
- Horizontal split (top/bottom)
- Quadrant division (for 4 robots)
- Checkerboard pattern
- Spiral patterns

### Adjust Visualization Speed
```python
if steps % 3 == 0:  # Update every 3 steps (Line 177)
    # Change to steps % 1 for real-time
```

### Change Colors
```python
colors = ['blue', 'red', 'green', 'orange']  # Line 95
```

## 🏆 Hackathon Features

### What's Implemented
✅ DFS traversal for painting  
✅ Rule-based region allocation  
✅ Zero overlap guarantee  
✅ Color-coded visualization  
✅ Pie chart showing coverage  
✅ Efficiency metrics  
✅ Pattern visualization  
✅ Single-file implementation (220 lines)

### Possible Extensions
- Add obstacles that can't be painted
- Implement different painting patterns (spiral, zigzag)
- Add paint capacity (limited paint, need refills)
- Create artistic patterns (gradients, designs)
- Add 3+ painting robots
- Implement dynamic region reallocation
- Add painting quality/layers (multiple coats)
- Create competitive mode (paint more area)
- Add time-based paint drying
- Implement different traversal algorithms (BFS, spiral)

## 📁 Project Structure

```
task7_grid_painting/
├── painting_simulation.py    # Main simulation file
├── README.md                  # This file
└── requirements.txt           # Python dependencies
```

## 🐛 Troubleshooting

**Issue: Robots painting same cells**
- This shouldn't happen with strict region boundaries
- Check region allocation logic

**Issue: Incomplete coverage**
- Verify DFS implementation
- Check if all cells are reachable

**Issue: Slow performance**
- Increase visualization update interval (line 177)
- Reduce grid size

**Issue: Colors not showing**
- Check matplotlib installation
- Verify color mapping in visualization

## 📝 Algorithm Details

### DFS (Depth-First Search)
- **Strategy**: Explore as far as possible before backtracking
- **Stack**: Implicit (recursion) or explicit
- **Visited**: Track painted cells
- **Pattern**: Creates distinctive "snake-like" paths
- **Efficiency**: O(n) where n is number of cells

### Rule-Based Allocation
- **Strategy**: Divide grid into equal regions
- **Method**: Vertical split for 2 robots
- **Guarantee**: No overlap by design
- **Balance**: Approximately equal cells per robot
- **Scalability**: Easy to extend to more robots

### Painting Mechanics
1. Robot starts at region boundary
2. Paint current cell
3. Find unpainted neighbor in region
4. Move to neighbor
5. Repeat until all cells painted
6. DFS ensures complete coverage

## 🎓 Learning Outcomes

This project demonstrates:
- Depth-First Search algorithm
- Rule-based task allocation
- Spatial partitioning strategies
- Collision-free coordination
- Coverage path planning
- Visual pattern generation

## 🎨 Painting Patterns

### DFS Pattern
- Creates "maze-like" paths
- Explores deeply before backtracking
- Distinctive visual appearance
- Efficient coverage

### Alternative Patterns (Extensions)
- **BFS**: Layer-by-layer expansion
- **Spiral**: Circular inward/outward
- **Zigzag**: Row-by-row scanning
- **Random**: Unpredictable coverage
- **Checkerboard**: Alternating cells

## 📊 Performance Metrics

### Coverage
- **Formula**: (Painted cells / Total cells) × 100
- **Goal**: 100% coverage
- **Guarantee**: DFS ensures complete coverage

### Efficiency
- **Formula**: (Total cells / Total steps) × 100
- **Goal**: Maximize cells per step
- **Optimal**: Approaches 200 cells/100 steps for 2 robots

### Balance
- **Formula**: Cells per robot / Total cells
- **Goal**: 50% / 50% for 2 robots
- **Achieved**: Perfect balance with equal regions

### Overlap
- **Metric**: Number of cells painted by multiple robots
- **Goal**: Zero overlaps
- **Guarantee**: Strict region boundaries ensure no overlap

## 🔄 Comparison with Other Tasks

| Feature | Painting | Cleaning | Exploration |
|---------|----------|----------|-------------|
| Algorithm | DFS | A* | BFS |
| Allocation | Region-based | Proximity | Region-based |
| Overlap | None (by design) | Avoided | Avoided |
| Pattern | Depth-first | Goal-directed | Breadth-first |
| Coordination | Independent | Dynamic | Dynamic |

## 📄 License

Free to use for educational and hackathon purposes.

---

**Paint the grid!** 🎨 Good luck with your hackathon!
