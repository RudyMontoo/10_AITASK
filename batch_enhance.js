// Batch Enhancement Script for All Tasks
// This script contains the common enhancements to apply

const commonEnhancements = {
    // Grid CSS
    gridCSS: `
    display: grid !important;
    grid-template-columns: repeat(var(--grid-size, 20), var(--cell-size, 28px)) !important;
    gap: 3px;
    justify-content: center;
    margin-bottom: 20px;
    padding: 15px;
    background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
    border-radius: 15px;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.1);
    min-height: 620px;
    visibility: visible !important;
    `,
    
    // Cell CSS
    cellCSS: `
    width: var(--cell-size, 28px) !important;
    height: var(--cell-size, 28px) !important;
    border-radius: 6px;
    transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    position: relative;
    display: block !important;
    `,
    
    // Container CSS
    containerCSS: `
    position: relative;
    animation: fadeIn 0.5s ease-in;
    `,
    
    // Progress Bar HTML
    progressBarHTML: `
    <div class="progress-container">
        <div class="progress-bar" id="progressBar"></div>
        <span class="progress-text" id="progressText">0%</span>
    </div>
    `,
    
    // Progress Bar CSS
    progressBarCSS: `
    .progress-container {
        width: 100%;
        height: 30px;
        background: #e9ecef;
        border-radius: 15px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--progress-color-1), var(--progress-color-2));
        border-radius: 15px;
        transition: width 0.5s ease-out;
        width: 0%;
        box-shadow: 0 0 20px var(--progress-color-1);
    }
    
    .progress-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-weight: bold;
        color: #333;
        font-size: 0.9em;
        text-shadow: 0 1px 2px rgba(255,255,255,0.8);
    }
    `
};

// Task-specific color schemes
const taskColors = {
    task3: { primary: '#f093fb', secondary: '#f5576c' },
    task5: { primary: '#ff9a56', secondary: '#ff6a88' },
    task6: { primary: '#30cfd0', secondary: '#330867' },
    task7: { primary: '#a8edea', secondary: '#fed6e3' },
    task8: { primary: '#ffecd2', secondary: '#fcb69f' },
    task9: { primary: '#ff6b6b', secondary: '#feca57' },
    task10: { primary: '#89f7fe', secondary: '#66a6ff' },
    task1: { primary: '#667eea', secondary: '#764ba2' }
};

console.log('Batch enhancement script loaded');
