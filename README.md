# Aggravation

The classic Aggravation board game written in Python with [Pygame](https://www.pygame.org/wiki/about).

![Alt text](images/board.png)

## Table of Contents

1. [Package Info and Use](#Package-Info-and-Use)
2. [Game Instructions](#Game-Instructions)
3. [Game Rules](#Game-Rules)
4. [Known Bugs](#Known-Bugs)

# Package Info and Use

There are two options for downloading and running the game:

## Option 1
Download [aggravation.py](https://github.com/vaughntastic77/Aggravation/tree/main/aggravation.py) and [images](https://github.com/vaughntastic77/Aggravation/tree/main/images) into same directory and run.

## Option 2 (Mac only):
Downlad [Aggravation.app](https://github.com/vaughntastic77/Aggravation/tree/main/package/dist/Aggravation.app) from the [dist](https://github.com/vaughntastic77/Aggravation/tree/main/package/dist) folder and run.

# Game Instructions

The game opens to the main menu. Here you can choose to resume the last saved game or start a new game.

When you choose a new game, you can choose 1-4 players and then choose if you want computers to fill the rest.

Instructions are given in game, but the general flow is as follows:
1. Press `Space` to roll the die
2. Choose an available marble to move by pressing `1`, `2`, `3`, or `4`.
3. Choose a which space to move the chosen marble to by pressing `1`, `2`, or `3`, or press `Esc` to go back to choosing a marble.

At the start of any turn, the pause menu can be opened with `P`. Here you can choose to resume `R`, save and quit `S`, or quit to menu `Esc`.

When a player wins, you can return to the menu `Space` or continue playing `C`.

# Game Rules

## Objective:
Be the first to move all 4 of your marbles from your base to home.

## Play the game:
Roll the die on your turn and try to start or move one of your marbles. Take another turn anytime a 6 is rolled.

You must roll a 1 or 6 to start a marble. Only one marble can occupy the start.

Once a marble is started, move each turn the count of the die clockwise around the board.

Anytime you roll a 1 or 6 you can start another marble if the space is open.

You can jump over openents marbles counting the space. You can land on an opponents marble to "aggravate" them and send their marble back to base. You CANNOT aggravate a player on their own start.

You CANNOT jump over or land on your OWN marble. If you cannot move a marble the full die count, then it cannot move. If you cannot move any marbles, your turn is over.

## Shortcuts:
You can use the white inside corners and black center as a shortcut to home. You must land on one of the spaces to use them on your next turn.

When on the white shortcuts, you can move clockwise around the white spaces the count of your die. When you wish to leave, you must do so on your next turn.

The center space can be accessed from your own start or the white shortcuts. If you roll a 6, you can move a marble that is at your start directly to the center. Otherwise, you must roll a 1 to enter the center from the white shortcuts. You must roll a 1 to leave the center onto any white shortcut.

## Winning:
A player wins when all 4 marbles are home. When entering home, you must reach each space by the exact count.

# Known Bugs

All known fixable bugs are currently resolved.

1. There is currently a bug with pygame that sometimes causes the display to not update correctly.
