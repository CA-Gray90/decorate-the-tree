def _yes_or_no(text):
    while True:
        choice = input(f'{text} (y/n): ').lower().strip()
        if choice in {'y', 'n', 'yes', 'no'}:
            return choice[0] == 'y'
        print('Invalid choice, please try again.')

if _yes_or_no('Here is a yes or no question.'):
    print('Got a yes response')
else:
    print('Got a no')