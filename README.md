# Mystery Island: The Lost Lighthouse

`Mystery Island` is a beginner-friendly, terminal-based Python adventure. A
storm leaves the player on an island where they must explore, manage energy,
collect two objects, cross an old bridge, and restore a lighthouse beacon.

The project uses only the Python standard library. It has no website, graphical
interface, game engine, database, external package, or AI API.

## Run the game

Python 3.8 or newer is recommended.

```bash
cd /home/student/island
python3 main.py
```

Enter the number shown beside an action. Enter `q` or `quit` at any numbered
menu to end the current game safely.

## Rules

- Every game begins on the **Beach** with **5 energy**.
- Normal movement costs 1 energy.
- Reaching 0 energy ends the game in a loss.
- The five locations are Beach, Jungle, Cave, Old Bridge, and Lighthouse.
- Rope and Lantern can each be collected only once.
- Rope is required to cross the Old Bridge.
- Lantern is required to light the Lighthouse.
- Tide pools, berries, caves, and unsafe bridge attempts have consequences.
- Lighting the beacon wins the game.
- After winning, losing, or quitting, the player can choose to replay with
  fresh energy and an empty inventory.

## Beginner-friendly code structure

The game is split into small functions in `main.py`:

- `show_title()` explains the story and rules.
- `get_player_name()` validates the player's name.
- `get_choice()` safely validates every numbered menu.
- `create_game_state()` creates energy, location, inventory, and event flags.
- `visit_beach()`, `visit_jungle()`, `visit_cave()`, `visit_bridge()`, and
  `visit_lighthouse()` control their respective locations.
- `run_game()` repeats location menus until the player wins, loses, or quits.
- `ask_to_replay()` handles starting a fresh game.
- `main()` connects the introduction, game, and replay loop.

Comments throughout `main.py` explain variables, conditions, loops, functions,
lists, dictionaries, input validation, and return values.

## Run the automated tests

```bash
python3 -m unittest discover -s tests -v
```

The tests cover:

- Required locations and starting state
- Invalid menu input recovery
- One-time inventory objects
- Rope and Lantern requirements
- A complete winning path
- A complete losing path
- Nested-menu quitting
- Replay validation

## Known limits

- Progress is not saved after the program closes.
- The story and map are intentionally small for beginner readability.
- The menus are text-only and designed for one local player.
