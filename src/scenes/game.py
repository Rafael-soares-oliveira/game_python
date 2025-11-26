import esper
import pygame

from src.core.components import Animation, PlayerTag, Sprite, Transform, Velocity
from src.core.scene import Scene
from src.core.systems import AnimationProcessor, MovementProcessor, RenderProcessor
from src.settings import COLORS, IMAGES_DIR, WINDOW_HEIGHT, WINDOW_WIDTH


class GameScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.world_name = "main_level"

        try:
            esper.switch_world(self.world_name)
            esper.delete_world(self.world_name)
        except (PermissionError, KeyError):
            pass

        # Configuração do Esper (World Context)
        esper.switch_world(self.world_name)

        self.camera = pygame.Vector2(0, 0)

        # Instancia e registra processadores
        self.movement_processor = MovementProcessor()
        self.animation_processor = AnimationProcessor()
        self.render_processor = RenderProcessor()

        esper.add_processor(self.movement_processor)
        esper.add_processor(self.animation_processor)
        esper.add_processor(self.render_processor)

        self.create_level()
        self.create_player()

    def on_enter(self):
        # Garante que o esper use este mundo ao voltar do menu
        esper.switch_world(self.world_name)

    def load_spritesheet(self, filename: str, frame_width: int, frame_height: int):
        """
        Carrega o PNG e recorta em frames individuais.

        Args:
            filename (str): _description_
            frame_width (int): _description_
            frame_height (int): _description_
        """
        path = IMAGES_DIR / filename

        sheet = pygame.image.load(path).convert_alpha()

        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()

        # Validação 1: A altura do frame não pode ser maior que a imagem
        if frame_height > sheet_height:
            raise ValueError(
                f"Erro: Frame altura ({frame_height}) maior que ({sheet_height})."
            )

        frames = []

        # Loop seguro
        for x in range(0, sheet_width, frame_width):
            # Validação 2: Se o próximo corte for passar do final da imagem, para.
            if x + frame_width > sheet_width:
                break

            frame = sheet.subsurface((x, 0, frame_width, frame_height))
            frames.append(frame)

        if not frames:
            raise ValueError("Nenhum frame foi carregado! Verifique as dimensões.")

        return frames

    def create_player(self):
        frame_w = 48
        frame_h = 48
        filename = "Main Ship - Base - Full health.png"
        anim_speed = 0.1

        try:
            frames_player = self.load_spritesheet(filename, frame_w, frame_h)
        except FileNotFoundError:
            s = pygame.Surface((frame_w, frame_h))
            s.fill((255, 0, 255))
            frames_player = [s]

        player = esper.create_entity()

        # Posição e Física
        esper.add_component(player, Transform(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        esper.add_component(player, Velocity(0, 0))
        esper.add_component(player, PlayerTag())

        # Visual e Animação
        esper.add_component(player, Sprite(image=frames_player[0], layer=2))
        esper.add_component(
            player, Animation(frames=frames_player, frame_duration=anim_speed)
        )

    def create_level(self):
        # 1. Carregar a imagem do disco
        bg_path = IMAGES_DIR / "background.png"

        try:
            bg_surf = pygame.image.load(bg_path).convert()
            bg_surf = pygame.transform.scale(bg_surf, (WINDOW_WIDTH, WINDOW_HEIGHT))

        except FileNotFoundError:
            bg_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            bg_surf.fill((20, 20, 30))

        # 2. Criar a Entidade de Fundo no ECS
        background = esper.create_entity()

        # Posição 0,0 - Superior esquerdo
        esper.add_component(background, Transform(0, 0))

        # Layer 0 (Fundo): Garante que será desenhado antes da nave
        esper.add_component(background, Sprite(image=bg_surf, layer=0))

    def process_input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            # ENTER: Pausa o Jogo (Push na pilha)
            if event.key == pygame.K_RETURN:
                from src.scenes.pause import PauseScene

                self.manager.push(PauseScene)

            # ESC: Volta direto pro Menu (Reset)
            elif event.key == pygame.K_ESCAPE:
                from src.scenes.menu import MenuScene

                self.manager.switch_to(MenuScene)

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            self._update_velocity()

    def _update_velocity(self):
        keys = pygame.key.get_pressed()
        speed = 500
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * speed
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * speed

        for ent, (vel, _) in esper.get_components(Velocity, PlayerTag):
            vel.x, vel.y = dx, dy

    def update(self, dt: float):
        esper.switch_world(self.world_name)

        # 1. Física
        self.movement_processor.process(dt)
        # 2. Aplica Restrições
        self._constrain_player_bounds()
        # 3. Animação (Troca os frames da nave)
        self.animation_processor.process(dt)

    def _constrain_player_bounds(self):
        """Impede que o jogador saia da área visível da janela."""
        # Busca Transform e Sprite (para saber a largura da nave)
        for ent, (trans, sprite) in esper.get_components(Transform, Sprite):
            # Aplica apenas ao Jogador (checando se tem a tag PlayerTag)
            if esper.has_component(ent, PlayerTag):
                # Largura/Altura da imagem (assumindo que sprite.image existe)
                # Se usou nosso Sprite component, ele tem .width e .height no post_init,
                # mas vamos pegar direto da imagem para garantir.
                w = sprite.image.get_width()
                h = sprite.image.get_height()

                # Clamping (Travar valores)

                # EIXO X: Entre 0 e (Largura da Tela - Largura da Nave)
                if trans.x < 0:
                    trans.x = 0
                elif trans.x > WINDOW_WIDTH - w:
                    trans.x = WINDOW_WIDTH - w

                # EIXO Y: Entre 0 e (Altura da Tela - Altura da Nave)
                if trans.y < 0:
                    trans.y = 0
                elif trans.y > WINDOW_HEIGHT - h:
                    trans.y = WINDOW_HEIGHT - h

    def draw(self):
        self.display.fill(COLORS["background"])

        # Renderização ECS com Câmera
        ctx = {"camera": (self.camera.x, self.camera.y)}
        self.render_processor.process(context=ctx)

        # UI Fixa
        if pygame.font.get_init():
            f = pygame.font.SysFont("arial", 18)
            self.display.blit(
                f.render("WASD: Mover | ENTER: Pause | ESC: Menu", True, "white"),
                (10, 10),
            )
