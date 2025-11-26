import esper
import pygame

from src.core.components import (
    Animation,
    EnemyTag,
    Gun,
    Health,
    Invincibility,
    PlayerTag,
    Projectile,
    Sprite,
    Transform,
    Velocity,
)
from src.settings import (
    COLORS,
    ENEMY_HP,
    IMAGES_DIR,
    LASER_DAMAGE,
    LASER_SPEED,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.utils import load_spritesheet


def create_player(world_name):
    esper.switch_world(world_name)

    filename = "Main Ship - Base - Full health.png"
    # Player geralmente tem tamanho fixo, mantemos assim
    w, h = 48, 48

    try:
        frames = load_spritesheet(filename, frame_height=h, frame_width=w)
    except FileNotFoundError:
        s = pygame.Surface((w, h))
        s.fill(COLORS["player"])
        frames = [s]

    player = esper.create_entity()
    spawn_x = (WINDOW_WIDTH // 2) - (w // 2)
    spawn_y = WINDOW_HEIGHT - 100

    esper.add_component(player, Transform(spawn_x, spawn_y))
    esper.add_component(player, Velocity(0, 0))
    esper.add_component(player, PlayerTag())
    esper.add_component(player, Sprite(frames[0], layer=2))
    # Velocidade fixa para o player
    esper.add_component(player, Animation(frames, 0.1))
    esper.add_component(player, Invincibility(duration=2.0))
    esper.add_component(player, Health(100, 100))
    esper.add_component(player, Gun())


def create_enemy(world_name):
    esper.switch_world(world_name)

    filename = "enemy.png"

    # --- CONTROLE TOTAL DA ANIMAÇÃO ---
    num_frames = 4  # Quantidade de sprites na imagem
    anim_speed = 0.2  # Velocidade da troca (0.2 = mais lento, 0.1 = rápido)
    scale = 2  # Tamanho final
    h_orig = 64  # Altura original da imagem (necessário saber)
    # ----------------------------------

    try:
        # Modo Inteligente: Passamos num_frames, ele calcula a largura sozinho
        raw_frames = load_spritesheet(
            filename, frame_height=h_orig, num_frames=num_frames
        )

        # Escala os frames retornados
        frames = []
        for f in raw_frames:
            w = f.get_width()
            h = f.get_height()
            scaled = pygame.transform.scale(f, (w * scale, h * scale))
            frames.append(scaled)

    except FileNotFoundError:
        s = pygame.Surface((64, 64))
        s.fill(COLORS["enemy"])
        frames = [s]

    final_w = frames[0].get_width()

    enemy = esper.create_entity()
    spawn_x = (WINDOW_WIDTH // 2) - (final_w // 2)

    esper.add_component(enemy, Transform(spawn_x, 30))
    esper.add_component(enemy, Velocity(0, 0))
    esper.add_component(enemy, EnemyTag())
    esper.add_component(enemy, Sprite(frames[0], layer=2))

    # AQUI ESTÁ O CONTROLE: Passamos a variável anim_speed
    esper.add_component(enemy, Animation(frames, anim_speed))
    esper.add_component(enemy, Health(ENEMY_HP, ENEMY_HP))


def create_laser(world_name, player_pos: Transform, player_sprite: Sprite):
    esper.switch_world(world_name)

    w, h = 4, 10
    surf = pygame.Surface((w, h))
    surf.fill(COLORS["laser"])

    laser = esper.create_entity()
    spawn_x = player_pos.x + (player_sprite.width // 2) - (w // 2)
    spawn_y = player_pos.y - h

    esper.add_component(laser, Transform(spawn_x, spawn_y))
    esper.add_component(laser, Velocity(0, LASER_SPEED))
    esper.add_component(laser, Sprite(surf, layer=1))
    esper.add_component(laser, Projectile(damage=LASER_DAMAGE))


def create_bg(world_name):
    esper.switch_world(world_name)

    try:
        bg = pygame.image.load(IMAGES_DIR / "background.png").convert()
        bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    except Exception:
        bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        bg.fill("#111122")

    ent = esper.create_entity()
    esper.add_component(ent, Transform(0, 0))
    esper.add_component(ent, Sprite(bg, layer=0))
