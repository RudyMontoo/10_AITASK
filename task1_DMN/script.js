const GRID_WIDTH = 20;
const GRID_HEIGHT = 15;
let grid = [];
let agents = [];
let keys = [];
let isRunning = false;
let intervalId = null;
let steps = 0;
let speed = 5;
let keysCollected = 0;

const gridElement = document.getElementById('grid');

function initGrid() {
    grid = Array(GRID_HEIGHT).fill().map(() => Array(GRID_WIDTH).fill(0)); // 0 = path, 1 = wall, 2 = key
    
    // Add border walls
    for (let i = 0; i < GRID_HEIGHT; i++) {
        grid[i][0] = 1;
        grid[i][GRID_WIDTH - 1] = 1;
    }
    for (let j = 0; j < GRID_WIDTH; j++) {
        grid[0][j] = 1;
        grid[GRID_HEIGHT - 1][j] = 1;
    }
    
    // Add random internal walls
    for (let i = 0; i < (GRID_WIDTH * GRID_HEIGHT) / 6; i++) {
        const x = Math.floor(Math.random() * (GRID_HEIGHT - 2)) + 1;
        const y = Math.floor(Math.random() * (GRID_WIDTH - 2)) + 1;
        grid[x][y] = 1;
    }
    
    // Place keys
    keys = [];
    for (let i = 0; i < 8; i++) {
        let x, y;
        do {
            x = Math.floor(Math.random() * (GRID_HEIGHT - 2)) + 1;
            y = Math.floor(Math.random() * (GRID_WIDTH - 2)) + 1;
        } while (grid[x][y] !== 0 || keys.some(k => k.x === x && k.y === y));
        keys.push({ x, y, collected: false });
        grid[x][y] = 2;
    }
    
    // Create agents at corners
    agents = [
        { id: 1, x: 1, y: 1, color: 'agent1', target: null, path: [], visited: new Set() },
        { id: 2, x: GRID_HEIGHT - 2, y: GRID_WIDTH - 2, color: 'agent2', target: null, path: [], visited: new Set() },
        { id: 3, x: 1, y: GRID_WIDTH - 2, color: 'agent3', target: null, path: [], visited: new Set() },
        { id: 4, x: GRID_HEIGHT - 2, y: 1, color: 'agent4', target: null, path: [], visited: new Set() }
    ];
    
    // Clear agent positions
    agents.forEach(a => {
        grid[a.x][a.y] = 0;
        a.visited.add(`${a.x},${a.y}`);
    });
    
    steps = 0;
    keysCollected = 0;
    renderGrid();
    updateStats();
}

function renderGrid() {
    gridElement.innerHTML = '';
    gridElement.style.gridTemplateColumns = `repeat(${GRID_WIDTH}, 28px)`;
    
    for (let x = 0; x < GRID_HEIGHT; x++) {
        for (let y = 0; y < GRID_WIDTH; y++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            
            const agent = agents.find(a => a.x === x && a.y === y);
            const key = keys.find(k => k.x === x && k.y === y && !k.collected);
            const isVisited = agents.some(a => a.visited.has(`${x},${y}`));
            
            if (agent) {
                cell.classList.add(agent.color);
            } else if (key) {
                cell.classList.add('key');
            } else if (grid[x][y] === 1) {
                cell.classList.add('wall');
            } else if (isVisited) {
                cell.classList.add('visited');
            } else {
                cell.classList.add('path');
            }
            
            gridElement.appendChild(cell);
        }
    }
}

function bfs(agent, targetKeys) {
    if (targetKeys.length === 0) return null;
    
    const queue = [[agent.x, agent.y, []]];
    const visited = new Set([`${agent.x},${agent.y}`]);
    
    while (queue.length > 0) {
        const [x, y, path] = queue.shift();
        
        // Check if we found a key
        const key = targetKeys.find(k => k.x === x && k.y === y && !k.collected);
        if (key) {
            return { key, path };
        }
        
        // Explore neighbors
        const neighbors = [
            [x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]
        ];
        
        for (const [nx, ny] of neighbors) {
            const key = `${nx},${ny}`;
            if (nx >= 0 && nx < GRID_HEIGHT && ny >= 0 && ny < GRID_WIDTH &&
                grid[nx][ny] !== 1 && !visited.has(key)) {
                visited.add(key);
                queue.push([nx, ny, [...path, [nx, ny]]]);
            }
        }
    }
    
    return null;
}

function moveAgents() {
    // Assign targets to agents without targets
    const availableKeys = keys.filter(k => !k.collected && !agents.some(a => a.target === k));
    
    agents.forEach(agent => {
        if (!agent.target && availableKeys.length > 0) {
            // Find nearest key
            let nearest = null;
            let minDist = Infinity;
            
            availableKeys.forEach(key => {
                const dist = Math.abs(agent.x - key.x) + Math.abs(agent.y - key.y);
                if (dist < minDist) {
                    minDist = dist;
                    nearest = key;
                }
            });
            
            if (nearest) {
                agent.target = nearest;
                const result = bfs(agent, [nearest]);
                if (result) {
                    agent.path = result.path;
                }
            }
        }
        
        // Move along path
        if (agent.path.length > 0) {
            const [nx, ny] = agent.path.shift();
            agent.x = nx;
            agent.y = ny;
            agent.visited.add(`${nx},${ny}`);
            
            // Check if reached target
            if (agent.target && agent.x === agent.target.x && agent.y === agent.target.y) {
                agent.target.collected = true;
                agent.target = null;
                keysCollected++;
            }
        }
    });
    
    steps++;
    renderGrid();
    updateStats();
    
    if (keysCollected === keys.length) {
        stop();
        document.getElementById('status').textContent = 'Complete!';
        alert(`All keys collected in ${steps} steps!`);
    }
}

function updateStats() {
    document.getElementById('steps').textContent = steps;
    document.getElementById('keys').textContent = `${keysCollected}/${keys.length}`;
}

function start() {
    if (!isRunning) {
        isRunning = true;
        document.getElementById('startBtn').disabled = true;
        document.getElementById('pauseBtn').disabled = false;
        document.getElementById('status').textContent = 'Navigating';
        intervalId = setInterval(moveAgents, 1000 / speed);
    }
}

function pause() {
    isRunning = false;
    document.getElementById('startBtn').disabled = false;
    document.getElementById('pauseBtn').disabled = true;
    document.getElementById('status').textContent = 'Paused';
    clearInterval(intervalId);
}

function stop() { pause(); }

function reset() {
    stop();
    initGrid();
    document.getElementById('status').textContent = 'Ready';
}

document.getElementById('startBtn').addEventListener('click', start);
document.getElementById('pauseBtn').addEventListener('click', pause);
document.getElementById('resetBtn').addEventListener('click', reset);
document.getElementById('speedSlider').addEventListener('input', (e) => {
    speed = parseInt(e.target.value);
    if (isRunning) { pause(); start(); }
});

initGrid();
