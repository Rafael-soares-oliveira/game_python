import pygame

from src.core.scene import Scene, SceneManager
from src.settings import WINDOW_HEIGHT, WINDOW_WIDTH


class VictoryScene(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager)
        self.font_big = pygame.font.SysFont("arial", 50, bold=True)
        self.font_small = pygame.font.SysFont("arial", 20)

    def process_input(self, event: pygame.Event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                from src.scenes.menu import MenuScene

                self.manager.switch_to(MenuScene)

    def update(self, dt: float):
        pass

    def draw(self):
        # TODO: Alterar tela vitória
        self.display.fill((0, 40, 0))

        # Texto VITÓRIA
        text_win = self.font_big.render("MISSÃO CUMPRIDA", True, (50, 255, 50))
        rect_win = text_win.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))

        # Opções
        text_menu = self.font_small.render(
            "Pressione ENTER para Voltar ao Menu", True, (200, 255, 200)
        )
        rect_menu = text_menu.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50)
        )

        self.display.blit(text_win, rect_win)
        self.display.blit(text_menu, rect_menu)
