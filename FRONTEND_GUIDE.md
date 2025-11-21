# 🌐 Web Frontend Guide

## Overview

All 9 tasks now have beautiful, interactive web frontends! No Python installation needed to run the simulations in your browser.

## 🎯 Quick Start

### Method 1: Dashboard (Recommended)
```bash
# Open the main dashboard
start frontend/index.html
```

Click any task card to launch that simulation!

### Method 2: Direct Task Access
```bash
# Open any task directly
start task2_cleaning_simulation/index.html
start task3_path_planners/index.html
start task4_warehouse_pickup/index.html
start task5_rescue_bots/index.html
start task6_drone_delivery/index.html
start task7_grid_painting/index.html
start task8_resource_collection/index.html
start task9_firefighters/index.html
start task10_map_exploration/index.html
```

## 📋 Available Frontends

### ✅ Task 2: Cleaning Simulation
- **Grid:** 20x20
- **Agents:** 4 cleaning robots
- **Features:** Real-time cleaning progress, percentage tracker
- **Colors:** Red, Teal, Yellow, Green agents

### ✅ Task 3: Path Planning (A*)
- **Grid:** 15x15
- **Agents:** 4 path planners
- **Features:** Obstacle avoidance, path visualization
- **Algorithm:** A* pathfinding with collision avoidance

### ✅ Task 4: Warehouse Pickup
- **Grid:** 20x20
- **Agents:** 4 warehouse robots
- **Features:** Package collection, depot delivery
- **Tracking:** Collected packages counter

### ✅ Task 5: Rescue Bots
- **Grid:** 18x18
- **Agents:** 4 rescue bots
- **Features:** Victim rescue, base return, obstacles
- **Animation:** Pulsing victims, glowing agents

### ✅ Task 6: Drone Delivery
- **Grid:** 16x16
- **Agents:** 3 delivery drones
- **Features:** Hub-based delivery, flying animation
- **Special:** Drones have floating animation effect

### ✅ Task 7: Grid Painting
- **Grid:** 20x20
- **Agents:** 4 painting robots
- **Features:** DFS painting, obstacle navigation
- **Tracking:** Percentage painted

### ✅ Task 8: Resource Collection
- **Grid:** 20x20
- **Agents:** 4 collector agents
- **Features:** Sparkling resources, greedy collection
- **Animation:** Resources sparkle and pulse

### ✅ Task 9: Firefighters
- **Grid:** 18x18
- **Agents:** 4 firefighters
- **Features:** Fire spreading, extinguishing animation
- **Dynamic:** Fires spread to neighbors randomly

### ✅ Task 10: Map Exploration
- **Grid:** 20x20
- **Agents:** 4 explorers
- **Features:** BFS exploration, fog of war effect
- **Tracking:** Exploration percentage

## 🎮 Controls

All frontends have the same controls:

- **Start Button** - Begin the simulation
- **Pause Button** - Pause the simulation
- **Reset Button** - Reset to initial state
- **Speed Slider** - Adjust simulation speed (1-10)

## 🎨 Features

### Visual Design
- **Gradient Backgrounds** - Each task has unique gradient
- **Smooth Animations** - CSS transitions for all elements
- **Color-Coded Agents** - Easy to distinguish agents
- **Responsive Grid** - Adapts to different screen sizes
- **Legend** - Shows what each color represents

### Interactive Elements
- **Real-time Stats** - Steps, progress, status
- **Info Panel** - Key metrics at a glance
- **Control Panel** - Easy-to-use buttons
- **Speed Control** - Adjust simulation speed on the fly

### Animations
- **Pulsing Effects** - For victims, fires, resources
- **Glowing Shadows** - For agents and special cells
- **Smooth Transitions** - For all state changes
- **Flying Effect** - For drones (Task 6)
- **Burning Effect** - For fires (Task 9)
- **Sparkle Effect** - For resources (Task 8)

## 🔧 Technical Details

### Technologies Used
- **HTML5** - Structure
- **CSS3** - Styling and animations
- **Vanilla JavaScript** - Logic and interactivity
- **No Dependencies** - Pure frontend, no libraries needed

