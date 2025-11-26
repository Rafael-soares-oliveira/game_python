import esper
import pygame

from src.core.components import Animation, Sprite, Transform, Velocity


class MovementProcessor(esper.Processor):
    """
    Atualiza a posição das entidades com Velocity.

    Espera que `dt` seja o delta time em segundos (float)

    Args:
        esper (Processor): Base class for all Processors to inherit from
    """

    def process(self, dt: float):
        """Atualiza transform.x/y com base em vel.x/y.

        Args:
            dt (float): tempo em segundos desde o último frame
        """
        # Itera apenas sobre entidades que têm Transform e Velocity.
        for ent, (transform, vel) in esper.get_components(Transform, Velocity):
            transform.x += vel.x * dt
            transform.y += vel.y * dt


class AnimationProcessor(esper.Processor):
    def process(self, dt: float):
        # Itera sobre entidades que têm Animação E Sprite
        for ent, (anim, sprite) in esper.get_components(Animation, Sprite):
            anim.timer += dt

            # Se o tempo passou da duração do frame...
            if anim.timer >= anim.frame_duration:
                anim.timer -= anim.frame_duration
                # Avança para o próximo frame (circular)
                anim.current_index = (anim.current_index + 1) % len(anim.frames)
                # Atualiza a imagem que está sendo desenhada
                sprite.image = anim.frames[anim.current_index]


class RenderProcessor(esper.Processor):
    """
    Renderiza entidades com Sprite e Transform.
    Suporta Câmera e Ordenação por Camadas (Z-Index)

    Args:
        esper (Processor): Base class for all processors to inherit from.
    """

    def __init__(self, camera=(0.0, 0.0)):
        super().__init__()
        self.camera = camera

    def process(self, context: dict | None = None):
        display = pygame.display.get_surface()
        if display is None:
            return

        cam_x, cam_y = self.camera
        if context and "camera" in context:
            cam_x, cam_y = context["camera"]

        # Coleta todas as entidades renderizáveis
        # Casting explicíto ajuda o editor, mas não é obrigatório em runtime
        entities: list[tuple[int, tuple[Transform, Sprite]]] = list(
            esper.get_components(Transform, Sprite)
        )

        # Ordena pelo atributo "layer" do Sprite (Z-Index)
        # Menor desenha primeiro (fundo), Maior desenha por último (frente)
        entities.sort(key=lambda item: getattr(item[1][1], "layer", 0))

        for ent, (tranform, sprite) in entities:
            img = getattr(sprite, "image", None)
            if img is None:
                continue

            # Conversão para int é necessário pois pixels não são fracionários
            display.blit(img, (int(tranform.x - cam_x), int(tranform.y - cam_y)))
