import random

def initiate_empty_tree_list():
    empty_tree = [
        '      ', 
        '    / \\',
        '   /   \\',
        '   /   \\',
        '  /     \\',
        '  /     \\',
        ' /       \\',
        '/         \\',
        '   |___|'
    ]
    
    return [list(line) for line in empty_tree]

def get_available_positions(tree_lists):
    available_positions = {}

    for line, lst in enumerate(tree_lists[2:-1], 2):
        start_boundary = lst.index('/')
        end_boundary = len(lst) - 1
        for idx in range(start_boundary + 1, end_boundary):
            if lst[idx] == ' ':
                available_positions[line] = \
                available_positions.get(line, []) + [idx]
    
    return available_positions

def decorate_tree(decorations, tree_lst):
    for decoration in decorations:
        available_positions = get_available_positions(tree_lst)
        line = random.choice(list(available_positions.keys()))
        position = random.choice(available_positions[line])

        tree_lst[line][position] = decoration

    return tree_lst

def display_ascii_tree(tree_lst):
    for lst in tree_lst:
        print(''.join(lst))


# TEst:
# decorations = ['o', 'O', '*']
# tree = initiate_empty_tree_list()
# tree = decorate_tree(decorations, tree)

# display_ascii_tree(tree)

# more_decorations = ['%', '$', '#']
# tree = decorate_tree(more_decorations, tree)

# display_ascii_tree(tree)