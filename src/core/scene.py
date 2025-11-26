"""
Esse código implementa um padrão de cenas (Scene / SceneManager) para organizar estados\
    de jogo em Pygame: cada cena herda de Scene e o SceneManager cria/troca e delega\
        chamadas de entrada, atualização e desenho para a cena ativa.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type, Union

import pygame


class Scene(ABC):
    """
    Base abstrata para cenas do jogo.

    Cada cena deve implementar os métodos abaixo. A cena recebe uma referência ao\
        SceneManager para permitir transições e acesso a recursos compartilhados.
    """

    def __init__(self, manager: SceneManager):
        """
        Inicializa a cena.

        Args:
            manager (SceneManager): Gerenciador de cenas que controla transições.
        """
        self.manager = manager
        surface = pygame.display.get_surface()
        if surface is None:
            raise RuntimeError(
                "Erro Crítico: Tentativa de criar Cena antes de "
                "pygame.display.set_mode()",
            )
        self.display: pygame.Surface = surface

    @abstractmethod
    def process_input(self, event: pygame.event.Event):
        """
        Processa um evento único do Pygame.

        Chamado pelo SceneManager para cada evento relevante (teclas, mouse).

        Args:
            event (pygame.event.Event): Evento a ser tratado.
        """
        pass

    @abstractmethod
    def update(self, dt: float):
        """
        Atualiza a lógica da cena.

        Chamado a cada frame com o delta time em segundos.

        Args:
            dt (float): Tempo em segundos desde o último frame.
        """
        pass

    @abstractmethod
    def draw(self):
        """
        Desenha a cena na superfície principal.

        Deve usar self.display para renderizar elementos.
        """
        pass

    # Hooks de Ciclo de Vida
    def on_enter(self):
        """Executado quando a cena entra no topo da pilha."""
        pass

    def on_exit(self):
        """Executando quando a cena sai do topo da pilha."""
        pass


class SceneManager:
    """
    Gerencia a cena ativa e transições entre cenas.

    Suporta trocar por nova cena, empilhar/estourar cenas (push/pop) e de chamadas de\
        input/update/draw para a cena atual. As cenas podem implementar hooks opcionais\
            `on_enter()` e `on_exit()` para inicialização/limpeza.
    """

    def __init__(self):
        """Inicializa o gerenciador com pilha vazia."""
        self._stack: list[Scene] = []

    @property
    def current_scene(self) -> Scene | None:
        return self._stack[-1] if self._stack else None

    def switch_to(self, scene: Union[Type[Scene], Scene]):
        """Troca completa: Remove a atual e coloca a nova.

        Args:
            scene (Union[Type[Scene], Scene]): Nova cena
        """
        if self.current_scene:
            self.current_scene.on_exit()

        new_scene = scene(self) if isinstance(scene, type) else scene

        self._stack = [new_scene]  # Limpa a pilha e define a nova
        new_scene.on_enter()

    def push(self, scene: Union[Type[Scene], Scene]):
        """Pausa a atual e coloca uma nova por cima (ex: Pause).

        Args:
            scene (Union[Type[Scene], Scene]): Nova cena
        """
        if self.current_scene:
            self.current_scene.on_exit()

        new_scene = scene(self) if isinstance(scene, type) else scene
        self._stack.append(new_scene)
        new_scene.on_enter()

    def pop(self):
        """Remove a cena do topo e retoma a anterior."""
        if not self._stack:
            return

        scene_to_remove = self._stack.pop()
        scene_to_remove.on_exit()

        # Retoma a cena anterior (se houver)
        if self.current_scene:
            self.current_scene.on_enter()

    def run(self, dt: float):
        """
        Loop reverso para desenhar transparência

        Args:
            dt (float): date time
        """
        # 1. Update: Só a cena do topo recebe a lógica (o jogo ao fundo não se move)
        if self.current_scene:
            self.current_scene.update(dt)

        # 2. Draw: Desenha todas as cenas da base para o topo
        # Isso permite menus semi-transparentes sobre o jogo
        for scene in self._stack:
            scene.draw()

    def process_input(self, event: pygame.event.Event):
        """Delegar evento para a cena ativa

        Args:
            event (pygame.event.Event): Evento a ser delegado
        """
        if self.current_scene:
            self.current_scene.process_input(event)
