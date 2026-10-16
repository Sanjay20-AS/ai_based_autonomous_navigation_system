from dataclasses import dataclass
from time import perf_counter

from .controller import WaypointController
from .grid import GridMap
from .models import PlanResult
from .planner import AStarPlanner


@dataclass
class SimulationMetrics:
    elapsed_seconds: float = 0.0
    travelled_steps: int = 0
    collision_count: int = 0


class NavigationSimulation:
    def __init__(self, grid: GridMap | None = None):
        self.grid = grid or GridMap()
        self.planner = AStarPlanner()
        self.metrics = SimulationMetrics()
        self.started_at = None
        self.paused = True
        self.robot = self.grid.start
        self.result: PlanResult = self.planner.plan(self.grid)
        self.controller = WaypointController(self.result.path)
        self.status = "READY" if self.result.found else "NO PATH"

    def replan(self):
        self.result = self.planner.plan(self.grid, self.robot, self.grid.goal)
        self.controller = WaypointController(self.result.path)
        self.metrics = SimulationMetrics()
        self.started_at = None
        self.paused = True
        self.status = "READY" if self.result.found else "NO PATH"

    def reset(self):
        self.robot = self.grid.start
        self.replan()

    def toggle_pause(self):
        if not self.result.found or self.status == "ARRIVED":
            return
        self.paused = not self.paused
        if self.paused:
            self.status = "PAUSED"
        else:
            self.status = "RUNNING"
            if self.started_at is None:
                self.started_at = perf_counter()

    def tick(self):
        if self.paused or not self.result.found or self.status == "ARRIVED":
            return
        if self.started_at is None:
            self.started_at = perf_counter()
        next_cell = self.controller.step()
        if next_cell is None:
            self.paused, self.status = True, "NO PATH"
            return
        if not self.grid.is_free(next_cell):
            self.metrics.collision_count += 1
            self.paused, self.status = True, "SAFETY STOP"
            return
        if next_cell != self.robot:
            self.metrics.travelled_steps += 1
        self.robot = next_cell
        if self.controller.finished and self.robot == self.grid.goal:
            self.status, self.paused = "ARRIVED", True
            self.metrics.elapsed_seconds = perf_counter() - self.started_at

    def elapsed(self) -> float:
        if self.started_at is None:
            return self.metrics.elapsed_seconds
        if self.status in ("ARRIVED", "SAFETY STOP"):
            return self.metrics.elapsed_seconds
        return max(0.0, perf_counter() - self.started_at)

    def summary(self) -> dict:
        return {
            "status": self.status,
            "path_found": self.result.found,
            "planned_steps": self.result.steps if self.result.found else None,
            "travelled_steps": self.metrics.travelled_steps,
            "expanded_nodes": self.result.expanded_nodes,
            "obstacle_count": len(self.grid.obstacles),
            "collision_count": self.metrics.collision_count,
            "message": self.result.message,
        }
