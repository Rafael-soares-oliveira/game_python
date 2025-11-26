import pygame

from src.core.scene import Scene, SceneManager
from src.settings import COLORS, WINDOW_HEIGHT, WINDOW_WIDTH


class GameOverScene(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager)
        self.font_big = pygame.font.SysFont("arial", 80, bold=True)
        self.font_small = pygame.font.SysFont("arial", 30)

    def process_input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            # ENTER: Reinicia o jogo
            if event.key == pygame.K_RETURN:
                from src.scenes.game import GameScene

                self.manager.switch_to(GameScene)

            # ESC: Volta ao Menu
            elif event.key == pygame.K_ESCAPE:
                from src.scenes.menu import MenuScene

                self.manager.switch_to(MenuScene)

    def update(self, dt: float):
        pass

    def draw(self):
        # Fundo
        self.display.fill((20, 0, 0))

        # Texto GAME OVER
        text_go = self.font_big.render("GAME OVER", True, (255, 50, 50))
        rect_go = text_go.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))

        # Opções
        text_restart = self.font_small.render(
            "Pressione ENTER para Tentar Novamente", True, COLORS["text"]
        )
        rect_restart = text_restart.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50)
        )

        text_menu = self.font_small.render(
            "ESC para Menu Principal", True, (150, 150, 150)
        )
        rect_menu = text_menu.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 90)
        )

        self.display.blit(text_go, rect_go)
        self.display.blit(text_restart, rect_restart)
        self.display.blit(text_menu, rect_menu)
