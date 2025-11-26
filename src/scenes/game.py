import time

import esper
import pygame

from src.core.components import (
    EnemyTag,
    Gun,
    Health,
    PlayerTag,
    Projectile,
    Sprite,
    Transform,
    Velocity,
)
from src.core.scene import Scene
from src.core.systems import (
    AnimationProcessor,
    CollisionProcessor,
    MovementProcessor,
    RenderProcessor,
)

# Importamos as fábricas
from src.entities import create_bg, create_enemy, create_laser, create_player
from src.settings import COLORS, PLAYER_SPEED, WINDOW_HEIGHT, WINDOW_WIDTH


class GameScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)

        # ID Único para evitar conflito de mundos
        self.world_name = f"level_{time.time()}"
        esper.switch_world(self.world_name)

        # Limpeza preventiva
        try:
            esper.clear_database()
        except Exception:
            pass

        self.camera = pygame.Vector2(0, 0)
        self._init_systems()
        self._init_level()

    def _init_systems(self):
        """Registra os processadores."""
        self.movement_processor = MovementProcessor()
        self.animation_processor = AnimationProcessor()
        self.collision_processor = CollisionProcessor()
        self.render_processor = RenderProcessor(self.camera)

        esper.add_processor(self.movement_processor)
        esper.add_processor(self.animation_processor)
        esper.add_processor(self.collision_processor)
        esper.add_processor(self.render_processor)

    def _init_level(self):
        """Cria as entidades iniciais."""
        create_bg(self.world_name)
        create_player(self.world_name)
        create_enemy(self.world_name)

    def on_enter(self):
        esper.switch_world(self.world_name)

    def process_input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from src.scenes.pause import PauseScene

                self.manager.push(PauseScene)
            elif event.key == pygame.K_ESCAPE:
                from src.scenes.menu import MenuScene

                self.manager.switch_to(MenuScene)

        # Input contínuo de movimento é tratado no update para suavidade,
        # mas aqui podemos setar flags se quisermos.

    def update(self, dt: float):
        esper.switch_world(self.world_name)

        # 1. Inputs de Gameplay (Tiro e Movimento)
        self._handle_input(dt)

        # 2. Limpeza
        self._cleanup_projectiles()

        # 3. ECS Process
        self.movement_processor.process(dt)
        self._constrain_player()
        self.animation_processor.process(dt)
        self.collision_processor.process(dt)

        # 4. Checagem de Estados
        self._check_game_over()
        self._check_victory()

    def _handle_input(self, dt):
        keys = pygame.key.get_pressed()

        # Movimento
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * PLAYER_SPEED
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * PLAYER_SPEED

        for ent, (vel, _) in esper.get_components(Velocity, PlayerTag):
            vel.x, vel.y = dx, dy

        # Tiro
        if keys[pygame.K_SPACE]:
            for ent, (gun, trans, sprite, _) in esper.get_components(
                Gun, Transform, Sprite, PlayerTag
            ):
                if gun.timer > 0:
                    gun.timer -= dt
                else:
                    create_laser(self.world_name, trans, sprite)
                    gun.timer = gun.cooldown
        else:
            # Resfria a arma mesmo sem atirar
            for ent, (gun, _) in esper.get_components(Gun, PlayerTag):
                if gun.timer > 0:
                    gun.timer -= dt

    def _cleanup_projectiles(self):
        for ent, (trans, _) in esper.get_components(Transform, Projectile):
            if trans.y < -50:
                esper.delete_entity(ent)

    def _constrain_player(self):
        for ent, (trans, sprite, _) in esper.get_components(
            Transform, Sprite, PlayerTag
        ):
            w, h = sprite.width, sprite.height
            if trans.x < 0:
                trans.x = 0
            elif trans.x > WINDOW_WIDTH - w:
                trans.x = WINDOW_WIDTH - w
            if trans.y < 0:
                trans.y = 0
            elif trans.y > WINDOW_HEIGHT - h:
                trans.y = WINDOW_HEIGHT - h

    def _check_game_over(self):
        for ent, (hp, _) in esper.get_components(Health, PlayerTag):
            if hp.current <= 0:
                from src.scenes.game_over import GameOverScene

                self.manager.switch_to(GameOverScene)

    def _check_victory(self):
        # Coleta entidades marcadas como inimigo de forma segura
        enemies_alive = [ent for ent, _ in esper.get_component(EnemyTag)]

        # Filtra apenas entidades que ainda existem (evita 'fantasmas')
        enemies_alive = [e for e in enemies_alive if esper.entity_exists(e)]

        if len(enemies_alive) == 0:
            from src.scenes.victory import VictoryScene

            self.manager.switch_to(VictoryScene)

    def draw(self):
        self.display.fill(COLORS["background"])

        ctx = {"camera": (self.camera.x, self.camera.y)}
        self.render_processor.process(context=ctx)

        self._draw_enemy_hp()
        self._draw_ui()

    def _draw_enemy_hp(self):
        """Desenha uma barra de vida pequena sobre cada inimigo."""
        for ent, (trans, sprite, health, _) in esper.get_components(
            Transform, Sprite, Health, EnemyTag
        ):
            # Configuração da Barrinha
            w = sprite.width
            h = 5
            x = trans.x - self.camera.x
            y = trans.y - self.camera.y - 10  # 10px acima da cabeça

            # Fundo Vermelho Escuro
            bg_rect = pygame.Rect(x, y, w, h)
            pygame.draw.rect(self.display, (50, 0, 0), bg_rect)

            # Frente Vermelho Claro
            pct = health.get_percentage()
            fill_rect = pygame.Rect(x, y, int(w * pct), h)
            pygame.draw.rect(self.display, (255, 0, 0), fill_rect)

    def _draw_ui(self):
        # 1. Busca os dados de vida do Player
        player_health = None
        for ent, (health, tag) in esper.get_components(Health, PlayerTag):
            player_health = health
            break

        if not player_health:
            return

        # 2. Configurações da Barra
        bar_width = 200
        bar_height = 20
        x = 20
        y = 20

        # 3. Desenho Matemático
        bg_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(self.display, COLORS["ui_bg"], bg_rect)

        fill_width = int(bar_width * player_health.get_percentage())
        fill_rect = pygame.Rect(x, y, fill_width, bar_height)
        pygame.draw.rect(self.display, COLORS["ui_fill"], fill_rect)

        pygame.draw.rect(self.display, COLORS["ui_border"], bg_rect, width=3)

        # 4. Texto
        if pygame.font.get_init():
            f = pygame.font.SysFont("arial", 14, bold=True)
            txt = f.render(
                f"HP: {player_health.current}/{player_health.maximum}",
                True,
                COLORS["text"],
            )
            self.display.blit(txt, (x + 10, y + 2))
