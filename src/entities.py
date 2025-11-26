import math
import random

import esper
import pygame

from src.core.components import (
    Animation,
    EnemyProjectile,
    EnemyTag,
    Gun,
    Health,
    Invincibility,
    MovePattern,
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
    PATTERN_0_SPEED,
    PATTERN_1_SPEED,
    PATTERN_2_SPEED,
    PATTERN_3_SPEED,
    PLAYER_GUN_COOLDOWN,
    PLAYER_START_DELAY,
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
    esper.add_component(
        player, Gun(cooldown=PLAYER_GUN_COOLDOWN, start_delay=PLAYER_START_DELAY)
    )


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


def create_enemy_bullet(world_name, x, y, pattern_type, angle, speed, freq=5.0):
    """Cria um único projétil inimigo com padrão matemático."""
    esper.switch_world(world_name)

    w, h = 8, 8
    surf = pygame.Surface((w, h))
    surf.fill("#ffff00")  # Amarelo

    bullet = esper.create_entity()

    # Nota: A posição será controlada pelo MovePattern, mas inicializamos o Transform
    esper.add_component(bullet, Transform(x, y))
    # Velocity zerada pois o MovePattern controla tudo
    esper.add_component(bullet, Velocity(0, 0))
    esper.add_component(bullet, Sprite(surf, layer=1))
    esper.add_component(bullet, EnemyProjectile(damage=10))

    # Componente matemático
    esper.add_component(
        bullet,
        MovePattern(
            pattern_type=pattern_type,
            start_x=x,
            start_y=y,
            angle=angle,
            speed=speed,
            frequency=freq,
            amplitude=30.0,  # Largura do zig-zag
        ),
    )


def spawn_enemy_pattern(world_name, enemy_x, enemy_y, pattern_idx):
    """Gerencia qual 'golpe' o inimigo vai usar."""

    # Padrão 0: Leque Simples (Fan)
    if pattern_idx == 0:
        angles = [60, 75, 90, 105, 120]  # Graus (90 é para baixo)
        for deg in angles:
            rad = math.radians(deg)
            speed = random.uniform(PATTERN_0_SPEED[0], PATTERN_0_SPEED[1])
            create_enemy_bullet(
                world_name, enemy_x, enemy_y, "linear", rad, speed=speed, freq=5
            )

    # Padrão 1: Zig-Zag Circular (360 graus)
    elif pattern_idx == 1:
        for deg in range(0, 360, 45):  # 8 direções
            rad = math.radians(deg)
            speed = random.uniform(PATTERN_1_SPEED[0], PATTERN_1_SPEED[1])
            create_enemy_bullet(
                world_name, enemy_x, enemy_y, "sine", rad, speed=speed, freq=5.0
            )

    # Padrão 2: Leque Zig-Zag (Wavy Fan)
    elif pattern_idx == 2:
        angles = [70, 80, 90, 100, 110]
        for deg in angles:
            rad = math.radians(deg)
            speed = random.uniform(PATTERN_2_SPEED[0], PATTERN_2_SPEED[1])
            create_enemy_bullet(
                world_name, enemy_x, enemy_y, "sine", rad, speed=speed, freq=3.0
            )

    # Padrão 3: Espiral Louca
    elif pattern_idx == 3:
        # Cria 4 braços de espiral
        for deg in [0, 90, 180, 270]:
            rad = math.radians(deg)
            speed = random.uniform(PATTERN_3_SPEED[0], PATTERN_3_SPEED[1])
            create_enemy_bullet(
                world_name, enemy_x, enemy_y, "spiral", rad, speed=speed, freq=1.0
            )
