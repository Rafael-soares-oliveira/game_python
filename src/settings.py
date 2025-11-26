from pathlib import Path

# --- Engenharia de Caminhos (Path Management) ---
# Resolve o caminho absoluto base para funcionar local e na web
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
FONTS_DIR = ASSETS_DIR / "fonts"

# --- Configurações de Display ---
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
TITLE = "SPACE SHOOTER"
FPS = 60

# --- Paleta de Cores (Modern Dark Theme) ---
# Usar dicionário facilita a troca de temas depois
COLORS = {
    "background": "#1e1e2e",  # Dark Blue/Grey
    "text": "#000000",  # Black
    "player": "#a6e3a1",  # Green
    "enemy": "#f38ba8",  # Red
    "ui_border": "#fab387",  # Orange
    "laser": "#ff3232",
    "ui_bg": "#140000",
    "ui_fill": "#00ffff",
}

# GAMEPLAY
PLAYER_SPEED = 500
PLAYER_HP = 100
PLAYER_GUN_COOLDOWN = 0.2
PLAYER_INVINCIBILITY = 2.0
PLAYER_START_DELAY = 2.0

LASER_SPEED = -600
LASER_DAMAGE = 5

ENEMY_HP = 200
ENEMY_SHOOT_COOLDOWN = 0.5

# Padrões de tipo do inimigo (velocidade min/max)
# Padrão 0: Leque linear
PATTERN_0_SPEED = (100, 250)

# Padrão 1: Círculo Zig-Zag
PATTERN_1_SPEED = (50, 150)

# Padrão 2: Leque Ondulado
PATTERN_2_SPEED = (180, 280)

# Padrão 3: Espiral
PATTERN_3_SPEED = (80, 120)

# --- Configurações de Debug ---
DEBUG_MODE = True  # Mostra hitboxes, FPS, etc.
