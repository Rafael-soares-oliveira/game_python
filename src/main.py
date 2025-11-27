import asyncio

import pygame

from src.core.scene import SceneManager
from src.scenes.menu import MenuScene
from src.settings import FPS, TITLE, WINDOW_HEIGHT, WINDOW_WIDTH


async def main():
    # 1. Setup Inicial
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # 2. Inicializa Gerenciador e Cena Inicial
    # (Importante: Display já existe aqui, então SceneManager não vai dar erro)
    manager = SceneManager()
    manager.switch_to(MenuScene)

    running = True
    while running:
        # Calcular Delta Time em segundos (essencial para física estável)
        dt = clock.tick(FPS) / 1000.0

        # 3. Processamento de Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Delega inputs (cliques, teclas) para a cena ativa
            manager.process_input(event)

        # 4. Update e Draw
        # O manager chama update(dt) na cena atual e draw() em todas (pilha)
        manager.run(dt)

        # 5. Flip e Controle de Async (Web)
        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()
