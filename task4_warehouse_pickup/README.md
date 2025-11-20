# Warehouse Pickup Team Simulation

## 📋 Overview
A multi-agent warehouse logistics system where two agents cooperatively pick up items from various locations and deliver them to dropoff zones. The system uses proximity-based task assignment to minimize total travel distance and maximize efficiency.

## 🎯 Problem Statement
Design two warehouse agents that:
- Pick up items from scattered locations
- Deliver items to designated dropoff zones
- Assign tasks based on proximity
- Minimize total travel distance
- Maximize pickup/delivery efficiency

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
python warehouse_simulation.py
```

### Step 3: Watch the Visualization
- Left panel shows the warehouse with:
  - **Green squares** = Dropoff zones (labeled "DROP")
  - **Brown boxes** = Items to pickup (numbered)
  - **Blue square** = Agent 1
  - **Red square** = Agent 2
  - **Small brown box on agent** = Agent carrying item
- Right panel shows:
  - **Performance table** = Real-time metrics for each agent

## 🧠 How It Works

### 1. Environment Setup
- Creates a 12x12 warehouse grid
- Places 10 items randomly
- Designates 2 dropoff zones (corners)
- Initializes 2 agents at dropoff zones

### 2. Proximity-Based Assignment
- Each agent selects nearest available item
- Distance calculated using Manhattan distance
- Prevents multiple agents targeting same item
- Dynamic reassignment as items are completed

### 3. A* Pathfinding
- Agents use A* for optimal path to pickup/dropoff
- Manhattan distance heuristic
- Guaranteed shortest path
- Efficient navigation

### 4. Pickup & Delivery Process
1. Agent identifies nearest available item
2. Navigates to item location using A*
3. Picks up item
4. Navigates to nearest dropoff zone
5. Drops off item
6. Immediately selects next item

### 5. Efficiency Tracking
- Distance traveled by each agent
- Items completed per agent
- Efficiency ratio (items/distance)
- Total time to completion

## 📊 Output Example

```
Starting Warehouse Pickup Team Simulation...
==================================================
Warehouse size: 12x12
Items to pickup: 10
Dropoff zones: 2

Step 8: Agent 1 picked up item 3
Step 15: Agent 1 dropped off item 3
Step 22: Agent 2 picked up item 7
Step 28: Agent 2 dropped off item 7
...

==================================================
RESULTS:
  Total Time: 156 steps
  Items Completed: 10/10
  Agent 1: 5 items, 78 distance
  Agent 2: 5 items, 72 distance
  Total Distance: 150
  Overall Efficiency: 0.067 items/step
  Status: SUCCESS
==================================================
```

### Visual Output
- **Warehouse view**: Real-time pickup/delivery operations
- **Performance table**: Live metrics showing:
  - Items completed per agent
  - Distance traveled per agent
  - Efficiency ratio per agent
  - Total statistics

## 🎨 Customization

### Change Warehouse Size
```python
WAREHOUSE_SIZE = 15  # Line 149
```

### Change Number of Items
```python
NUM_ITEMS = 15  # Line 150
```

### Add More Dropoff Zones
```python
dropoff_zones = [(0, 0), (11, 11), (0, 11), (11, 0)]  # Line 156
```

### Visualization Speed
```python
if steps % 5 == 0:  # Update every 5 steps (Line 221)
    # Change to steps % 1 for real-time
```

## 🏆 Hackathon Features

### What's Implemented
✅ A* pathfinding for optimal routes  
✅ Proximity-based task assignment  
✅ Pickup and delivery mechanics  
✅ Real-time performance table  
✅ Distance tracking  
✅ Efficiency metrics  
✅ Conflict avoidance (no duplicate assignments)  
✅ Single-file implementation (260 lines)

### Possible Extensions
- Add item weights (capacity constraints)
- Implement priority items (urgent deliveries)
- Add obstacles/shelves in warehouse
- Create multi-floor warehouse (3D)
- Implement battery/energy management
- Add item categories (fragile, heavy, etc.)
- Create time windows for deliveries
- Implement 3+ warehouse agents
- Add dynamic item arrivals
- Create optimal assignment algorithm (Hungarian)
- Add collision avoidance between agents
- Implement conveyor belts
- Add packing stations

## 📁 Project Structure

```
task4_warehouse_pickup/
├── warehouse_simulation.py    # Main simulation file
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

