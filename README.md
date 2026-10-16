# AI-Based Autonomous Navigation System

A simulation-first Python project demonstrating a virtual robot navigation pipeline: grid mapping, A* path planning, waypoint following, collision checks, and navigation metrics.

**Scope:** educational 2D grid-world simulation. No real robot, camera, LiDAR, ROS, or autonomous vehicle is controlled. Future extensions are labelled accordingly.

## Quick start

Requires Python 3.10+.

**Windows PowerShell**
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m autonav_sim
```

If activation is blocked:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m autonav_sim
```

**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m autonav_sim
```

Headless path-planning report:
```bash
python -m autonav_sim --headless
```

Tests:
```bash
python -m pytest
```

## Controls
- `SPACE`: start/pause
- `R`: reset robot and re-plan
- `P`: re-plan after map changes
- Left-click a grid cell: toggle obstacle (start/goal cannot be blocked)
- `S`: save screenshot to `artifacts/simulation.png`
- `ESC`: quit

Green = start, red = goal, dark grey = obstacle, blue = planned route, yellow = robot.

## Implemented
- Grid environment and static obstacles
- A* shortest-path planner using Manhattan heuristic and 4-direction movement
- Interactive Pygame visualizer and manual obstacle editing
- Waypoint-following virtual robot
- Blocked-cell safety guard and collision-event counter
- Planned/travelled steps and expanded-node metrics
- Headless JSON report and automated tests

## Architecture
`GridMap → AStarPlanner → WaypointController → NavigationSimulation → Visualizer`

- `models.py`: coordinate and result data types
- `grid.py`: map and obstacle operations
- `planner.py`: A* search
- `controller.py`: waypoint following
- `simulation.py`: simulation state and metrics
- `visualizer.py`: Pygame interface
- `main.py`: application entry point

## GitHub publishing
1. Extract the ZIP and open the folder in VS Code.
2. Run the headless demo, GUI, and tests.
3. Create a public repository named `ai-based-autonomous-navigation-system`.
4. From the project root:
   ```bash
   git init
   git add .
   git commit -m "Build A* autonomous navigation simulator"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ai-based-autonomous-navigation-system.git
   git push -u origin main
   ```
5. Replace `YOUR_USERNAME` with your GitHub username.
6. Run the GUI and press `S` to create a screenshot; inspect it and commit it.
7. Pin the repository and add topics such as `python`, `robotics`, `autonomous-navigation`, `path-planning`, `astar`, `simulation`, `pygame`.

## Resume bullet (only after you run and understand it)
**AI-Based Autonomous Navigation System | Python, A*, Pygame**
- Built a 2D virtual navigation simulator using A* path planning, grid-based obstacle modelling, waypoint following, collision checks, and route/search metrics.
- Added interactive obstacle editing, replanning, headless execution, and automated tests for repeatable navigation experiments.

## Metrics
- Planned steps: number of grid moves in the computed route
- Travelled steps: grid moves made by the simulated robot
- Expanded nodes: A* cells explored
- Collision events: attempted unsafe movements caught by the safety guard
- Status: READY, RUNNING, PAUSED, ARRIVED, or NO PATH

These are educational simulation metrics, not real-world vehicle safety or performance claims.

## Limitations and next steps
This version uses static obstacles and discrete four-direction movement. It does not model acceleration, braking, wheel slip, localization error, sensor noise, traffic rules, or safety-certified control. Future work could add Dijkstra comparison, weighted A*, dynamic obstacles, PID/differential-drive motion, simulated LiDAR, and ROS 2/Gazebo integration. Do not describe future work as implemented until you have built and tested it.
