const GRID_SIZE = 16;
let grid = [];
let drones = [];
let destinations = [];
let hub = { x: 8, y: 8 };
let isRunning = false;
let intervalId = null;
let steps = 0;
let speed = 5;
let delivered = 0;

const gridElement = document.getElementById('grid');

function initGrid() {
    grid = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(0));
    
    drones = [
        { id: 1, x: 8, y: 8, color: 'drone1', hasPackage: false, target: null },
        { id: 2, x: 8, y: 8, color: 'drone2', hasPackage: false, target: null },
        { id: 3, x: 8, y: 8, color: 'drone3', hasPackage: false, target: null }
    ];
    
    destinations = [];
    for (let i = 0; i < 12; i++) {
        let x, y;
        do {
            x = Math.floor(Math.random() * GRID_SIZE);
            y = Math.floor(Math.random() * GRID_SIZE);
        } while ((x === hub.x && y === hub.y) || destinations.some(d => d.x === x && d.y === y));
        destinations.push({ x, y, delivered: false });
    }
    
    steps = 0;
    delivered = 0;
    renderGrid();
    updateStats();
}

function renderGrid() {
    gridElement.innerHTML = '';
    for (let y = 0; y < GRID_SIZE; y++) {
        for (let x = 0; x < GRID_SIZE; x++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            
            const drone = drones.find(d => d.x === x && d.y === y);
            const dest = destinations.find(d => d.x === x && d.y === y && !d.delivered);
            
            if (drone) {
                cell.classList.add(drone.color);
            } else if (x === hub.x && y === hub.y) {
                cell.classList.add('hub');
            } else if (dest) {
                cell.classList.add('destination');
            } else {
                cell.classList.add('empty');
            }
            
            gridElement.appendChild(cell);
        }
    }
}

function moveDrones() {
    drones.forEach(drone => {
        if (!drone.hasPackage && !drone.target) {
            let nearest = null;
            let minDist = Infinity;
            destinations.forEach(d => {
                if (!d.delivered && !drones.some(dr => dr.target === d)) {
                    const dist = Math.abs(drone.x - d.x) + Math.abs(drone.y - d.y);
                    if (dist < minDist) {
                        minDist = dist;
                        nearest = d;
                    }
                }
            });
            if (nearest) {
                drone.target = nearest;
                drone.hasPackage = true;
            }
        }
        
        if (drone.hasPackage && drone.target) {
            moveTowards(drone, drone.target.x, drone.target.y);
            if (drone.x === drone.target.x && drone.y === drone.target.y) {
                drone.target.delivered = true;
                drone.hasPackage = false;
                drone.target = null;
                delivered++;
            }
        } else if (!drone.hasPackage && !drone.target) {
            moveTowards(drone, hub.x, hub.y);
        }
    });
    
    steps++;
    renderGrid();
    updateStats();
    
    if (delivered === destinations.length) {
        stop();
        document.getElementById('status').textContent = 'Complete!';
        alert(`All deliveries complete in ${steps} steps!`);
    }
}

function moveTowards(drone, targetX, targetY) {
    const dx = targetX > drone.x ? 1 : targetX < drone.x ? -1 : 0;
    const dy = targetY > drone.y ? 1 : targetY < drone.y ? -1 : 0;
    
    if (dx !== 0) drone.x += dx;
    else if (dy !== 0) drone.y += dy;
}

function updateStats() {
    document.getElementById('steps').textContent = steps;
    document.getElementById('delivered').textContent = `${delivered}/${destinations.length}`;
}

function start() {
    if (!isRunning) {
        isRunning = true;
        document.getElementById('startBtn').disabled = true;
        document.getElementById('pauseBtn').disabled = false;
        document.getElementById('status').textContent = 'Delivering';
        intervalId = setInterval(moveDrones, 1000 / speed);
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