## 🐛 Troubleshooting

**Issue: Agents target same item**
- Conflict avoidance logic prevents this
- Check assignment function (line 183)

**Issue: Inefficient routing**
- A* guarantees shortest path
- May need better assignment strategy
- Try Hungarian algorithm for optimal assignment

**Issue: Agents stuck**
- Check A* pathfinding
- Verify no unreachable locations

**Issue: Slow performance**
- Increase visualization update interval (line 221)
- Reduce warehouse size or item count

## 📝 Algorithm Details

### A* Pathfinding
- **Heuristic**: Manhattan distance
- **Cost**: Number of steps
- **Optimality**: Guaranteed shortest path
- **Complexity**: O(b^d) where b=branching, d=depth

### Proximity-Based Assignment
- **Strategy**: Each agent picks nearest item
- **Distance**: Manhattan distance to pickup location
- **Conflict**: Prevents duplicate assignments
- **Dynamic**: Reassigns after each completion
- **Complexity**: O(n) where n=number of items

### Efficiency Calculation
- **Formula**: Items completed / Distance traveled
- **Goal**: Maximize efficiency ratio
- **Factors**: Assignment strategy, warehouse layout

## 🎓 Learning Outcomes

This project demonstrates:
- Warehouse logistics optimization
- Proximity-based task allocation
- A* pathfinding algorithm
- Multi-agent coordination
- Efficiency metrics tracking
- Real-time performance monitoring

## 📊 Performance Metrics

### Total Time
- **Metric**: Steps to complete all pickups
- **Goal**: Minimize total time
- **Factors**: Assignment, pathfinding, coordination

### Distance Traveled
- **Metric**: Total steps taken by all agents
- **Goal**: Minimize total distance
- **Optimal**: Depends on item distribution

### Efficiency
- **Formula**: Items / Distance
- **Goal**: Maximize items per step
- **Benchmark**: >0.05 is good, >0.10 is excellent

### Balance
- **Metric**: Items per agent
- **Goal**: Equal distribution
- **Ideal**: 50% / 50% for 2 agents

## 📦 Warehouse Scenarios

### Small Warehouse
- 10x10 grid
- 5 items
- 2 dropoff zones
- Quick completion

### Medium Warehouse (Default)
- 12x12 grid
- 10 items
- 2 dropoff zones
- Balanced challenge

### Large Warehouse
- 15x15 grid
- 15 items
- 4 dropoff zones
- Complex logistics

### Mega Warehouse
- 20x20 grid
- 25 items
- 4 dropoff zones
- Add obstacles
- 3+ agents

## 🔄 Comparison with Other Tasks

| Feature | Warehouse | Drone Delivery | Resource Collection |
|---------|-----------|----------------|---------------------|
| Algorithm | A* | A* | A* |
| Assignment | Proximity | Greedy | Distributed |
| Task | Pickup + Drop | Pickup + Deliver | Collection only |
| Zones | Dropoff zones | Delivery locations | None |
| Metric | Efficiency | Delivery time | Collection rate |

## 💡 Optimization Strategies

### Current (Proximity-Based)
- Simple and fast
- Good for dynamic scenarios
- May not be globally optimal

### Hungarian Algorithm
- Optimal assignment
- Minimizes total distance
- Better for static scenarios

### Auction-Based
- Distributed decision making
- Good for large teams
- Requires communication

### Cluster-Based
- Group nearby items
- Assign clusters to agents
- Reduces travel distance

## 📄 License

Free to use for educational and hackathon purposes.

---

**Optimize your warehouse!** 📦🤖 Good luck with your hackathon!
