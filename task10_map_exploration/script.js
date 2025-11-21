const GRID_SIZE = 20;
let grid = [];
let explorers = [];
let isRunning = false;
let intervalId = null;
let steps = 0;
let speed = 5;

const gridElement = document.getElementById('grid');

function initGrid() {
    grid = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(0)); // 0 = unexplored, 1 = explored, 2 = obstacle
    
    // Add obstacles
    for (let i = 0; i < 50; i++) {
        const x = Math.floor(Math.random() * GRID_SIZE);
        const y = Math.floor(Math.random() * GRID_SIZE);
        grid[y][x] = 2;
    }
    
    explorers = [
        { id: 1, x: 1, y: 1, color: 'explorer1', queue: [] },
        { id: 2, x: 18, y: 1, color: 'explorer2', queue: [] },
        { id: 3, x: 1, y: 18, color: 'explorer3', queue: [] },
        { id: 4, x: 18, y: 18, color: 'explorer4', queue: [] }
    ];
    
    // Clear explorer positions
    explorers.forEach(e => grid[e.y][e.x] = 0);
    
    // Initialize BFS queues
    explorers.forEach(e => e.queue.push({ x: e.x, y: e.y }));
    
    steps = 0;
    renderGrid();
    updateStats();
}

function renderGrid() {
    gridElement.innerHTML = '';
    for (let y = 0; y < GRID_SIZE; y++) {
        for (let x = 0; x < GRID_SIZE; x++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            
            const explorer = explorers.find(e => e.x === x && e.y === y);
            
            if (explorer) {
                cell.classList.add(explorer.color);
            } else if (grid[y][x] === 2) {
                cell.classList.add('obstacle');
            } else if (grid[y][x] === 1) {
                cell.classList.add('explored');
            } else {
                cell.classList.add('unexplored');
            }
            
            gridElement.appendChild(cell);
        }
    }
}

function moveExplorers() {
    explorers.forEach(explorer => {
        // Mark current as explored
        if (grid[explorer.y][explorer.x] === 0) {
            grid[explorer.y][explorer.x] = 1;
        }
        
        // BFS: explore neighbors
        const neighbors = [
            { x: explorer.x, y: explorer.y - 1 },
            { x: explorer.x + 1, y: explorer.y },
            { x: explorer.x, y: explorer.y + 1 },
            { x: explorer.x - 1, y: explorer.y }
        ];
        
        for (const n of neighbors) {
            if (n.x >= 0 && n.x < GRID_SIZE && n.y >= 0 && n.y < GRID_SIZE) {
                if (grid[n.y][n.x] === 0 && !explorer.queue.some(q => q.x === n.x && q.y === n.y)) {
                    explorer.queue.push(n);
                }
            }
        }
        
        // Move to next in queue
        if (explorer.queue.length > 0) {
            const next = explorer.queue.shift();
            explorer.x = next.x;
            explorer.y = next.y;
        }
    });
    
    steps++;
    renderGrid();
    updateStats();
    
    if (isComplete()) {
        stop();
        document.getElementById('status').textContent = 'Complete!';
        alert(`Map fully explored in ${steps} steps!`);
    }
}

function isComplete() {
    for (let y = 0; y < GRID_SIZE; y++) {
        for (let x = 0; x < GRID_SIZE; x++) {
            if (grid[y][x] === 0) return false;
        }
    }
    return true;
}

function updateStats() {
    document.getElementById('steps').textContent = steps;
    const total = GRID_SIZE * GRID_SIZE;
    const explored = grid.flat().filter(c => c === 1).length;
    const percentage = Math.round((explored / total) * 100);
    document.getElementById('explored').textContent = percentage + '%';
}

function start() {
    if (!isRunning) {
        isRunning = true;
        document.getElementById('startBtn').disabled = true;
        document.getElementById('pauseBtn').disabled = false;
        document.getElementById('status').textContent = 'Exploring';
        intervalId = setInterval(moveExplorers, 1000 / speed);
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
