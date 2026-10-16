from .models import Cell


class WaypointController:
    """Moves one grid cell at a time along the planned route."""

    def __init__(self, path: list[Cell]):
        self.path = path
        self.index = 0

    @property
    def finished(self) -> bool:
        return not self.path or self.index >= len(self.path) - 1

    @property
    def current(self) -> Cell | None:
        return self.path[self.index] if self.path else None

    def step(self) -> Cell | None:
        if not self.finished:
            self.index += 1
        return self.current
