from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Cell:
    # x is column, y is row
    x: int
    y: int


@dataclass
class PlanResult:
    path: list[Cell]
    expanded_nodes: int
    found: bool
    cost: float = 0.0
    message: str = ""

    @property
    def steps(self) -> int:
        return max(0, len(self.path) - 1)
