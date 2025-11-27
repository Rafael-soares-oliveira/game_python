import pygame

from src.core.scene import Scene, SceneManager
from src.settings import COLORS, WINDOW_HEIGHT, WINDOW_WIDTH


class MenuScene(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager)
        self.title_font = pygame.font.SysFont("arial", 50, bold=True)
        self.font = pygame.font.SysFont("arial", 24)
        self.blink_timer = 1

    def process_input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from src.scenes.game import GameScene

                self.manager.switch_to(GameScene)

    def update(self, dt: float):
        self.blink_timer += dt * 3

    def draw(self):
        self.display.fill(COLORS["background"])

        # Título
        title = self.title_font.render("SHOOTER PYTHON", True, COLORS["ui_border"])
        title_rect = title.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3))
        self.display.blit(title, title_rect)

        # Texto Piscante
        if int(self.blink_timer) % 2 == 0:
            msg = self.font.render("Pressione ENTER para Iniciar", True, COLORS["text"])
            msg_rect = msg.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            self.display.blit(msg, msg_rect)
