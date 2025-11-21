const API_URL = 'http://localhost:8000';

function openTask(taskId) {
    // Map task IDs to their HTML files
    const taskMap = {
        'task1': '../task1_DMN/index.html',
        'task2': '../task2_cleaning_simulation/index.html',
        'task3': '../task3_path_planners/index.html',
        'task4': '../task4_warehouse_pickup/index.html',
        'task5': '../task5_rescue_bots/index.html',
        'task6': '../task6_drone_delivery/index.html',
        'task7': '../task7_grid_painting/index.html',
        'task8': '../task8_resource_collection/index.html',
        'task9': '../task9_firefighters/index.html',
        'task10': '../task10_map_exploration/index.html'
    };
    
    const url = taskMap[taskId];
    if (url) {
        window.open(url, '_blank');
    } else {
        alert(`Task ${taskId} is not yet implemented`);
    }
}

// Check API connection on load
async function checkAPIConnection() {
    try {
        const response = await fetch(`${API_URL}/`);
        const data = await response.json();
        console.log('API Connected:', data);
    } catch (error) {
        console.warn('API not available. Running in standalone mode.');
    }
}

// Load tasks from API
async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/api/tasks`);
        const data = await response.json();
        console.log('Available tasks:', data.tasks);
    } catch (error) {
        console.warn('Could not load tasks from API');
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkAPIConnection();
    loadTasks();
});
