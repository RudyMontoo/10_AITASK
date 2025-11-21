# Setup Instructions for Web Frontend

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Installation

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
# Option 1: Using the batch file (Windows)
start_backend.bat

# Option 2: Manual start
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will start on `http://localhost:8000`

### 3. Open the Frontend
```bash
# Option 1: Using the batch file (Windows)
start_frontend.bat

# Option 2: Manual open
# Simply open frontend/index.html in your browser
```

## Project Structure
```
MSE2/
├── backend/
│   ├── main.py              # FastAPI server with WebSocket support
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html          # Main dashboard
│   ├── style.css           # Dashboard styles
│   └── script.js           # Dashboard logic
├── task2_cleaning_simulation/
│   ├── index.html          # Task 2 frontend
│   ├── style.css
│   └── script.js
├── task3_path_planners/
│   ├── index.html          # Task 3 frontend
│   ├── style.css
│   └── script.js
└── [other task folders...]
```

## Features

### Backend (FastAPI)
- RESTful API endpoints
- WebSocket support for real-time simulation updates
- CORS enabled for cross-origin requests
- Connects to existing Python simulations

### Frontend
- Interactive dashboard with all 9 tasks
- Real-time visualization using HTML5 Canvas
- WebSocket connection for live updates
- Responsive design
- Start/Pause/Reset controls
- Speed adjustment slider

## API Endpoints

### REST Endpoints
- `GET /` - API info
- `GET /api/tasks` - List all available tasks

### WebSocket Endpoints
- `WS /ws/{task_id}` - Connect to specific task simulation
  - Send: `{"command": "start"}` to start simulation
  - Send: `{"command": "stop"}` to stop simulation
  - Receive: Real-time simulation updates

## Usage

1. Start the backend server
2. Open the frontend dashboard in your browser
3. Click on any task card to launch that simulation
4. Use the controls to start/pause/reset the simulation
5. Adjust speed with the slider

## Troubleshooting

### Backend won't start
- Make sure port 8000 is not in use
- Check if all dependencies are installed: `pip install -r backend/requirements.txt`

### Frontend can't connect to backend
- Verify backend is running on `http://localhost:8000`
- Check browser console for connection errors
- Ensure CORS is properly configured

### Simulations not working
- Check browser console for JavaScript errors
- Verify WebSocket connection is established
- Make sure backend simulation logic is implemented

## Next Steps
- Add more interactive features
- Implement remaining task simulations
- Add performance metrics and charts
- Create mobile-responsive layouts
