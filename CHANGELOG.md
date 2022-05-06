# 0.1
- Added CHANGELOG.md
- Removed Reverse cards from `game.deck` becauseI don't know how I would implement them into the game
# 0.1.1
- Renamed `get_keys_from_value()` to `getKeysFromValue()`
- Moved `getKeysFromValue()` to a new module called `methods.py` in `/lib`
# 0.1.2
## run.py
- Added `run.py`, which allows the user to run Uno and select the amount of players and, if they want, run some tests in `Uno.py` without having to edit code to be able to do both.
## Uno.py
- Added a `_recite()` method to the `Game` object for testing purposes
- Renamed the `nothing` cardType to `normal`
- Fixed card parsing from card codes
# 0.1.3
