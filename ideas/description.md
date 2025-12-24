# General description of game:
In this game, you play a character that needs to pick up all the christmas
tree Decorations in a field and deposit them at the Tree before the Grinch catches
you.

The game works like this:
    - At the start:
        - You spawn in a random position in the Field
        - The Grinch spawns in a random position
        - The Tree spawns in a random position
        - The decorations are scattered randomly throughout the field
    - You can then choose to make a move: up, down, left, right
        (May incorporate abbreviated versions and 'wasd' moves)
    - The Grinch makes a move towards you.
    
    - If you are over a decoration position, you pick it up. Your Inventory can
    hold 3 Decorations.
    - If you are over the Tree position you deposit the Decorations in your
    Inventory. 

    - Once you deposit all the Decorations at the Tree, you win the game!
    - If the Grinch lands on your position however you lose the game!

# Major Nouns and Verbs
## Nouns:
    Game
    Field
    Position

    Character:
        Player
        Grinch
    Move
    Inventory

    Tree
    Decorations (o, 0, *, @)

## Verbs
    play
    pickup
    deposit
    move
    spawn
    catch

# Noun, verb associations:
Game:
    Has:
        - Players (Human, Grinch)
        - Field
        - Tree
        - Decorations
    Can:
        - Initiate Game (play)
        - Display Field (with Human, Grinch, Tree, Decorations)
        - Spawn Players, Tree, Decorations (or ask them to spawn)
        - Check if Tree is decorated
        - Check if Player has been caught
        - Play again(?)

Player:
    Has: 
        - Position
    Can:
        - move
        - spawn (random position)

Human(Player):
    Has:
        - Inventory
        - (Position)
    Can:
        - Pickup
        - Deposit
        - (move, spawn)

Grinch(Player):
    Has:
        - (Position)
    Can:
        - catch(? Should Game be in charge?)
        - (move, spawn)

Inventory:
    Has:
        - Space for 3 items (Decorations)
    Can:
        - Add decoration
        - remove/deposit decoration
        - be displayed(?)

Tree:
    Has:
        - Position
        - Decorations (or a place for them)
    Can:
        - spawn
        - be decorated (take decoration deposit)
        - Display (via Mixin?)

Decorations:
    Has:
        - Position
    Can:
        - Spawn
        - be picked up
        - be deposited    

Field:
    Has: 
        - Positions (based on matrix columns and rows?)
        - Players?
        - Tree?
        - Decorations?
    Can:
        - Spawn all players
        - Track all positions?
        - Display?

# Notes:
- Position objects should be able to be compared for equality Position == Position
- Display methods should be in a seperate mixin?
- Spawn behaviour should perhaps be shared through a Mixin? It works with the 
position Object to produce a random Position
- Tree is able to decorate itself randomly (use of nested lists) to be displayed
- Spawn positions must not overlap