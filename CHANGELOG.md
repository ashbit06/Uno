# 0.1.4
## Uno.py
- Fixed so many things that I've lost track (mostly because I lost the diff)
- Also aded a recursion error. Need to find out what's causing it
### Game()
- Fixed card matching on turn
- Changed the type values for wild cards
### Card()
- Object initialization is simpler
- Now supports all Wild card colors
# 0.1.3
## General Changes
- Made player count prompt effective when running from `run.py`, and ineffective when running from `Uno.py`
## Uno.py
- Fixed `setup()` where it would give each player the amount of players times 7 cards
- Began work on fixing card matching on turn
### Game()
- Fixed a syntax error in `deckCheck()`
- Fixed `AttributeError: 'int' object has no attribute 'discard'` in line 191
- Added more things in `_recite()`
### Card()
- Made `Card().full` return a Title Case string
# 0.1.2
## run.py
- Added `run.py`, which allows the user to run Uno and select the amount of players and, if they want, run some tests in
`Uno.py` without having to edit code to be able to do both.
## Uno.py
- Added a `_recite()` method to the `Game` object for testing purposes
- Renamed the `nothing` cardType to `normal`
- Fixed card parsing from card codes
# 0.1.0
- Added CHANGELOG.md
- Removed Reverse cards from `game.deck` because I don't know how I would implement them into the game
# 0.1.1
- Renamed `get_keys_from_value()` to `getKeysFromValue()`
- Moved `getKeysFromValue()` to a new module called `methods.py` in `/lib`
