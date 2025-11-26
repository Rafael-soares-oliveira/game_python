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


@dataclass
class EnemyTag:
    """Identifica entidades que são inimigos."""

    pass


@dataclass
class Invincibility:
    """Controla o estado de dano/invunerabilidade."""

    duration: float = 2.0  # Tempo total invencível (segundos)
    timer: float = 0.0  # Cronômetro regressivo
    is_active: bool = False  # Está invencível agora?
    blink_interval: float = 0.1  # Velocidade da piscada


@dataclass
class Health:
    current: int
    maximum: int

    def get_percentage(self) -> float:
        """Retorna valor entre 0.0 e 1.0"""
        if self.maximum == 0:
            return 0.0
        return max(0.0, min(1.0, self.current / self.maximum))


@dataclass
class Projectile:
    """Marcar a entidade como um tiro e guardar quanto dano ela causa."""

    damage: int = 10


@dataclass
class Gun:
    """Anexar ao player e controlar o tempo entre disparos."""

    cooldown: float = 0.2  # Tempo mínimo entre tiros
    timer: float = 0.0  # Cronômetro interno
    start_delay: float = 0.0  # Cronômetro para começar a atirar


@dataclass
class EnemyProjectile:
    """Lasers do inimigo."""

    damage: int = 10


@dataclass
class MovePattern:
    """Padrão de movimento dos lasers."""

    pattern_type: str = "linear"
    start_x: float = 0.0
    start_y: float = 0.0
    time: float = 0.0

    # Parâmetros matemáticos
    speed: float = 200.0  # Velocidade base
    angle: float = 0.0  # Ângulo base (radianos)
    amplitude: float = 50.0  # Largura do zig-zag
    frequency: float = 5.0  # Velocidade do zig-zag
