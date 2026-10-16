from autonav_sim.grid import GridMap
from autonav_sim.models import Cell
from autonav_sim.planner import AStarPlanner, manhattan


def test_manhattan_distance():
    assert manhattan(Cell(1, 2), Cell(4, 6)) == 7


def test_astar_finds_path_and_avoids_obstacles():
    grid = GridMap(12, 10)
    grid.clear_obstacles()
    grid.obstacles.update({Cell(4, y) for y in range(1, 8) if y != 5})
    start, goal = Cell(1, 1), Cell(9, 8)
    result = AStarPlanner().plan(grid, start, goal)
    assert result.found and result.path[0] == start and result.path[-1] == goal
    assert all(grid.is_free(cell) for cell in result.path)
    assert all(manhattan(a, b) == 1 for a, b in zip(result.path, result.path[1:]))


def test_astar_reports_no_path():
    grid = GridMap(8, 8)
    grid.clear_obstacles()
    start, goal = Cell(1, 1), Cell(6, 6)
    grid.obstacles.update(Cell(3, y) for y in range(8))
    result = AStarPlanner().plan(grid, start, goal)
    assert not result.found and result.path == []


def test_start_equals_goal():
    grid = GridMap(8, 8)
    grid.clear_obstacles()
    cell = Cell(3, 3)
    result = AStarPlanner().plan(grid, cell, cell)
    assert result.found and result.path == [cell] and result.steps == 0


def test_blocked_start_is_rejected():
    grid = GridMap(8, 8)
    grid.clear_obstacles()
    start, goal = Cell(1, 1), Cell(6, 6)
    grid.obstacles.add(start)
    result = AStarPlanner().plan(grid, start, goal)
    assert not result.found and "Start cell" in result.message
