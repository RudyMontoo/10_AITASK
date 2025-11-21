const GRID_SIZE = 20;
let grid = [];
let agents = [];
let resources = [];
let isRunning = false;
let intervalId = null;
let steps = 0;
let speed = 5;
let collected = 0;

const gridElement = document.getElementById('grid');

function initGrid() {
    grid = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(0));
    
    agents = [
        { id: 1, x: 0, y: 0, color: 'agent1', target: null },
        { id: 2, x: 19, y: 0, color: 'agent2', target: null },
        { id: 3, x: 0, y: 19, color: 'agent3', target: null },
        { id: 4, x: 19, y: 19, color: 'agent4', target: null }
    ];
    
    resources = [];
    for (let i = 0; i < 25; i++) {
        let x, y;
        do {
            x = Math.floor(Math.random() * GRID_SIZE);
            y = Math.floor(Math.random() * GRID_SIZE);
        } while (agents.some(a => a.x === x && a.y === y) || resources.some(r => r.x === x && r.y === y));
        resources.push({ x, y, collected: false });
    }
    
    steps = 0;
    collected = 0;
    renderGrid();
    updateStats();
}

function renderGrid() {
    gridElement.innerHTML = '';
    for (let y = 0; y < GRID_SIZE; y++) {
        for (let x = 0; x < GRID_SIZE; x++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            
            const agent = agents.find(a => a.x === x && a.y === y);
            const resource = resources.find(r => r.x === x && r.y === y && !r.collected);
            
            if (agent) {
                cell.classList.add(agent.color);
            } else if (resource) {
                cell.classList.add('resource');
            } else {
                cell.classList.add('empty');
            }
            
            gridElement.appendChild(cell);
        }
    }
}

function moveAgents() {
    agents.forEach(agent => {
        if (!agent.target) {
            let nearest = null;
            let minDist = Infinity;
            resources.forEach(r => {
                if (!r.collected && !agents.some(a => a.target === r)) {
                    const dist = Math.abs(agent.x - r.x) + Math.abs(agent.y - r.y);
                    if (dist < minDist) {
                        minDist = dist;
                        nearest = r;
                    }
                }
            });
            agent.target = nearest;
        }
        
        if (agent.target) {
            moveTowards(agent, agent.target.x, agent.target.y);
            if (agent.x === agent.target.x && agent.y === agent.target.y) {
                agent.target.collected = true;
                agent.target = null;
                collected++;
            }
        }
    });
    
    steps++;
    renderGrid();
    updateStats();
    
    if (collected === resources.length) {
        stop();
        document.getElementById('status').textContent = 'Complete!';
        alert(`All resources collected in ${steps} steps!`);
    }
}

function moveTowards(agent, targetX, targetY) {
    const dx = targetX > agent.x ? 1 : targetX < agent.x ? -1 : 0;
    const dy = targetY > agent.y ? 1 : targetY < agent.y ? -1 : 0;
    
    if (dx !== 0) agent.x += dx;
    else if (dy !== 0) agent.y += dy;
}

function updateStats() {
    document.getElementById('steps').textContent = steps;
    document.getElementById('collected').textContent = `${collected}/${resources.length}`;
}

function start() {
    if (!isRunning) {
        isRunning = true;
        document.getElementById('startBtn').disabled = true;
        document.getElementById('pauseBtn').disabled = false;
        document.getElementById('status').textContent = 'Collecting';
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
