from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio
import json
from typing import Dict, List
import sys
import os

# Add parent directory to path to import simulations
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="Multi-Agent Simulations API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active WebSocket connections
active_connections: Dict[str, List[WebSocket]] = {}

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, task_id: str):
        await websocket.accept()
        if task_id not in self.active_connections:
            self.active_connections[task_id] = []
        self.active_connections[task_id].append(websocket)

    def disconnect(self, websocket: WebSocket, task_id: str):
        if task_id in self.active_connections:
            self.active_connections[task_id].remove(websocket)

    async def send_message(self, message: dict, task_id: str):
        if task_id in self.active_connections:
            for connection in self.active_connections[task_id]:
                try:
                    await connection.send_json(message)
                except:
                    pass

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"message": "Multi-Agent Simulations API", "version": "1.0"}

@app.get("/api/tasks")
async def get_tasks():
    """Get list of all available tasks"""
    return {
        "tasks": [
            {"id": "task2", "name": "Cleaning Simulation", "agents": 4},
            {"id": "task3", "name": "Path Planning (A*)", "agents": 4},
            {"id": "task4", "name": "Warehouse Pickup", "agents": 4},
            {"id": "task5", "name": "Rescue Bots", "agents": 4},
            {"id": "task6", "name": "Drone Delivery", "agents": 3},
            {"id": "task7", "name": "Grid Painting", "agents": 4},
            {"id": "task8", "name": "Resource Collection", "agents": 4},
            {"id": "task9", "name": "Firefighters", "agents": 4},
            {"id": "task10", "name": "Map Exploration", "agents": 4}
        ]
    }

@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await manager.connect(websocket, task_id)
    try:
        while True:
            data = await websocket.receive_json()
            command = data.get("command")
            
            if command == "start":
                await run_simulation(task_id, websocket)
            elif command == "stop":
                await manager.send_message({"type": "stopped"}, task_id)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, task_id)

async def run_simulation(task_id: str, websocket: WebSocket):
    """Run the appropriate simulation based on task_id"""
    
    if task_id == "task2":
        await run_cleaning_simulation(websocket)
    elif task_id == "task3":
        await run_pathfinding_simulation(websocket)
    elif task_id == "task4":
        await run_warehouse_simulation(websocket)
    elif task_id == "task5":
        await run_rescue_simulation(websocket)
    elif task_id == "task6":
        await run_drone_simulation(websocket)
    elif task_id == "task7":
        await run_painting_simulation(websocket)
    elif task_id == "task8":
        await run_resource_simulation(websocket)
    elif task_id == "task9":
        await run_firefighter_simulation(websocket)
    elif task_id == "task10":
        await run_exploration_simulation(websocket)

