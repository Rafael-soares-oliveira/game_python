import asyncio

import pygame

# TODO: Configurações iniciais, mover para settings.py
WIDTH, HEIGHT = 1280, 720
FPS = 60


async def main():
    """Ponto de entrada principal do jogo (Entrypoint)"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Portfolio Game - Eng. de Software")
    clock = pygame.time.Clock()

    running = True

    while running:
        # 1. Processamento de Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. Atualização de Lógica (Update)
        # TODO: Aqui entrará o world.process() do ECS depois

        # 3. Renderização (Draw)
        screen.fill("black")  # Limpar a tela

        # Exemplo de texto para confirmar que funcionou
        font = pygame.font.SysFont("arial", 36)
        text = font.render("Engenharia de Software + Game Dev", True, "white")
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        # 4. Controle de FPS e await para Web (Crítico para Pybag)
        clock.tick(FPS)
        await asyncio.sleep(0)  # Libera o controle para o navegador não travar

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
