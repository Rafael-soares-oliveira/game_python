import math

import esper
import pygame

from src.core.components import (
    Animation,
    EnemyProjectile,
    EnemyTag,
    Health,
    Invincibility,
    MovePattern,
    PlayerTag,
    Projectile,
    Sprite,
    Transform,
    Velocity,
)


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

        # 2. Movimento Matemático Complexo (Inimigo)
        for ent, (trans, pattern) in esper.get_components(Transform, MovePattern):
            pattern.time += dt
            t = pattern.time

            if pattern.pattern_type == "linear":
                # Movimento reto baseado em ângulo
                trans.x = pattern.start_x + math.cos(pattern.angle) * pattern.speed * t
                trans.y = pattern.start_y + math.sin(pattern.angle) * pattern.speed * t

            elif pattern.pattern_type == "sine":
                # Zig-Zag: Move na direção do ângulo, oscila na perpendicular
                # Posição base avançando
                base_x = pattern.start_x + math.cos(pattern.angle) * pattern.speed * t
                base_y = pattern.start_y + math.sin(pattern.angle) * pattern.speed * t

                # Oscilação (Seno)
                offset = math.sin(t * pattern.frequency) * pattern.amplitude

                # Aplica offset perpendicular ao ângulo (-sin, cos)
                trans.x = base_x - math.sin(pattern.angle) * offset
                trans.y = base_y + math.cos(pattern.angle) * offset

            elif pattern.pattern_type == "spiral":
                # Espiral crescendo
                current_radius = pattern.speed * t
                current_angle = pattern.angle + (t * pattern.frequency)
                trans.x = pattern.start_x + math.cos(current_angle) * current_radius
                trans.y = pattern.start_y + math.sin(current_angle) * current_radius


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
        entities: list[tuple[int, tuple[Transform, Sprite]]] = list(
            esper.get_components(Transform, Sprite)
        )

        # Ordena pelo atributo "layer" do Sprite (Z-Index)
        # Menor desenha primeiro (fundo), Maior desenha por último (frente)
        entities.sort(key=lambda item: getattr(item[1][1], "layer", 0))

        for ent, (transform, sprite) in entities:
            if sprite.image:
                display.blit(
                    sprite.image, (int(transform.x - cam_x), int(transform.y - cam_y))
                )


class CollisionProcessor(esper.Processor):
    def process(self, dt: float):
        # Parte 1: Invincibility
        for ent, (inv, sprite) in esper.get_components(Invincibility, Sprite):
            if inv.is_active:
                inv.timer -= dt
                if inv.timer <= 0:
                    inv.is_active = False
                    sprite.image.set_alpha(255)
                else:
                    if (inv.timer % (inv.blink_interval * 2)) > inv.blink_interval:
                        sprite.image.set_alpha(50)
                    else:
                        sprite.image.set_alpha(255)

        # Parte 2: Coleta Inimigos
        enemies_data = []
        for ent, (trans, sprite, _) in esper.get_components(
            Transform, Sprite, EnemyTag
        ):
            rect = pygame.Rect(trans.x, trans.y, sprite.width, sprite.height)
            enemies_data.append((rect, ent))

        # Parte 3: Player vs Enemy
        enemy_projectiles = []
        for ent, (trans, sprite, proj) in esper.get_components(
            Transform, Sprite, EnemyProjectile
        ):
            rect = pygame.Rect(trans.x, trans.y, sprite.width, sprite.height)
            enemy_projectiles.append((rect, ent, proj.damage))

        for ent, (trans, sprite, inv, health) in esper.get_components(
            Transform, Sprite, Invincibility, Health
        ):
            if not esper.has_component(ent, PlayerTag):
                continue
            if inv.is_active:
                continue

            player_rect = pygame.Rect(trans.x, trans.y, sprite.width, sprite.height)
            hit_damage = 0

            # A. Checa colisão com corpo do Inimigo
            for enemy_rect, enemy_ent in enemies_data:
                if player_rect.colliderect(enemy_rect):
                    hit_damage = 20
                    break

            # B. Checa colisão com Tiro do Inimigo
            if hit_damage == 0:
                for proj_rect, proj_ent, damage in enemy_projectiles:
                    if player_rect.colliderect(proj_rect):
                        hit_damage = damage
                        esper.delete_entity(proj_ent, immediate=True)  # Tiro some
                        break

            # Aplica Dano se houve colisão
            if hit_damage > 0:
                health.current -= hit_damage
                inv.is_active = True
                inv.timer = inv.duration

        # -------------------------------------------------
        # PARTE 4: Laser vs Inimigo
        # - Evita deletar durante iteração: acumula e deleta depois
        # -------------------------------------------------
        lasers_to_delete: set[int] = set()
        enemies_to_delete: set[int] = set()

        for laser_ent, (l_trans, l_sprite, l_proj) in esper.get_components(
            Transform, Sprite, Projectile
        ):
            # Se o laser já está marcado para remoção, pula
            if laser_ent in lasers_to_delete:
                continue

            laser_rect = pygame.Rect(
                l_trans.x, l_trans.y, l_sprite.width, l_sprite.height
            )

            for enemy_rect, enemy_ent in enemies_data:
                if laser_rect.colliderect(enemy_rect):
                    if not esper.entity_exists(enemy_ent) or not esper.entity_exists(
                        laser_ent
                    ):
                        continue

                    # Marca o laser para remoção
                    lasers_to_delete.add(laser_ent)

                    # Aplica dano ao inimigo (se tiver componente Health)
                    enemy_health = esper.try_component(enemy_ent, Health)
                    if enemy_health:
                        enemy_health.current -= l_proj.damage
                        if enemy_health.current <= 0:
                            enemies_to_delete.add(enemy_ent)
                    else:
                        # Sem componente Health = morte instantânea
                        enemies_to_delete.add(enemy_ent)

                    # Não checar mais inimigos para esse laser
                    break

        # Agora deletar todas as entidades marcadas (após iteração)
        for ent in lasers_to_delete:
            if esper.entity_exists(ent):
                esper.delete_entity(ent, immediate=True)

        for ent in enemies_to_delete:
            if esper.entity_exists(ent):
                esper.delete_entity(ent, immediate=True)
