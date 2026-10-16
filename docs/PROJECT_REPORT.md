# Project Report: AI-Based Autonomous Navigation System

## Abstract
This project implements a simulation-first autonomous navigation pipeline in a 2D grid world. A* search computes a route between a start and goal while avoiding blocked cells. A waypoint controller advances a virtual robot along the route, and safety checks prevent movement into blocked or out-of-bounds cells. A Pygame interface displays the map and navigation metrics.

## Problem statement
Testing navigation algorithms on physical robots can require hardware, sensors, lab space, and safety controls. A grid-world simulation provides a low-cost, repeatable environment for learning path planning before moving to robotics middleware or hardware.

## Objectives
- Represent an environment as a grid.
- Plan a route using A* and an admissible heuristic.
- Follow waypoints in simulation.
- Guard against occupied cells.
- Display search and navigation metrics.
- Provide tests and reproducible run instructions.

## Methodology
1. Store grid dimensions, start/goal cells, and obstacle cells.
2. Generate four-direction neighbours that are inside the grid and free.
3. Run A*: priority is `f(n) = g(n) + h(n)`, where `g` is route cost and `h` is Manhattan distance.
4. Reconstruct the route by following parent pointers from goal to start.
5. Advance the virtual robot one route cell per simulation tick.
6. Validate the target cell before movement.
7. Record route steps, expanded nodes, obstacle count, and collision events.

## Implemented vs future work

| Capability | Status |
|---|---|
| Grid environment and static obstacles | Implemented |
| A* path planning and Manhattan heuristic | Implemented |
| Interactive Pygame view | Implemented |
| Manual obstacle editing and replanning | Implemented |
| Waypoint following and blocked-cell guard | Implemented |
| Headless JSON report and automated tests | Implemented |
| Dynamic obstacle detection | Future enhancement |
| Camera/LiDAR perception | Future enhancement |
| ROS 2 / Gazebo integration | Future enhancement |
| Physical robot or autonomous vehicle control | Not implemented |

## Testing
Run `python -m pytest`. Tests cover heuristic distance, valid route construction, obstacle avoidance, unreachable goals, blocked start cells, start-equals-goal, and a complete simulated route. Also run the headless mode and manually test UI controls.

## Limitations
This is a discrete educational model. It does not model wheel slip, acceleration, braking distance, localization error, sensor noise, moving actors, road rules, or certified controls. Metrics are simulation measurements, not real-vehicle benchmarks.

## Conclusion
The project demonstrates a testable path-planning loop without physical hardware. Next steps include comparing A* with Dijkstra and weighted A*, then adding a differential-drive model or ROS 2 simulation.

## References
- Hart, Nilsson, Raphael, “A Formal Basis for the Heuristic Determination of Minimum Cost Paths,” IEEE Transactions on Systems Science and Cybernetics, 1968.
- https://docs.python.org/3/
- https://www.pygame.org/docs/
- https://www.redblobgames.com/pathfinding/a-star/introduction.html
