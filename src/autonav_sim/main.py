import argparse
import json

from .grid import GridMap
from .planner import AStarPlanner
from .simulation import NavigationSimulation
from .visualizer import Visualizer


def run_headless() -> int:
    grid = GridMap()
    result = AStarPlanner().plan(grid)
    print(json.dumps({
        "mode": "headless",
        "algorithm": "A*",
        "heuristic": "Manhattan distance",
        "movement": "4-direction, unit cost",
        "path_found": result.found,
        "planned_steps": result.steps if result.found else None,
        "expanded_nodes": result.expanded_nodes,
        "obstacle_count": len(grid.obstacles),
        "message": result.message,
    }, indent=2))
    return 0 if result.found else 1


def main():
    parser = argparse.ArgumentParser(description="AI-Based Autonomous Navigation System")
    parser.add_argument("--headless", action="store_true",
                        help="print planning metrics without opening a window")
    args = parser.parse_args()
    if args.headless:
        raise SystemExit(run_headless())
    Visualizer(NavigationSimulation()).run()


if __name__ == "__main__":
    main()
