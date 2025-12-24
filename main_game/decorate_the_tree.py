import random
import time
import os
import ascii_main_title_mod
import json
import re

class Position:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        if not isinstance(value, int) and value != None:
            raise TypeError('Value given must be an integer')
        self._x = value
    
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if not isinstance(value, int) and value != None:
            raise TypeError('Value given must be an integer')
        self._y = value

    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return (self.x == other.x) and (self.y == other.y)

class PositionMixin:
    @property
    def position(self):
        return self._position
    
    @property
    def position_values(self):
        return (self._position.x, self._position.y)
    
    def set_position(self, x, y):
        self._position.x = x
        self._position.y = y

class Player(PositionMixin):
    def __init__(self):
        self._position = Position()

    def move(self, choice):
        current_x, current_y = self.position.x, self.position.y

        match choice:
            case 'up':
                new_x = current_x
                new_y = current_y - 1
            case 'down':
                new_x = current_x
                new_y = current_y + 1
            case 'left':
                new_x = current_x - 1
                new_y = current_y
            case 'right':
                new_x  = current_x + 1
                new_y = current_y
            case _:
                new_x = current_x
                new_y = current_y

        self.set_position(new_x, new_y)

class Human(Player):
    def __init__(self):
        super().__init__()
        self._inventory = Inventory()
        self._mark = 'E'    # E for Elf

    @property
    def mark(self):
        return self._mark
    
    @property
    def inventory(self):
        return self._inventory

    def pick_up(self, item):
        if isinstance(item, Decoration):
            self._inventory.insert_item(item)
    
    def drop_off(self):
        return self._inventory.dump_all_items()

class Grinch(Player):
    def __init__(self):
        super().__init__()
        self._mark = 'G'

    @property
    def mark(self):
        return self._mark

    def _left_right_move(self, player_position):
        if self.position.x > player_position.x:
            return 'left'
        elif self.position.x < player_position.x:
            return 'right'
        else:
            return None
    
    def _up_down_move(self, player_position):
        if self.position.y > player_position.y:
            return 'up'
        elif self.position.y < player_position.y:
            return 'down'
        else:
            return None

    def get_move(self, player_position):
        left_right_move = self._left_right_move(player_position)
        up_down_move = self._up_down_move(player_position)
        random_move_direction = random.choice(('left_right', 'up_down'))

        match random_move_direction:
            case 'left_right':
                if left_right_move:
                    return left_right_move
                return up_down_move
            case 'up_down':
                if up_down_move:
                    return up_down_move
                return up_down_move

class Tree(PositionMixin):
    def __init__(self):
        self._position = Position()
        self._decorations = []
    
    @property
    def decorations(self):
        return tuple(self._decorations)

    def place_decorations(self, items):
        '''
        Docstring for place_decorations
        
        :param items: Expects a sequence of Decoration type objects
        '''

        for item in items:
            if isinstance(item, Decoration):
                self._decorations.append(item)
    
    @property
    def mark(self):
        return self.__class__.__name__[0].capitalize()


class Decoration(PositionMixin):
    number_of_decorations = 0

    def __init__(self):
        self._position = Position()
        self._mark = None
        self._name = self.__class__.__name__
        Decoration.number_of_decorations += 1
    
    @property
    def name(self):
        return self._name
    
    @property
    def mark(self):
        return self._mark
    
    def __str__(self):
        return self._mark

    def __repr__(self):
        return f'{self.__class__.__name__}'

class SmallBauble(Decoration):
    def __init__(self):
        super().__init__()
        self._mark = 'o'
        self._name = 'Small Bauble'

class BigBauble(Decoration):
    def __init__(self):
        super().__init__()
        self._mark = '0'
        self._name = 'Big Bauble'

class Light(Decoration):
    def __init__(self):
        super().__init__()
        self._mark = '*'

class Star(Decoration):
    def __init__(self):
        super().__init__()
        self._mark = '@'

class Inventory:
    MAX_ITEMS = 4

    def __init__(self):
        self._items = []

    def is_full(self):
        return len(self._items) == self.__class__.MAX_ITEMS
    
    def insert_item(self, item):
        if not self.is_full():
            self._items.append(item)

    def dump_all_items(self):
        items = self._items
        if items:
            self._items = []
            return items
        return []

    @property
    def items(self):
        return tuple(self._items)

