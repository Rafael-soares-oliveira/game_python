import pygame

from src.settings import IMAGES_DIR


def load_spritesheet(
    filename: str, frame_height: int, frame_width: int = 0, num_frames: int = 0
) -> list[pygame.Surface]:
    """
    Carrega PNG e recorta em frames.

    Modo 1: Passar frame_width (recorta baseado no tamanho).
    Modo 2: Passar num_frames (calcula o tamanho baseado na quantidade).
    """
    path = IMAGES_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Asset não encontrado: {path}")

    sheet = pygame.image.load(path).convert_alpha()
    sheet_width = sheet.get_width()

    # Lógica Inteligente: Calcula largura se num_frames foi passado
    if num_frames > 0:
        frame_width = sheet_width // num_frames

    # Validação de Segurança
    if frame_width == 0:
        raise ValueError("Você deve fornecer frame_width OU num_frames!")

    frames = []
    for x in range(0, sheet_width, frame_width):
        # Proteção para não pegar frame vazio no final
        if x + frame_width > sheet_width:
            break

        frame = sheet.subsurface((x, 0, frame_width, frame_height))
        frames.append(frame)

    # Se pediu uma quantidade exata, garante que retorna apenas ela
    if num_frames > 0:
        frames = frames[:num_frames]

    if not frames:
        raise ValueError("Nenhum frame carregado.")

    return frames
