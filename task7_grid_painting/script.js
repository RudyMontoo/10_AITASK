const GRID_SIZE = 20;
let grid = [];
let robots = [];
let isRunning = false;
let intervalId = null;
let steps = 0;
let speed = 5;

const gridElement = document.getElementById('grid');

function initGrid() {
    grid = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(0)); // 0 = unpainted
    
    // Add obstacles
    for (let i = 0; i < 30; i++) {
        const x = Math.floor(Math.random() * GRID_SIZE);
        const y = Math.floor(Math.random() * GRID_SIZE);
        grid[y][x] = 2; // 2 = obstacle
    }
    
    robots = [
        { id: 1, x: 0, y: 0, color: 'robot1', stack: [] },
        { id: 2, x: 19, y: 0, color: 'robot2', stack: [] },
        { id: 3, x: 0, y: 19, color: 'robot3', stack: [] },
        { id: 4, x: 19, y: 19, color: 'robot4', stack: [] }
    ];
    
    // Clear robot starting positions
    robots.forEach(r => grid[r.y][r.x] = 0);
    
    // Initialize DFS stacks
    robots.forEach(r => r.stack.push({ x: r.x, y: r.y }));
    
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
            
            const robot = robots.find(r => r.x === x && r.y === y);
            
            if (robot) {
                cell.classList.add(robot.color);
            } else if (grid[y][x] === 2) {
                cell.classList.add('obstacle');
            } else if (grid[y][x] === 1) {
                cell.classList.add('painted');
            } else {
                cell.classList.add('unpainted');
            }
            
            gridElement.appendChild(cell);
        }
    }
}

function moveRobots() {
    robots.forEach(robot => {
        // Paint current cell
        if (grid[robot.y][robot.x] === 0) {
            grid[robot.y][robot.x] = 1;
        }
        
        // DFS: explore neighbors
        const neighbors = [
            { x: robot.x, y: robot.y - 1 },
            { x: robot.x + 1, y: robot.y },
            { x: robot.x, y: robot.y + 1 },
            { x: robot.x - 1, y: robot.y }
        ];
        
        let moved = false;
        for (const n of neighbors) {
            if (n.x >= 0 && n.x < GRID_SIZE && n.y >= 0 && n.y < GRID_SIZE) {
                if (grid[n.y][n.x] === 0 && !robots.some(r => r.x === n.x && r.y === n.y)) {
                    robot.stack.push({ x: robot.x, y: robot.y });
                    robot.x = n.x;
                    robot.y = n.y;
                    moved = true;
                    break;
                }
            }
        }
        
        // Backtrack if no unpainted neighbors
        if (!moved && robot.stack.length > 0) {
            const prev = robot.stack.pop();
            robot.x = prev.x;
            robot.y = prev.y;
        }
    });
    
    steps++;
    renderGrid();
    updateStats();
    
    if (isComplete()) {
        stop();
        document.getElementById('status').textContent = 'Complete!';
        alert(`Painting complete in ${steps} steps!`);
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
    const painted = grid.flat().filter(c => c === 1).length;
    const percentage = Math.round((painted / total) * 100);
    document.getElementById('painted').textContent = percentage + '%';
    
    // Update progress bar
    document.getElementById('progressBar').style.width = percentage + '%';
    document.getElementById('progressText').textContent = percentage + '%';
}

function start() {
    if (!isRunning) {
        isRunning = true;
        document.getElementById('startBtn').disabled = true;
        document.getElementById('pauseBtn').disabled = false;
        document.getElementById('status').textContent = 'Painting';
        intervalId = setInterval(moveRobots, 1000 / speed);
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
