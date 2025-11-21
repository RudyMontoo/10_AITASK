const GRID_SIZE = 18;
let grid = [];
let bots = [];
let victims = [];
let base = { x: 9, y: 9 };
let isRunning = false;
let intervalId = null;
let steps = 0;
let speed = 5;
let rescued = 0;

const gridElement = document.getElementById('grid');

function initGrid() {
    grid = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(0));
    
    // Add obstacles
    for (let i = 0; i < 40; i++) {
        const x = Math.floor(Math.random() * GRID_SIZE);
        const y = Math.floor(Math.random() * GRID_SIZE);
        if (x !== base.x || y !== base.y) grid[y][x] = 1;
    }
    
    bots = [
        { id: 1, x: 1, y: 1, color: 'bot1', hasVictim: false, target: null },
        { id: 2, x: 16, y: 1, color: 'bot2', hasVictim: false, target: null },
        { id: 3, x: 1, y: 16, color: 'bot3', hasVictim: false, target: null },
        { id: 4, x: 16, y: 16, color: 'bot4', hasVictim: false, target: null }
    ];
    
    victims = [];
    for (let i = 0; i < 15; i++) {
        let x, y;
        do {
            x = Math.floor(Math.random() * GRID_SIZE);
            y = Math.floor(Math.random() * GRID_SIZE);
        } while (grid[y][x] === 1 || (x === base.x && y === base.y) || bots.some(b => b.x === x && b.y === y));
        victims.push({ x, y, rescued: false });
    }
    
    grid[base.y][base.x] = 0;
    bots.forEach(b => grid[b.y][b.x] = 0);
    
    steps = 0;
    rescued = 0;
    renderGrid();
    updateStats();
}

function renderGrid() {
    gridElement.innerHTML = '';
    for (let y = 0; y < GRID_SIZE; y++) {
        for (let x = 0; x < GRID_SIZE; x++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            
            const bot = bots.find(b => b.x === x && b.y === y);
            const victim = victims.find(v => v.x === x && v.y === y && !v.rescued);
            
            if (bot) {
                cell.classList.add(bot.color);
            } else if (x === base.x && y === base.y) {
                cell.classList.add('base');
            } else if (victim) {
                cell.classList.add('victim');
            } else if (grid[y][x] === 1) {
                cell.classList.add('obstacle');
            } else {
                cell.classList.add('empty');
            }
            
            gridElement.appendChild(cell);
        }
    }
}

function moveBots() {
    bots.forEach(bot => {
        if (!bot.hasVictim && !bot.target) {
            let nearest = null;
            let minDist = Infinity;
            victims.forEach(v => {
                if (!v.rescued && !bots.some(b => b.target === v)) {
                    const dist = Math.abs(bot.x - v.x) + Math.abs(bot.y - v.y);
                    if (dist < minDist) {
                        minDist = dist;
                        nearest = v;
                    }
                }
            });
            bot.target = nearest;
        }
        
        if (bot.hasVictim) {
            moveTowards(bot, base.x, base.y);
            if (bot.x === base.x && bot.y === base.y) {
                bot.hasVictim = false;
                rescued++;
            }
        } else if (bot.target) {
            moveTowards(bot, bot.target.x, bot.target.y);
            if (bot.x === bot.target.x && bot.y === bot.target.y) {
                bot.target.rescued = true;
                bot.hasVictim = true;
                bot.target = null;
            }
        }
    });
    
    steps++;
    renderGrid();
    updateStats();
    
    if (rescued === victims.length) {
        stop();
        document.getElementById('status').textContent = 'Mission Complete!';
        alert(`All victims rescued in ${steps} steps!`);
    }
}

function moveTowards(bot, targetX, targetY) {
    const dx = targetX > bot.x ? 1 : targetX < bot.x ? -1 : 0;
    const dy = targetY > bot.y ? 1 : targetY < bot.y ? -1 : 0;
    
    const nx = bot.x + dx;
    const ny = bot.y + dy;
    
    if (dx !== 0 && nx >= 0 && nx < GRID_SIZE && grid[ny === bot.y ? bot.y : ny][nx] === 0) {
        bot.x = nx;
    } else if (dy !== 0 && ny >= 0 && ny < GRID_SIZE && grid[ny][bot.x] === 0) {
        bot.y = ny;
    }
}

function updateStats() {
    document.getElementById('steps').textContent = steps;
    document.getElementById('rescued').textContent = `${rescued}/${victims.length}`;
}

function start() {
    if (!isRunning) {
        isRunning = true;
        document.getElementById('startBtn').disabled = true;
        document.getElementById('pauseBtn').disabled = false;
        document.getElementById('status').textContent = 'Rescuing';
        intervalId = setInterval(moveBots, 1000 / speed);
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
