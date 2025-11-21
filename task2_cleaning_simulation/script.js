const GRID_SIZE = 20;
let grid = [];
let agents = [];
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
    grid = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(1)); // 1 = dirty
    agents = [
        { id: 1, x: 0, y: 0, color: 'agent1' },
        { id: 2, x: GRID_SIZE-1, y: 0, color: 'agent2' },
        { id: 3, x: 0, y: GRID_SIZE-1, color: 'agent3' },
        { id: 4, x: GRID_SIZE-1, y: GRID_SIZE-1, color: 'agent4' }
    ];
    steps = 0;
    renderGrid();
    updateStats();
}

function renderGrid() {
    gridElement.innerHTML = '';
    for (let row = 0; row < GRID_SIZE; row++) {
        for (let col = 0; col < GRID_SIZE; col++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            
            // Check if any agent is at this position
            // Agents use x=col, y=row
            const agent = agents.find(a => a.x === col && a.y === row);
            if (agent) {
                cell.classList.add(agent.color);
            } else {
                cell.classList.add(grid[row][col] === 1 ? 'dirty' : 'clean');
            }
            
            gridElement.appendChild(cell);
        }
    }
}

function moveAgents() {
    agents.forEach(agent => {
        // Clean current cell
        grid[agent.y][agent.x] = 0;
        
        // Find nearest dirty cell
        let bestMove = null;
        let minDist = Infinity;
        
        const moves = [
            { dx: 0, dy: -1 }, { dx: 1, dy: 0 },
            { dx: 0, dy: 1 }, { dx: -1, dy: 0 }
        ];
        
        for (const move of moves) {
            const nx = agent.x + move.dx;
            const ny = agent.y + move.dy;
            
            if (nx >= 0 && nx < GRID_SIZE && ny >= 0 && ny < GRID_SIZE) {
                // Check if another agent is there
                const occupied = agents.some(a => a.id !== agent.id && a.x === nx && a.y === ny);
                if (!occupied) {
                    const dist = findNearestDirty(nx, ny);
                    if (dist < minDist) {
                        minDist = dist;
                        bestMove = { x: nx, y: ny };
                    }
                }
            }
        }
        
        if (bestMove) {
            agent.x = bestMove.x;
            agent.y = bestMove.y;
        }
    });
    
    steps++;
    renderGrid();
    updateStats();
    
    if (isComplete()) {
        stop();
        alert(`Cleaning complete in ${steps} steps!`);
    }
}

function findNearestDirty(x, y) {
    let minDist = Infinity;
    for (let dy = 0; dy < GRID_SIZE; dy++) {
        for (let dx = 0; dx < GRID_SIZE; dx++) {
            if (grid[dy][dx] === 1) {
                const dist = Math.abs(x - dx) + Math.abs(y - dy);
                minDist = Math.min(minDist, dist);
            }
        }
    }
    return minDist;
}

function isComplete() {
    return grid.every(row => row.every(cell => cell === 0));
}

function updateStats() {
    document.getElementById('steps').textContent = steps;
    const totalCells = GRID_SIZE * GRID_SIZE;
    const cleanedCells = grid.flat().filter(c => c === 0).length;
    const percentage = Math.round((cleanedCells / totalCells) * 100);
    document.getElementById('cleaned').textContent = percentage + '%';
}

function start() {
    if (!isRunning) {
        isRunning = true;
        startBtn.disabled = true;
        pauseBtn.disabled = false;
        const delay = 1000 / speed;
        intervalId = setInterval(moveAgents, delay);
    }
}

function pause() {
    isRunning = false;
    startBtn.disabled = false;
    pauseBtn.disabled = true;
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

// Initialize
initGrid();