class Field():
    FIELD_SIZE = 10
    EMPTY = ' '
    MAX_DECORATIONS = int(FIELD_SIZE * 1.5)
    MIN_DECORATIONS = FIELD_SIZE
    X_BOUNDARY = FIELD_SIZE - 1      # x is columns, left to right
    Y_BOUNDARY = FIELD_SIZE - 1      # y is rows, top to bottom

    def __init__(self):
        self.reset()
    
    def reset(self):
        self._field_matrix = self._set_empty_field(Field.FIELD_SIZE)
        self._human = Human()
        self._grinch = Grinch()
        self._tree = Tree()
        self._decorations = self._get_decorations()
        self._total_decorations = len(self._decorations)
        self._occupied = set()
    
    @property
    def field_matrix(self):
        return self._field_matrix
    
    @property
    def player_inventory(self):
        return self._human.inventory.items

    @property
    def decorations(self):
        return self._decorations
    
    def _get_decorations(self):
        choices = (SmallBauble, BigBauble, Light)
        min, max = Field.MIN_DECORATIONS, Field.MAX_DECORATIONS

        quantity = random.randrange(min, max)
        decorations = [random.choice(choices)() for _ in range(quantity)]
        decorations.append(Star())
        return decorations

    def get_random_position(self):
        occupied = self._occupied

        while True:
            x = random.randrange(self.FIELD_SIZE)
            y = random.randrange(self.FIELD_SIZE)
            if (x, y) not in occupied:
                occupied.add((x, y))
                break

        return (x, y)

    def spawn_field(self):
        for thing in (self._human, self._grinch, self._tree,
                      *self._decorations):
            thing.set_position(*self.get_random_position())
        
        self._human.inventory

    @staticmethod
    def _set_empty_field(n):
        matrix = [
            [Field.EMPTY for _ in range(n)] for _ in range(n)
        ]
        return matrix

    def _clear_field(self):
        for row in self._field_matrix:
            for idx in range(len(row)):
                row[idx] = Field.EMPTY
        
        self._occupied = set()

    def _remove_decoration(self, decoration):
        self._decorations.remove(decoration)

    def _pick_up_item(self):
        for decoration in self._decorations:
            if decoration.position == self._human.position:
                if not self._human.inventory.is_full():
                    self._human.pick_up(decoration)
                    print()
                    print(f'You picked up a {decoration.name}!')
                    print()
                    self._remove_decoration(decoration)
                else:
                    print()
                    print('Inventory full!')
                    print()

    def _drop_off_item(self):
        if self._tree.position == self._human.position:
            decorations = self._human.drop_off()
            print()
            print('Decorations being dropped off:')
            print(f'{', '.join(
                decoration.name for decoration in decorations)}')
            print()

            self._tree.place_decorations(decorations)
            print('Tree now has:')
            print(self._tree.decorations)
            print(f'({len(self._tree.decorations)}/{self._total_decorations})')

    def check_item_actions(self):
        self._pick_up_item()
        self._drop_off_item()

    def tree_full(self):
        return len(self._tree.decorations) == self._total_decorations

    def _valid_position(self, player):
        if player.position.x > Field.X_BOUNDARY or \
        player.position.x < 0:
            return False
        elif player.position.y > Field.Y_BOUNDARY or \
        player.position.y < 0:
            return False
        return True

    def update_positions(self):
        self._clear_field()

        for thing in (*self._decorations, self._tree,
                      self._human, self._grinch):

            x, y = thing.position_values
            marker = thing.mark  # A way to get a display for now

            self._field_matrix[y][x] = marker
            self._occupied.add((x, y))

    def human_move(self, choice):
        previous_x, previous_y = self._human.position_values
        self._human.move(choice)
        if not self._valid_position(self._human):
            self._human.set_position(previous_x, previous_y)

    def grinch_move(self):
        human_position = self._human.position
        choice = self._grinch.get_move(human_position)
        self._grinch.move(choice)
    
    def human_caught(self):
        return self._human.position == self._grinch.position