async def run_cleaning_simulation(websocket: WebSocket):
    """Task 2: Cleaning Simulation"""
    GRID_SIZE = 20
    grid = [[1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    agents = [
        {"id": 1, "x": 0, "y": 0, "color": "agent1"},
        {"id": 2, "x": GRID_SIZE-1, "y": 0, "color": "agent2"},
        {"id": 3, "x": 0, "y": GRID_SIZE-1, "color": "agent3"},
        {"id": 4, "x": GRID_SIZE-1, "y": GRID_SIZE-1, "color": "agent4"}
    ]
    
    steps = 0
    while not all(cell == 0 for row in grid for cell in row):
        # Clean current positions
        for agent in agents:
            grid[agent["y"]][agent["x"]] = 0
        
        # Move agents
        for agent in agents:
            moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            best_move = None
            min_dist = float('inf')
            
            for dx, dy in moves:
                nx, ny = agent["x"] + dx, agent["y"] + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    occupied = any(a["x"] == nx and a["y"] == ny and a["id"] != agent["id"] for a in agents)
                    if not occupied:
                        dist = sum(1 for row in grid for cell in row if cell == 1)
                        if dist < min_dist:
                            min_dist = dist
                            best_move = (nx, ny)
            
            if best_move:
                agent["x"], agent["y"] = best_move
        
        steps += 1
        cleaned = sum(1 for row in grid for cell in row if cell == 0)
        total = GRID_SIZE * GRID_SIZE
        
        await websocket.send_json({
            "type": "update",
            "step": steps,
            "agents": agents,
            "grid": grid,
            "progress": round((cleaned / total) * 100, 1)
        })
        
        await asyncio.sleep(0.1)
    
    await websocket.send_json({"type": "complete", "steps": steps})

async def run_pathfinding_simulation(websocket: WebSocket):
    """Task 3: Path Planning"""
    import random
    GRID_SIZE = 15
    
    # Create grid with obstacles
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for _ in range(30):
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        grid[y][x] = 1
    
    agents = [
        {"id": 1, "x": 1, "y": 1, "targetX": 13, "targetY": 13, "color": "agent1"},
        {"id": 2, "x": 13, "y": 1, "targetX": 1, "targetY": 13, "color": "agent2"},
        {"id": 3, "x": 1, "y": 13, "targetX": 13, "targetY": 1, "color": "agent3"},
        {"id": 4, "x": 13, "y": 13, "targetX": 1, "targetY": 1, "color": "agent4"}
    ]
    
    # Clear agent positions
    for agent in agents:
        grid[agent["y"]][agent["x"]] = 0
        grid[agent["targetY"]][agent["targetX"]] = 0
    
    await websocket.send_json({
        "type": "init",
        "grid": grid,
        "agents": agents
    })
    
    # Simple movement simulation
    steps = 0
    max_steps = 50
    while steps < max_steps:
        for agent in agents:
            dx = 1 if agent["x"] < agent["targetX"] else -1 if agent["x"] > agent["targetX"] else 0
            dy = 1 if agent["y"] < agent["targetY"] else -1 if agent["y"] > agent["targetY"] else 0
            
            nx, ny = agent["x"] + dx, agent["y"] + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[ny][nx] == 0:
                agent["x"], agent["y"] = nx, ny
        
        steps += 1
        await websocket.send_json({
            "type": "update",
            "step": steps,
            "agents": agents
        })
        
        await asyncio.sleep(0.2)
    
    await websocket.send_json({"type": "complete", "steps": steps})

async def run_warehouse_simulation(websocket: WebSocket):
    """Task 4: Warehouse Pickup"""
    await websocket.send_json({"type": "info", "message": "Warehouse simulation starting..."})
    await asyncio.sleep(1)
    await websocket.send_json({"type": "complete", "message": "Simulation complete"})

async def run_rescue_simulation(websocket: WebSocket):
    """Task 5: Rescue Bots"""
    await websocket.send_json({"type": "info", "message": "Rescue simulation starting..."})
    await asyncio.sleep(1)
    await websocket.send_json({"type": "complete", "message": "Simulation complete"})

async def run_drone_simulation(websocket: WebSocket):
    """Task 6: Drone Delivery"""
    await websocket.send_json({"type": "info", "message": "Drone simulation starting..."})
    await asyncio.sleep(1)
    await websocket.send_json({"type": "complete", "message": "Simulation complete"})

async def run_painting_simulation(websocket: WebSocket):
    """Task 7: Grid Painting"""
    await websocket.send_json({"type": "info", "message": "Painting simulation starting..."})
    await asyncio.sleep(1)
    await websocket.send_json({"type": "complete", "message": "Simulation complete"})

async def run_resource_simulation(websocket: WebSocket):
    """Task 8: Resource Collection"""
    await websocket.send_json({"type": "info", "message": "Resource simulation starting..."})
    await asyncio.sleep(1)
    await websocket.send_json({"type": "complete", "message": "Simulation complete"})

async def run_firefighter_simulation(websocket: WebSocket):
    """Task 9: Firefighters"""
    await websocket.send_json({"type": "info", "message": "Firefighter simulation starting..."})
    await asyncio.sleep(1)
    await websocket.send_json({"type": "complete", "message": "Simulation complete"})

async def run_exploration_simulation(websocket: WebSocket):
    """Task 10: Map Exploration"""
    await websocket.send_json({"type": "info", "message": "Exploration simulation starting..."})
    await asyncio.sleep(1)
    await websocket.send_json({"type": "complete", "message": "Simulation complete"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
