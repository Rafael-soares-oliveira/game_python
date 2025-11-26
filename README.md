# 🚀 Space Shooter - Python

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Engine](https://img.shields.io/badge/Engine-Pygame_CE-yellow)
![Architecture](https://img.shields.io/badge/Architecture-ECS-green)
![Build](https://img.shields.io/github/actions/workflow/status/Rafael-soares-oliveira/game_python/ci.yml?label=CI%2FCD)

Um Shoot 'em Up desenvolvido em Python focado em **Engenharia de Software**, **Arquitetura Limpa** e **Padrões de Projeto**.

Este projeto demonstra como desacoplar dados de comportamento utilizando o padrão **ECS (Entity Component System)**, fugindo da orientação a objetos tradicional para garantir performance e escalabilidade. O jogo roda nativamente no Desktop e na Web (WebAssembly).

---

## 🎮 Demo Online (WASM)

O projeto conta com um pipeline de CI/CD que compila o Python para WebAssembly.
**[Jogue aqui no Navegador](https://Rafael-soares-oliveira.github.io/game_python/)**

---

## 🛠️ Tecnologias
- Python 3.12
- Pygame-ce (Community Edition)
- Esper (ECS)
- Pygbag (WebAssembly Export)
- Ruff (Linter)

---

## 🏗️ Arquitetura e Engenharia

O diferencial deste projeto é a estrutura robusta, organizada para manutenção e escalabilidade.

### 1. Entity Component System (ECS)
Utilizando a biblioteca `esper`, o jogo separa estritamente dados e lógica:
* **Entities:** Apenas IDs inteiros (Player, Enemy, Laser).
* **Components:** `dataclasses` puras sem métodos (ex: `Velocity`, `Transform`, `Health`, `MovePattern`).
* **Systems:** Processadores que executam a lógica a cada frame (ex: `MovementProcessor`, `CollisionProcessor`, `RenderProcessor`).

### 2. State Pattern (Máquina de Estados)
O fluxo do jogo é gerenciado por uma **Stack-based State Machine**.
* Permite empilhar cenas (ex: Pausar o jogo sem perder o estado da partida).
* Transições limpas entre Menu -> Jogo -> Vitória/GameOver.
* Isolamento total de memória entre reinícios de partida (`World Context Isolation`).

### 3. Tooling Moderno
* **Gerenciamento de Dependências:** Utiliza `uv` (sucessor ultra-rápido do Pip/Poetry).
* **Linting & Formatting:** Código padronizado com `ruff`.
* **Type Hinting:** Uso extensivo de tipagem estática para robustez.
* **CI/CD:** GitHub Actions configurado para Quality Gate (Linting) e Deploy automático para GitHub Pages via `pygbag`.

---

## 📂 Estrutura do Projeto

```text
src/
├── core/           # O "Motor" do jogo (Agnóstico ao gameplay)
│   ├── scene.py    # Classe Base e SceneManager (State Machine)
│   ├── systems.py  # Lógica pesada (Física, Colisão, Render, IA)
│   └── components.py # Dados puros (Dataclasses)
├── scenes/         # Telas do jogo (Menu, Game, Pause, Victory)
├── entities.py     # Factory Pattern: Criação e montagem de entidades
├── settings.py     # Configurações globais e constantes
├── utils.py        # Ferramentas (Carregamento inteligente de sprites)
└── main.py         # Ponto de entrada e Game Loop assíncrono
```

---

## 🕹️ Mecânicas Implementadas
**Auto-Fire System:** Disparo automático com delay inicial estratégico.

**Math-based Enemy Patterns:** O inimigo utiliza funções trigonométricas (Seno, Cosseno) para criar padrões de tiro complexos (Leque, Zig-Zag, Espiral) com velocidade variável (random.uniform).

**Invincibility Frames:** Sistema de feedback visual e imunidade temporária ao receber dano.

**UI Reativa:** Barras de vida desenhadas proceduralmente (pixel art via código).

---

## ⌨️ Controles

| Tecla | Ação |
| :----: | :----: |
| WASD | Mover a Nave |
| Automático | Atirar (Inicia após 2s) |
| ENTER | Pausar / Confirmar / Reiniciar |
| ESC | Voltar ao Menu / Sair |