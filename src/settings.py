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
TITLE = "Portfolio Game - Eng. de Software"
FPS = 60

# --- Paleta de Cores (Modern Dark Theme) ---
# Usar dicionário facilita a troca de temas depois
COLORS = {
    "background": "#1e1e2e",  # Dark Blue/Grey
    "text": "#cdd6f4",  # Soft White
    "player": "#a6e3a1",  # Green
    "enemy": "#f38ba8",  # Red
    "ui_border": "#fab387",  # Orange
}

# --- Configurações de Debug ---
DEBUG_MODE = True  # Mostra hitboxes, FPS, etc.
