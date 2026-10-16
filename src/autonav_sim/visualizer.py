from pathlib import Path
import pygame

from .models import Cell
from .simulation import NavigationSimulation

CELL, MARGIN, TOP, PANEL = 28, 18, 76, 270
BG, GRID_LINE, OBSTACLE = (245, 247, 250), (216, 222, 230), (54, 63, 75)
PATH, START, GOAL, ROBOT = (68, 135, 220), (46, 160, 100), (220, 75, 75), (255, 190, 45)
TEXT, MUTED = (35, 43, 54), (95, 106, 120)


class Visualizer:
    def __init__(self, sim: NavigationSimulation):
        pygame.init()
        self.sim = sim
        self.screen = pygame.display.set_mode(
            (MARGIN * 2 + sim.grid.width * CELL + PANEL,
             TOP + MARGIN + sim.grid.height * CELL + MARGIN))
        pygame.display.set_caption("AI-Based Autonomous Navigation System")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("segoeui", 18)
        self.small = pygame.font.SysFont("segoeui", 14)
        self.title = pygame.font.SysFont("segoeui", 23, bold=True)
        self.running, self.accumulator, self.step_interval = True, 0.0, 0.14

    def cell_rect(self, cell):
        return pygame.Rect(MARGIN + cell.x * CELL, TOP + cell.y * CELL, CELL, CELL)

    def text(self, value, x, y, font=None, color=TEXT):
        self.screen.blit((font or self.font).render(value, True, color), (x, y))

    def draw(self):
        self.screen.fill(BG)
        self.text("AI-Based Autonomous Navigation", MARGIN, 20, self.title)
        self.text("A* path planning  |  Grid-world simulation", MARGIN, 49, self.small, MUTED)
        grid_rect = pygame.Rect(MARGIN, TOP, self.sim.grid.width * CELL, self.sim.grid.height * CELL)
        pygame.draw.rect(self.screen, (255, 255, 255), grid_rect)
        for cell in self.sim.grid.obstacles:
            pygame.draw.rect(self.screen, OBSTACLE, self.cell_rect(cell).inflate(-2, -2), border_radius=3)
        if self.sim.result.found:
            for cell in self.sim.result.path[1:]:
                pygame.draw.rect(self.screen, PATH, self.cell_rect(cell).inflate(-8, -8), border_radius=4)
        for x in range(self.sim.grid.width + 1):
            px = MARGIN + x * CELL
            pygame.draw.line(self.screen, GRID_LINE, (px, TOP), (px, TOP + self.sim.grid.height * CELL))
        for y in range(self.sim.grid.height + 1):
            py = TOP + y * CELL
            pygame.draw.line(self.screen, GRID_LINE, (MARGIN, py), (MARGIN + self.sim.grid.width * CELL, py))
        pygame.draw.rect(self.screen, START, self.cell_rect(self.sim.grid.start).inflate(-5, -5), border_radius=6)
        pygame.draw.rect(self.screen, GOAL, self.cell_rect(self.sim.grid.goal).inflate(-5, -5), border_radius=6)
        pygame.draw.circle(self.screen, ROBOT, self.cell_rect(self.sim.robot).center, CELL // 3)
        pygame.draw.circle(self.screen, (110, 82, 15), self.cell_rect(self.sim.robot).center, CELL // 3, 2)

        px, y = MARGIN * 2 + self.sim.grid.width * CELL, TOP + 3
        self.text("NAVIGATION STATUS", px, y); y += 34
        self.text(self.sim.status, px, y, self.title, START if self.sim.status == "ARRIVED" else TEXT); y += 45
        stats = [
            ("Planned steps", str(self.sim.result.steps if self.sim.result.found else "—")),
            ("Travelled steps", str(self.sim.metrics.travelled_steps)),
            ("Expanded nodes", str(self.sim.result.expanded_nodes)),
            ("Obstacles", str(len(self.sim.grid.obstacles))),
            ("Collision events", str(self.sim.metrics.collision_count)),
            ("Elapsed", f"{self.sim.elapsed():.1f} s"),
        ]
        for label, value in stats:
            self.text(label, px, y, self.small, MUTED)
            self.text(value, px + 145, y)
            y += 31
        y += 12
        self.text("CONTROLS", px, y); y += 30
        for line in ["SPACE  Start / pause", "R      Reset robot", "P      Re-plan route",
                     "Click  Toggle obstacle", "S      Save screenshot", "ESC    Quit"]:
            self.text(line, px, y, self.small, MUTED); y += 24
        y += 14
        self.text("EDITING MAP", px, y); y += 27
        self.text("Click a cell to pause and edit.", px, y, self.small, MUTED); y += 20
        self.text("Press P to plan around changes.", px, y, self.small, MUTED)
        pygame.display.flip()

    def save_screenshot(self):
        out = Path("artifacts")
        out.mkdir(exist_ok=True)
        path = out / "simulation.png"
        pygame.image.save(self.screen, str(path))
        return path

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_SPACE:
                self.sim.toggle_pause()
            elif event.key == pygame.K_r:
                self.sim.reset()
            elif event.key == pygame.K_p:
                self.sim.replan()
            elif event.key == pygame.K_s:
                print(f"Screenshot saved to {self.save_screenshot()}")
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            cell = Cell(int((mx - MARGIN) // CELL), int((my - TOP) // CELL))
            if self.sim.grid.in_bounds(cell):
                self.sim.paused, self.sim.status = True, "PAUSED"
                self.sim.grid.toggle_obstacle(cell)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                self.handle_event(event)
            if not self.sim.paused and self.sim.status == "RUNNING":
                self.accumulator += dt
                while self.accumulator >= self.step_interval:
                    self.sim.tick()
                    self.accumulator -= self.step_interval
            self.draw()
        pygame.quit()