class InputMixin:
    VALID_UP = {'u', 'up'}
    VALID_DOWN = {'d', 'down'}
    VALID_LEFT = {'l', 'left'}
    VALID_RIGHT = {'r', 'right'}

    @staticmethod
    def _prompt(text):
        return f'=> {text}'

    def _yes_or_no(self, text):
        while True:
            choice = input(f'{self._prompt(text)} (y/n): ').lower().strip()
            if choice in {'y', 'n', 'yes', 'no'}:
                return choice[0] == 'y'
            print('Invalid choice, please try again.')

    def _move_choice(self):
        print('Players move')
        while True:
            choice = input(f'{self._prompt(
                'Choose from: (u)p, (d)own, (l)eft, (r)ight:'
                )} ').lower().strip()

            if choice in InputMixin.VALID_UP:
                return 'up'
            elif choice in InputMixin.VALID_DOWN:
                return 'down'
            elif choice in InputMixin.VALID_LEFT:
                return 'left'
            elif choice in InputMixin.VALID_RIGHT:
                return 'right'
            else:
                print('Choice is not valid, please try again.')

    def _enter_to_continue(self, msg='Press Enter to continue...'):
        input(self._prompt(msg))

class DisplayMixin(InputMixin):
    DISPLAY_WIDTH = 60

    def _display_welcome(self):
        ascii_main_title_mod.main_title_animation()
        print()

    def _display_rules(self):
        if self._yes_or_no('Would you like to see the rules?'):
            with open('DTT_rules.json', 'r') as file:
                rules = json.load(file)
            
            rule_sets = [rules['game_intro'],
                        rules['gameplay_rules'],
                        rules['rules_outro']]

            for idx, rule_set in enumerate(rule_sets):
                print()
                for line in rule_set:
                    print(line)
                print()
                if idx != len(rule_sets) - 1:
                    self._enter_to_continue()
        
        self._enter_to_continue('Ready to play? Enter to continue...')

    @staticmethod
    def _get_cleaned_line_display(string):
        cleaned_string = re.sub(r"[\[\]']", '', repr(string))
        cleaned_string = re.sub(r",", " ", cleaned_string)
        return cleaned_string

    def _display_field(self):
        field = self._field.field_matrix
        row_length = len(self._get_cleaned_line_display(field[0])) + 2

        print()
        print(('_' * row_length).center(DisplayMixin.DISPLAY_WIDTH, ' '))
        for row in field:
            row = self._get_cleaned_line_display(row)
            print(f'|{row}|'.center(DisplayMixin.DISPLAY_WIDTH, ' '))
        print(('-' * row_length).center(DisplayMixin.DISPLAY_WIDTH, ' '))
        print()
    
    def _display_inventory(self):
        print(f'Inventory:\n{self._field.player_inventory}')

    def _clear_and_display_title(self):
        os.system('clear')
        print(' Decorate the Tree! '.center(DisplayMixin.DISPLAY_WIDTH, '*'))
        self._display_key()
    
    @staticmethod
    def _display_goodbye():
        print('Thank you for playing. Goodbye and Merry Xmas!')
    
    @staticmethod
    def _display_key():
        print()
        print('Reference Sheet:')
        print('--------------------------')
        print('Elf (You)   : E')
        print('Grinch      : G')
        print('Tree        : T')
        print('Decorations : *, o, O, @')
        print('--------------------------')
        print()

class DTTGame(DisplayMixin):
    def __init__(self):
        self._field = Field()

    def _human_turn(self):
        choice = self._move_choice()
        self._field.human_move(choice)
    
    def _grinch_turn(self):
        number_of_moves = random.randrange(3)
        while number_of_moves > 0:   
            self._field.grinch_move()
            number_of_moves -= 1
    
    def _got_caught(self):
        return self._field.human_caught()
    
    def _game_end(self):
        if self._got_caught():
            print()
            print('Oh no! You got caught by the Grinch!')
            print('You lose...')
            print()
        else:
            print()
            print('Tree is full of decorations! You win.')
            print()
    
    def _play_again(self):
        return self._yes_or_no('Would you like to play again?')

    def _countdown(self):
        print('Game will begin in:')
        for n in range(3, 0, -1):
            print(n)
            time.sleep(1)

    def play(self):
        os.system('clear')
        self._display_welcome()
        self._display_rules()
        self._countdown()
        keep_playing = True
        
        while keep_playing:
            self._field.spawn_field()
            while True:
                self._clear_and_display_title()
                self._field.update_positions()
                print('Number of decorations left: '
                    f'{len(self._field.decorations)}')
                self._display_field()
                self._display_inventory()
                self._field.check_item_actions()
                
                if self._got_caught():
                    break
                if self._field.tree_full():
                    break
                self._human_turn()
                self._grinch_turn()
            self._game_end()
            if self._play_again():
                self._countdown()
                self._field.reset()
            else:
                keep_playing = False

        self._display_goodbye()

game = DTTGame()
game.play()