### File Structure
Each task has 3 files:
```
taskX_name/
├── index.html  # Structure and layout
├── style.css   # Styling and animations
└── script.js   # Simulation logic
```

### Grid Rendering
- Uses CSS Grid for layout
- Each cell is a div with dynamic classes
- Real-time updates via JavaScript
- Efficient rendering (no canvas needed)

## 🚀 Advanced: With Backend

For advanced features, you can run with the FastAPI backend:

### 1. Install Backend
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Backend
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Open Frontend
```bash
start frontend/index.html
```

### Backend Features
- **WebSocket Support** - Real-time updates
- **REST API** - Task information endpoints
- **CORS Enabled** - Cross-origin requests
- **Python Integration** - Connect to Python simulations

## 📱 Browser Compatibility

Tested and working on:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

## 🎯 Use Cases

### For Presentations
1. Open dashboard
2. Click task to demo
3. Adjust speed for audience
4. Reset and try different scenarios

### For Development
1. Open specific task
2. Modify parameters in script.js
3. Refresh browser to see changes
4. No compilation needed!

### For Teaching
1. Show students the dashboard
2. Explain each algorithm
3. Run simulations side-by-side
4. Compare different approaches

### For Hackathons
1. Quick demos without setup
2. Works on any computer with browser
3. No Python installation needed
4. Impressive visual presentation

## 🎨 Customization

### Change Grid Size
Edit in `script.js`:
```javascript
const GRID_SIZE = 25; // Change from 20 to 25
```

### Change Agent Count
Edit in `script.js`:
```javascript
agents = [
    { id: 1, x: 0, y: 0, color: 'agent1' },
    { id: 2, x: 19, y: 0, color: 'agent2' },
    { id: 3, x: 0, y: 19, color: 'agent3' },
    { id: 4, x: 19, y: 19, color: 'agent4' },
    { id: 5, x: 10, y: 10, color: 'agent5' } // Add new agent
];
```

### Change Colors
Edit in `style.css`:
```css
.agent1 {
    background: #your-color;
}
```

### Change Speed Range
Edit in `index.html`:
```html
<input type="range" id="speedSlider" min="1" max="20" value="5">
```

## 🐛 Troubleshooting

### Simulation Not Starting
- Check browser console for errors (F12)
- Ensure JavaScript is enabled
- Try refreshing the page

### Agents Not Moving
- Click the Start button
- Check if speed slider is at 0
- Reset and try again

### Grid Not Displaying
- Check if CSS file is loaded
- Verify file paths are correct
- Try a different browser

### Performance Issues
- Reduce grid size
- Lower agent count
- Decrease speed slider
- Close other browser tabs

## 📊 Performance

### Recommended Settings
- **Grid Size:** 15-20 for smooth performance
- **Agents:** 2-4 for best visualization
- **Speed:** 3-7 for comfortable viewing
- **Browser:** Chrome for best performance

### Optimization Tips
- Use smaller grids for more agents
- Lower speed for complex scenarios
- Close unused browser tabs
- Use modern browsers

## 🎓 Learning Resources

### Understanding the Code
1. Start with `index.html` - See structure
2. Check `style.css` - Learn styling
3. Read `script.js` - Understand logic

### Modifying Simulations
1. Change constants (GRID_SIZE, etc.)
2. Modify agent behavior
3. Add new features
4. Experiment with algorithms

### Creating New Tasks
1. Copy existing task folder
2. Modify grid and agents
3. Update algorithm logic
4. Customize colors and styles

## 🌟 Best Practices

### For Demos
- Start with dashboard overview
- Show 2-3 different tasks
- Explain algorithms briefly
- Let audience control speed

### For Development
- Test in multiple browsers
- Keep grid sizes reasonable
- Comment your code changes
- Use meaningful variable names

### For Teaching
- Start with simple tasks (Task 2, 3)
- Progress to complex (Task 9, 10)
- Show code alongside demo
- Encourage experimentation

## 📞 Support

For issues or questions:
1. Check this guide
2. Review SETUP_INSTRUCTIONS.md
3. Check browser console (F12)
4. Open GitHub issue

## 🎉 Enjoy!

You now have 9 fully interactive web frontends for all multi-agent simulations. No installation, no setup - just open and run!

**Happy Simulating! 🚀**
