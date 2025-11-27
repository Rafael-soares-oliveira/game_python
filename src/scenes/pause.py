import pygame

from src.core.scene import Scene, SceneManager
from src.settings import COLORS, WINDOW_HEIGHT, WINDOW_WIDTH


class PauseScene(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager)
        self.font_title = pygame.font.SysFont("arial", 60, bold=True)
        self.font_option = pygame.font.SysFont("arial", 30)

        # Cria uma superfície preta semi-transparente para o overlay
        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(150)  # 0 = invisível, 255 = opaco

    def process_input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.manager.pop()

            elif event.key == pygame.K_ESCAPE:
                from src.scenes.menu import MenuScene

                self.manager.switch_to(MenuScene)

    def update(self, dt: float):
        pass

    def draw(self):
        # 1. Desenha o fundo escuro sobre a cena anterior (Jogo)
        self.display.blit(self.overlay, (0, 0))

        # 2. Textos Centralizados
        text_paused = self.font_title.render("JOGO PAUSADO", True, COLORS["ui_border"])
        rect_paused = text_paused.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50)
        )

        text_resume = self.font_option.render("ENTER: Continuar", True, COLORS["text"])
        rect_resume = text_resume.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 20)
        )

        text_menu = self.font_option.render("ESC: Menu Principal", True, COLORS["text"])
        rect_menu = text_menu.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 60)
        )

        self.display.blit(text_paused, rect_paused)
        self.display.blit(text_resume, rect_resume)
        self.display.blit(text_menu, rect_menu)
