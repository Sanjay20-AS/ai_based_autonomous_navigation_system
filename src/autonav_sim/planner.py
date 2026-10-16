import heapq
from itertools import count

from .grid import GridMap
from .models import Cell, PlanResult


def manhattan(a: Cell, b: Cell) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


class AStarPlanner:
    """A* shortest-path planner with deterministic tie-breaking."""

    def plan(self, grid: GridMap, start: Cell | None = None,
             goal: Cell | None = None) -> PlanResult:
        start, goal = start or grid.start, goal or grid.goal
        if not grid.is_free(start):
            return PlanResult([], 0, False, message="Start cell is blocked or outside the map.")
        if not grid.is_free(goal):
            return PlanResult([], 0, False, message="Goal cell is blocked or outside the map.")
        if start == goal:
            return PlanResult([start], 0, True, 0.0, "Start and goal are the same cell.")

        serial = count()
        frontier = [(float(manhattan(start, goal)), next(serial), start)]
        came_from: dict[Cell, Cell | None] = {start: None}
        g_score = {start: 0.0}
        expanded = 0

        while frontier:
            _, _, current = heapq.heappop(frontier)
            expanded += 1
            if current == goal:
                path, cursor = [], goal
                while cursor is not None:
                    path.append(cursor)
                    cursor = came_from[cursor]
                path.reverse()
                return PlanResult(path, expanded, True, g_score[goal], "Path found.")
            for neighbor in grid.neighbors(current):
                tentative = g_score[current] + 1.0
                if tentative < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative
                    priority = tentative + manhattan(neighbor, goal)
                    heapq.heappush(frontier, (priority, next(serial), neighbor))
        return PlanResult([], expanded, False, message="No valid path exists.")
