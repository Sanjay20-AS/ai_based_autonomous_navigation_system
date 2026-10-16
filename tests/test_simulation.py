from autonav_sim.grid import GridMap
from autonav_sim.models import Cell
from autonav_sim.simulation import NavigationSimulation


def test_simulation_reaches_goal_without_collision():
    grid = GridMap(12, 10)
    grid.clear_obstacles()
    grid.start, grid.goal = Cell(1, 1), Cell(9, 8)
    sim = NavigationSimulation(grid)
    sim.toggle_pause()
    for _ in range(100):
        sim.tick()
        if sim.status == "ARRIVED":
            break
    assert sim.status == "ARRIVED"
    assert sim.robot == grid.goal
    assert sim.metrics.collision_count == 0
    assert sim.metrics.travelled_steps == sim.result.steps


def test_replan_after_obstacle_edit():
    grid = GridMap(12, 10)
    grid.clear_obstacles()
    grid.start, grid.goal = Cell(1, 1), Cell(9, 8)
    sim = NavigationSimulation(grid)
    grid.toggle_obstacle(Cell(2, 1))
    sim.replan()
    assert sim.result.found
    assert all(grid.is_free(cell) for cell in sim.result.path)
