# Game-of-battleship
Programmed the game of battleship in Python

Battleship is a classic two person game, originally played with pen and paper.

On a grid (typically 10 x 10), players ’hide’ ships of mixed length; horizontally or vertically (not diagonally) without any overlaps. The exact types and number of ships varies by rule, but for this posting, I’m using ships of lengths: 5, 4, 3, 3, 2 (which results in 17 possible targets out of the total of 100 squares).

Note: even though ships cannot overlap, there is nothing in the rules to say they cannot touch. (In fact, some players consider this a strategy to confuse an opponent by obfuscating the true layout of ships. If there are five ‘hits’ in a row, a naive player might consider this to be the successful destruction of an aircraft carrier of length 5, but actually it could be the sinking of a battleship of length 4, and part of a cruiser of length 3)

## Simple Game Rules

We’ll start with a description of the simplified method of play:

After each player has hidden his fleet, players alternate taking shots at each other by specifying the coordinates of the target location. After each shot, the opponent responds with either a call HIT! or MISS! indicating whether the target coordinates have hit part of a boat, or open water. An example of a game in progress is show on the left.

## Hunt and Target strategy

I have implemented the hunt and target strategy where once I find a battleship on the board, in every turn I try and find its next position till its completely eliminated. In the code, I am tracing the the board using alternate diagonal strategy.

## References
http://datagenetics.com/blog/december32011/index.html
