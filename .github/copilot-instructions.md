<!-- Copilot instructions for the Asteroids repo -->
# Copilot / AI Agent Guidance

Purpose: concise, actionable notes so an AI coding agent can be productive immediately in this small Pygame-based project.

Quick run
- Install dependencies (project uses Pygame 2.6.1 declared in `pyproject.toml`). Example:

```bash
python -m pip install pygame==2.6.1
python main.py
```

Big picture
- Small Pygame-based Asteroids demo. `main.py` holds the primary game loop and calls `log_state()` every frame.
- `circleshape.py` provides `CircleShape`, a thin `pygame.sprite.Sprite`-based base class. Subclasses are expected to define `draw(self, screen)` and `update(self, dt)` and expose attributes like `position` (pygame.Vector2), `velocity`, `radius`, and optionally `rotation`.
- `logger.py` snapshots runtime state once per second and writes JSONL to `game_state.jsonl` (and events to `game_events.jsonl`). It scans the caller's local scope for `pygame` objects, `Group` instances, and individual sprites.

Key patterns and conventions (do not invent alternatives)
- Sprite container pattern: classes may define a class attribute `containers` so instances are auto-added to groups in `CircleShape.__init__` — preserve this pattern when creating new sprite classes.
- Attributes: prefer `position` (Vector2), `velocity` (Vector2), `radius` (number), `rotation` (degrees float). The logger relies on these names.
- Draw/update: implement `draw(self, screen)` for rendering and `update(self, dt)` for movement/logic; `main.py` handles the Pygame loop and flipping the display.
- Logging: `logger.log_state()` expects that the screen and sprite `Group`s are visible in the caller's local variables (it inspects the calling frame). Keep main loop variables in plain names (e.g., `screen`, `all_sprites`) to make logs meaningful.

Files of interest
- `main.py`: game loop, calls `log_state()` per frame, sets up `pygame.display` and `fps_clock`.
- `circleshape.py`: base sprite class and expected extension points.
- `player.py`: intended player implementation; currently contains syntax errors (missing `pygame` import, invalid class definition/signature and draw call). Fixes should follow `CircleShape` patterns.
- `logger.py`: state/event logging implementation — read before changing naming conventions.
- `constants.py`: game-wide constants like `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `PLAYER_RADIUS`.

Common fixes an agent may be asked to do (examples)
- Repair `player.py`: import `pygame`, declare `class Player(CircleShape):`, implement `__init__(self, x, y, radius=PLAYER_RADIUS):` that sets `rotation`, `position`, `velocity`, and `radius` by calling `super().__init__(x, y, radius)`; implement `draw(self, screen)` using `pygame.draw.polygon(screen, color, self.triangle())` and ensure `triangle()` uses `self.position`, `self.rotation` and `self.radius`.
- Add or preserve group containers: if a new sprite class needs automatic addition to groups, define `containers = (some_group,)` as a class attribute and rely on `CircleShape`'s constructor behavior.

Testing / debugging notes
- There are no automated tests. Run locally with `python main.py` and watch `game_state.jsonl` and `game_events.jsonl` for logger output.
- If modifying logging or variable names, update `logger.py` expectations (it inspects frame locals and specific attribute names). Prefer changing code rather than the logger when possible.

When editing: be conservative and local
- Make minimal changes that preserve the current attribute and naming conventions (position/velocity/radius/rotation).
- Prefer adding small helper functions over large refactors; this repo is minimal and relies on simple conventions.

Ask the maintainer when unclear
- If you need new global state (new Groups, different attribute names), request clarification before sweeping changes — the logger and existing code rely on current names.

If any section here is unclear or you want more examples (e.g., a corrected `player.py`), ask and I'll provide a patch.
