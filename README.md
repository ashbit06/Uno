# Uno in Python!
Currently in development, with a bunch of bugs. Please help contribute!

I try to have this follow the rules of Uno, with no special rules such as the 7's Rule or stacking. However, if you are willing to try to add an optional rule, go right ahead. Be sure to somehow add them to the `game.rules` dictionary. Still don't know how I'd implement it though.
## Running the Program

Just run it in python or like this in the terminal:
```
$ python3 /file/path/run.py
```

## How to Play
### Starting the Game
**Be sure to run `run.py` and not `Uno.py`.** Once you start the program, you will be prompted with a message like this:
```
How many players?
```
Enter in a number 2-8 (I always use 3 players when testing).

## TODO
- [x] Fix the card dealing (currently gives each player *21 cards*???)
- [ ] Fix card matching on turn
- [x] Fix card parsing...
	- [x] From a card code
	- [x] From a card name
- [ ] Make all cards functional
	- [x] Number cards
	- [ ] Skip cards
	- [ ] Reverse cards
	- [ ] Wild cards
