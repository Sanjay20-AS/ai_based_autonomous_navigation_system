from .models import Cell


class GridMap:
    """Rectangular grid where True cells are blocked."""

    def __init__(self, width: int = 30, height: int = 20):
        if width < 2 or height < 2:
            raise ValueError("Grid width and height must both be at least 2.")
        self.width, self.height = width, height
        self.obstacles: set[Cell] = set()
        self.start = Cell(2, 2)
        self.goal = Cell(width - 3, height - 3)
        self._add_demo_obstacles()

    def _add_demo_obstacles(self):
        for y in range(2, self.height - 3):
            if y not in (6, 7):
                self.obstacles.add(Cell(self.width // 3, y))
        for y in range(4, self.height - 2):
            if y not in (11, 12):
                self.obstacles.add(Cell((2 * self.width) // 3, y))
        for x in range(self.width // 2 - 2, self.width // 2 + 2):
            for y in range(self.height // 2 - 1, self.height // 2 + 2):
                self.obstacles.add(Cell(x, y))
        self.obstacles.discard(self.start)
        self.obstacles.discard(self.goal)

    def in_bounds(self, cell: Cell) -> bool:
        return 0 <= cell.x < self.width and 0 <= cell.y < self.height

    def is_free(self, cell: Cell) -> bool:
        return self.in_bounds(cell) and cell not in self.obstacles

    def neighbors(self, cell: Cell) -> list[Cell]:
        candidates = (Cell(cell.x + 1, cell.y), Cell(cell.x - 1, cell.y),
                      Cell(cell.x, cell.y + 1), Cell(cell.x, cell.y - 1))
        return [candidate for candidate in candidates if self.is_free(candidate)]

    def toggle_obstacle(self, cell: Cell) -> bool:
        if not self.in_bounds(cell) or cell in (self.start, self.goal):
            return False
        if cell in self.obstacles:
            self.obstacles.remove(cell)
        else:
            self.obstacles.add(cell)
        return True

    def clear_obstacles(self):
        self.obstacles.clear()
