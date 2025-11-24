const GRID_SIZE = 15;
let grid = [];
let agents = [];
let paths = [];
let isRunning = false;
let intervalId = null;
let steps = 0;
let speed = 5;

const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');
const resetBtn = document.getElementById('resetBtn');
const speedSlider = document.getElementById('speedSlider');
const gridElement = document.getElementById('grid');

function initGrid() {
    grid = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(0));
    
    // Add obstacles
    for (let i = 0; i < 30; i++) {
        const x = Math.floor(Math.random() * GRID_SIZE);
        const y = Math.floor(Math.random() * GRID_SIZE);
        grid[y][x] = 1; // 1 = obstacle
    }
    
    agents = [
        { id: 1, x: 1, y: 1, targetX: 13, targetY: 13, color: 'agent1', pathIndex: 0 },
        { id: 2, x: 13, y: 1, targetX: 1, targetY: 13, color: 'agent2', pathIndex: 0 },
        { id: 3, x: 1, y: 13, targetX: 13, targetY: 1, color: 'agent3', pathIndex: 0 },
        { id: 4, x: 13, y: 13, targetX: 1, targetY: 1, color: 'agent4', pathIndex: 0 }
    ];
    
    // Clear agent positions
    agents.forEach(a => grid[a.y][a.x] = 0);
    agents.forEach(a => grid[a.targetY][a.targetX] = 0);
    
    // Calculate paths
    paths = agents.map(agent => aStar(agent.x, agent.y, agent.targetX, agent.targetY));
    
    steps = 0;
    renderGrid();
    updateStats();
}

function aStar(startX, startY, goalX, goalY) {
    const openSet = [{ x: startX, y: startY, g: 0, h: heuristic(startX, startY, goalX, goalY), parent: null }];
    const closedSet = new Set();
    
    while (openSet.length > 0) {
        openSet.sort((a, b) => (a.g + a.h) - (b.g + b.h));
        const current = openSet.shift();
        
        if (current.x === goalX && current.y === goalY) {
            return reconstructPath(current);
        }
        
        closedSet.add(`${current.x},${current.y}`);
        
        const neighbors = [
            { x: current.x + 1, y: current.y },
            { x: current.x - 1, y: current.y },
            { x: current.x, y: current.y + 1 },
            { x: current.x, y: current.y - 1 }
        ];
        
        for (const neighbor of neighbors) {
            if (neighbor.x < 0 || neighbor.x >= GRID_SIZE || neighbor.y < 0 || neighbor.y >= GRID_SIZE) continue;
            if (grid[neighbor.y][neighbor.x] === 1) continue;
            if (closedSet.has(`${neighbor.x},${neighbor.y}`)) continue;
            
            const g = current.g + 1;
            const h = heuristic(neighbor.x, neighbor.y, goalX, goalY);
            const existing = openSet.find(n => n.x === neighbor.x && n.y === neighbor.y);
            
            if (!existing) {
                openSet.push({ x: neighbor.x, y: neighbor.y, g, h, parent: current });
            } else if (g < existing.g) {
                existing.g = g;
                existing.parent = current;
            }
        }
    }
    
    return [];
}

function heuristic(x1, y1, x2, y2) {
    return Math.abs(x1 - x2) + Math.abs(y1 - y2);
}

function reconstructPath(node) {
    const path = [];
    while (node) {
        path.unshift({ x: node.x, y: node.y });
        node = node.parent;
    }
    return path;
}

function renderGrid() {
    gridElement.innerHTML = '';
    for (let y = 0; y < GRID_SIZE; y++) {
        for (let x = 0; x < GRID_SIZE; x++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            
            const agent = agents.find(a => a.x === x && a.y === y);
            const isTarget = agents.some(a => a.targetX === x && a.targetY === y);
            const isPath = paths.some(path => path.some(p => p.x === x && p.y === y));
            
            if (agent) {
                cell.classList.add(agent.color);
            } else if (isTarget) {
                cell.classList.add('target');
            } else if (grid[y][x] === 1) {
                cell.classList.add('obstacle');
            } else if (isPath) {
                cell.classList.add('path');
            } else {
                cell.classList.add('empty');
            }
            
            gridElement.appendChild(cell);
        }
    }
}

function moveAgents() {
    let allReached = true;
    
    agents.forEach((agent, i) => {
        if (agent.pathIndex < paths[i].length - 1) {
            agent.pathIndex++;
            const nextPos = paths[i][agent.pathIndex];
            agent.x = nextPos.x;
            agent.y = nextPos.y;
            allReached = false;
        }
    });
    
    steps++;
    renderGrid();
    updateStats();
    
    if (allReached) {
        stop();
        document.getElementById('status').textContent = 'Complete!';
        alert(`All agents reached their targets in ${steps} steps!`);
    }
}

function updateStats() {
    document.getElementById('steps').textContent = steps;
    const progress = Math.min((steps / 50) * 100, 100);
    document.getElementById('progressBar').style.width = progress + '%';
    document.getElementById('progressText').textContent = Math.round(progress) + '%';
}

function start() {
    if (!isRunning) {
        isRunning = true;
        startBtn.disabled = true;
        pauseBtn.disabled = false;
        document.getElementById('status').textContent = 'Running';
        const delay = 1000 / speed;
        intervalId = setInterval(moveAgents, delay);
    }
}

function pause() {
    isRunning = false;
    startBtn.disabled = false;
    pauseBtn.disabled = true;
    document.getElementById('status').textContent = 'Paused';
    clearInterval(intervalId);
}

function stop() {
    pause();
}

function reset() {
    stop();
    initGrid();
    startBtn.disabled = false;
    pauseBtn.disabled = true;
    document.getElementById('status').textContent = 'Ready';
}

startBtn.addEventListener('click', start);
pauseBtn.addEventListener('click', pause);
resetBtn.addEventListener('click', reset);
speedSlider.addEventListener('input', (e) => {
    speed = parseInt(e.target.value);
    if (isRunning) {
        pause();
        start();
    }
});

initGrid();
