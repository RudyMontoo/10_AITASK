const GRID_SIZE = 20;
let grid = [];
let robots = [];
let packages = [];
let depot = { x: 10, y: 10 };
let isRunning = false;
let intervalId = null;
let steps = 0;
let speed = 5;
let collected = 0;

const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');
const resetBtn = document.getElementById('resetBtn');
const speedSlider = document.getElementById('speedSlider');
const gridElement = document.getElementById('grid');

function initGrid() {
    grid = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(0));
    
    robots = [
        { id: 1, x: 0, y: 0, color: 'robot1', hasPackage: false, targetPackage: null },
        { id: 2, x: 19, y: 0, color: 'robot2', hasPackage: false, targetPackage: null },
        { id: 3, x: 0, y: 19, color: 'robot3', hasPackage: false, targetPackage: null },
        { id: 4, x: 19, y: 19, color: 'robot4', hasPackage: false, targetPackage: null }
    ];
    
    packages = [];
    for (let i = 0; i < 20; i++) {
        let x, y;
        do {
            x = Math.floor(Math.random() * GRID_SIZE);
            y = Math.floor(Math.random() * GRID_SIZE);
        } while ((x === depot.x && y === depot.y) || robots.some(r => r.x === x && r.y === y));
        packages.push({ x, y, collected: false });
    }
    
    steps = 0;
    collected = 0;
    renderGrid();
    updateStats();
}

function renderGrid() {
    gridElement.innerHTML = '';
    
    for (let row = 0; row < GRID_SIZE; row++) {
        for (let col = 0; col < GRID_SIZE; col++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            
            const robot = robots.find(r => r.x === col && r.y === row);
            const pkg = packages.find(p => p.x === col && p.y === row && !p.collected);
            
            if (robot) {
                cell.classList.add(robot.color);
            } else if (col === depot.x && row === depot.y) {
                cell.classList.add('depot');
            } else if (pkg) {
                cell.classList.add('package');
            } else {
                cell.classList.add('empty');
            }
            
            gridElement.appendChild(cell);
        }
    }
}

function moveRobots() {
    robots.forEach(robot => {
        if (!robot.hasPackage && !robot.targetPackage) {
            // Find nearest unclaimed package
            let nearest = null;
            let minDist = Infinity;
            packages.forEach(pkg => {
                if (!pkg.collected && !robots.some(r => r.targetPackage === pkg)) {
                    const dist = Math.abs(robot.x - pkg.x) + Math.abs(robot.y - pkg.y);
                    if (dist < minDist) {
                        minDist = dist;
                        nearest = pkg;
                    }
                }
            });
            robot.targetPackage = nearest;
        }
        
        if (robot.hasPackage) {
            // Move to depot
            moveTowards(robot, depot.x, depot.y);
            if (robot.x === depot.x && robot.y === depot.y) {
                robot.hasPackage = false;
                collected++;
            }
        } else if (robot.targetPackage) {
            // Move to package
            moveTowards(robot, robot.targetPackage.x, robot.targetPackage.y);
            if (robot.x === robot.targetPackage.x && robot.y === robot.targetPackage.y) {
                robot.targetPackage.collected = true;
                robot.hasPackage = true;
                robot.targetPackage = null;
            }
        }
    });
    
    steps++;
    renderGrid();
    updateStats();
    
    if (collected === packages.length) {
        stop();
        document.getElementById('status').textContent = 'Complete!';
        alert(`All packages collected in ${steps} steps!`);
    }
}

function moveTowards(robot, targetX, targetY) {
    const dx = targetX > robot.x ? 1 : targetX < robot.x ? -1 : 0;
    const dy = targetY > robot.y ? 1 : targetY < robot.y ? -1 : 0;
    
    if (dx !== 0) robot.x += dx;
    else if (dy !== 0) robot.y += dy;
}

function updateStats() {
    document.getElementById('steps').textContent = steps;
    document.getElementById('collected').textContent = `${collected}/${packages.length}`;
    
    // Update progress bar
    const progress = (collected / packages.length) * 100;
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
        intervalId = setInterval(moveRobots, delay);
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
