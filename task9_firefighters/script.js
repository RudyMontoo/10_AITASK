const GRID_SIZE = 18;
let grid = [];
let firefighters = [];
let fires = [];
let isRunning = false;
let intervalId = null;
let steps = 0;
let speed = 5;

const gridElement = document.getElementById('grid');

function initGrid() {
    grid = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(0)); // 0 = safe, 1 = fire, 2 = extinguished
    
    firefighters = [
        { id: 1, x: 1, y: 1, color: 'ff1', target: null },
        { id: 2, x: 16, y: 1, color: 'ff2', target: null },
        { id: 3, x: 1, y: 16, color: 'ff3', target: null },
        { id: 4, x: 16, y: 16, color: 'ff4', target: null }
    ];
    
    // Start fires
    fires = [];
    for (let i = 0; i < 15; i++) {
        let x, y;
        do {
            x = Math.floor(Math.random() * GRID_SIZE);
            y = Math.floor(Math.random() * GRID_SIZE);
        } while (firefighters.some(f => f.x === x && f.y === y) || fires.some(f => f.x === x && f.y === y));
        fires.push({ x, y, active: true });
        grid[y][x] = 1;
    }
    
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
            
            const ff = firefighters.find(f => f.x === x && f.y === y);
            
            if (ff) {
                cell.classList.add(ff.color);
            } else if (grid[y][x] === 1) {
                cell.classList.add('fire');
            } else if (grid[y][x] === 2) {
                cell.classList.add('extinguished');
            } else {
                cell.classList.add('safe');
            }
            
            gridElement.appendChild(cell);
        }
    }
}

function moveFirefighters() {
    // Spread fires
    if (Math.random() < 0.1) {
        const activeFires = fires.filter(f => f.active);
        if (activeFires.length > 0) {
            const fire = activeFires[Math.floor(Math.random() * activeFires.length)];
            const neighbors = [
                { x: fire.x + 1, y: fire.y },
                { x: fire.x - 1, y: fire.y },
                { x: fire.x, y: fire.y + 1 },
                { x: fire.x, y: fire.y - 1 }
            ];
            
            for (const n of neighbors) {
                if (n.x >= 0 && n.x < GRID_SIZE && n.y >= 0 && n.y < GRID_SIZE && grid[n.y][n.x] === 0) {
                    if (Math.random() < 0.3) {
                        grid[n.y][n.x] = 1;
                        fires.push({ x: n.x, y: n.y, active: true });
                        break;
                    }
                }
            }
        }
    }
    
    // Move firefighters
    firefighters.forEach(ff => {
        if (!ff.target) {
            let nearest = null;
            let minDist = Infinity;
            fires.forEach(f => {
                if (f.active && !firefighters.some(fighter => fighter.target === f)) {
                    const dist = Math.abs(ff.x - f.x) + Math.abs(ff.y - f.y);
                    if (dist < minDist) {
                        minDist = dist;
                        nearest = f;
                    }
                }
            });
            ff.target = nearest;
        }
        
        if (ff.target) {
            moveTowards(ff, ff.target.x, ff.target.y);
            if (ff.x === ff.target.x && ff.y === ff.target.y) {
                ff.target.active = false;
                grid[ff.target.y][ff.target.x] = 2;
                ff.target = null;
            }
        }
    });
    
    steps++;
    renderGrid();
    updateStats();
    
    const activeFires = fires.filter(f => f.active).length;
    if (activeFires === 0) {
        stop();
        document.getElementById('status').textContent = 'All Clear!';
        alert(`All fires extinguished in ${steps} steps!`);
    }
}

function moveTowards(ff, targetX, targetY) {
    const dx = targetX > ff.x ? 1 : targetX < ff.x ? -1 : 0;
    const dy = targetY > ff.y ? 1 : targetY < ff.y ? -1 : 0;
    
    if (dx !== 0) ff.x += dx;
    else if (dy !== 0) ff.y += dy;
}

function updateStats() {
    document.getElementById('steps').textContent = steps;
    const activeFires = fires.filter(f => f.active).length;
    document.getElementById('fires').textContent = activeFires;
}

function start() {
    if (!isRunning) {
        isRunning = true;
        document.getElementById('startBtn').disabled = true;
        document.getElementById('pauseBtn').disabled = false;
        document.getElementById('status').textContent = 'Fighting';
        intervalId = setInterval(moveFirefighters, 1000 / speed);
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
