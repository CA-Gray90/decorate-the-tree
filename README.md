# README #
Repository for working on my 'Find the Ring' game. 

A terminal game in which the user plays Bilbo Baggins from The Hobbit.

The game uses a matrix to display the users position ('B') and Gollums
position ('G'). 

The user moves thier character position by entering commands into the console.
The commands are either 'up', 'down', 'left', 'right'.

Gollums position changes automatically on each turn, moving towards the character.
The amount of moves Gollum makes is selected randomly between 0 - 2 for each turn.

If the user stumbles upon the ring (i.e the matrix position that 'contains'
the ring), they win. 
If Gollum catches up to them (i.e Gollumns position and the users position are
the same), the player loses.

Work in progress.