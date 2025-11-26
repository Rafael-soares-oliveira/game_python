from dataclasses import dataclass

import pygame


@dataclass
class Transform:
    """Representa a posição espacial."""

    x: float
    y: float


@dataclass
class Velocity:
    """Representa o vetor do movimento."""

    x: float = 0.0
    y: float = 0.0


@dataclass
class Sprite:
    """Representa a parte visual."""

    image: pygame.Surface
    layer: int = 0  # 0 = Fundo, 1 = Chão, 2 = Player, etc

    # Metadados úteis para colisão simples sem retângulos complexos
    def __post_init__(self):
        if self.image:
            self.width = self.image.get_width()
            self.height = self.image.get_height()


@dataclass
class Animation:
    """Guarda a lista de frames e o timer para troca."""

    frames: list[pygame.Surface]
    frame_duration: float = 0.1
    timer: float = 0.0
    current_index: int = 0


@dataclass
class PlayerTag:
    """Componente vazio (Tag) apenas para identificar quem é o jogador."""

    pass
