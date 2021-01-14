# TODO - make sure people have to enter at least 2 cards
# TODO - fix empty entries

from cards import Card
import random

SPACES = '               '
CARD_MATCHER ='''            .------..------..------..------.
            |C.--. ||A.--. ||R.--. ||D.--. |
            | :/\: || (\/) || :(): || :/\: |
            | :\/: || :\/: || ()() || (__) |
            | '--'C|| '--'A|| '--'R|| '--'D|
            `------'`------'`------'`------'
███    ███  █████  ████████  ██████ ██   ██ ███████ ██████  
████  ████ ██   ██    ██    ██      ██   ██ ██      ██   ██ 
██ ████ ██ ███████    ██    ██      ███████ █████   ██████  
██  ██  ██ ██   ██    ██    ██      ██   ██ ██      ██   ██ 
██      ██ ██   ██    ██     ██████ ██   ██ ███████ ██   ██ '''

def get_cards():
    GAME_MAX = 6
    entry = ""
    entries = []
    welcome = f'\n\n\n\n\n\n\n\n\n\n\n{SPACES}                      Welcome to\n' + SPACES + f"\n{SPACES}".join(CARD_MATCHER.splitlines()) + f"\n\n{SPACES}To get going, please give us the words you'd like to appear on the cards\n\n{SPACES}You can enter up to {GAME_MAX} words\n\n{SPACES}When you're ready to start the game type GO and hit ENTER"


    def show_welcome(*args):
        print(welcome)
        print('\n' * (GAME_MAX - len(entries)))
        
        for i, entry in enumerate(entries, 1):
            print('     WORD #' + str(i) + ' - ' + entry)

        
    
    while entry.upper() != "GO" or len(entries) < 2:
        if len(entries) < GAME_MAX:
            
            show_welcome()
            
            if len(entries) < 2:
                print(f'{SPACES}You need at least 2 words to play')
                entry = input(f'{(len(SPACES) - 4) * " "}>>> ')
            else:
                entry = input(f'\n{(len(SPACES) - 4) * " "}>>> ')

            while len(entry) > (Card.CARD_WIDTH - 2) or entry == "":
                if entry == "":
                    show_welcome()
                    entry = str(input(f"{SPACES}Entries can't be blank.\n{(len(SPACES) - 4) * ' '}>>> "))
                elif (len(entry) > Card.CARD_WIDTH - 2):
                    show_welcome()
                    entry = str(input(f'{SPACES}Please enter a word with less than {Card.CARD_WIDTH - 2} characters.\n{(len(SPACES) - 4) * " "}>>> ')) 
                else:
                    continue
            
            if entry.upper() != "GO":
                entries.append(entry)

        else:
            break
    
    show_welcome()
    input(f"\n{SPACES}That's {len(entries)} entries. Let's start the game! To start, hit ENTER   ")
    return entries


class Game:

    cards = []
    game_board = []
    mapped_values = {}
    face_up_cards = []
    game_won = False
    error_message = "\n"

    def add_cards(self, *args):
        for card in args:
            self.cards.append(card)

    def create_board(self):
        num_remaining_cards = len(self.cards)
    
        for card in range(len(self.cards)):
            random_index = random.randint(0,num_remaining_cards-1)
            self.game_board.append(self.cards.pop(random_index))
            num_remaining_cards -= 1

    def create_mapped_values(self):
        length = len(self.game_board)
        
        for i in range(length):
            if i < length/2:
                self.mapped_values["A" + str(i+1)] = i
            else:
                self.mapped_values["B" + str(i - int(length/2) + 1)] = i
                    
    def print_row(self, label, *args):
        lines = len(args[0].card_frame().splitlines())
        space = "   "

        for row in range(lines):
            temp_string = ""
            
            if row == int(lines/2):
                for card in args:
                    temp_string += card.card_frame().splitlines()[row] + space

                print("   " + label + "  " + temp_string)
            else:
                for card in args:
                    temp_string += card.card_frame().splitlines()[row] + space

                print(SPACES + "   "+ temp_string)
    
    def show_board(self):
        print('\n\n\n\n\n\n\n\n\n\n\n')

        length = int(len(self.game_board)/2)
        
        temp_str = ""

        for i in range(length):
            temp_str += str(i + 1) + (Card.CARD_WIDTH * " ") + "    "
        
        print(SPACES + "        " + temp_str)
        self.print_row((len(SPACES)-3)*" " + "A", *self.game_board[0:length])
        self.print_row((len(SPACES)-3)*" " + "B", *self.game_board[length:])
        print("")
    
    def reset_board(self):
        for item in self.game_board:
            item.word_visible = False
        self.face_up_cards.clear()

    def guess(self):
        def flip_card(location):
            self.game_board[self.mapped_values[location]].word_visible = True
            self.show_board()

        def not_valid_location(*args):
            if len(args) == 1:
                self.error_message = f"{SPACES}       >>  {args[0]}  <<\n{SPACES}Sorry that's not a valid location. Please try again."
            else:
                self.error_message = f"{SPACES}Card 1 >>  {args[0]}\n{SPACES}       >>  {args[1]}  << Sorry that's not a valid location. Please try again."

        def not_a_match():
            input(SPACES + "Whoops, those don't match! Try again! Hit ENTER to continue.   ")
            self.reset_board()
            
        def show_both_cards(guess_one, guess_two):
            self.show_board()
            print(f'{SPACES}Card 1 >>  {guess_one}\n{SPACES}Card 2 >>  {guess_two}')
        
        def reset_error():
            self.error_message = "\n"
        
        def already_flipped_message(*args):
            if len(args) == 1:
                self.error_message = f"\n{SPACES}{args[0]} is already flipped. Please enter a new value."
            elif args[0] == args[1]:
                self.error_message = f"{SPACES}Card 1 >>  {args[0]}  << {args[1]} was your first guess.\n{SPACES}                  Please enter a new value."
            else:
                self.error_message = f"{SPACES}Card 1 >>  {args[0]}\n{SPACES}{args[1]} is already flipped. Please enter a new value."


        print(self.error_message)
        guess_one = str(input(f"{SPACES}Card 1 >>  ")).upper()
        reset_error()

        # makes sure guess 1 is valid entry
        if guess_one in self.mapped_values.keys(): 
            
            # if it's valid, make sure card hasn't already been flipped
            if guess_one not in self.face_up_cards:
                flip_card(guess_one)

                guess_two = str(input(f'\n{SPACES}Card 1 >>  {guess_one}\n{SPACES}Card 2 >>  ')).upper()

                # error checking second guess
                while guess_two not in self.mapped_values.keys() or guess_two in self.face_up_cards or guess_two == guess_one:
                    
                    # if it's not valid
                    if guess_two not in self.mapped_values.keys():
                        self.show_board()
                        not_valid_location(guess_one, guess_two)
                        print(self.error_message)
                        guess_two = str(input(SPACES + "Card 2 >>  ")).upper()
                        reset_error()
                    
                    # if it's valid, but it's already flipped,              
                    elif guess_two in self.face_up_cards or guess_two == guess_one:
                        self.show_board()
                        already_flipped_message(guess_one, guess_two)
                        print(self.error_message)
                        guess_two = str(input(SPACES + "Card 2 >>  ")).upper()
                        reset_error()
                                
                else:
                    if guess_two in self.mapped_values.keys():
                        flip_card(guess_two)

                        if self.game_board[self.mapped_values[guess_one]] == self.game_board[self.mapped_values[guess_two]]: 
                            self.face_up_cards.append(guess_one)
                            self.face_up_cards.append(guess_two)
                            pass
                        else:
                            show_both_cards(guess_one, guess_two)
                            not_a_match()
                    else:
                        show_both_cards(guess_one, guess_two)
                        not_valid_location()
            else: # if it has been flipped already
                already_flipped_message(guess_one)
        else: # if entry isn't valid, error message log
            not_valid_location(guess_one)

    def check_game_over(self):
        cards_correct = []
        for card in self.game_board:
            cards_correct.append(card.word_visible)
        if all(cards_correct):
            self.game_won = True
        else:
            cards_correct.clear()
    
    def game_won_display(self):
        print('''\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
                                        CONGRATULATIONS!!
        ____    ____   ______    __    __     ____    __    ____  __  .__   __.  __   __   __  
        \   \  /   /  /  __  \  |  |  |  |    \   \  /  \  /   / |  | |  \ |  | |  | |  | |  | 
         \   \/   /  |  |  |  | |  |  |  |     \   \/    \/   /  |  | |   \|  | |  | |  | |  | 
          \_    _/   |  |  |  | |  |  |  |      \            /   |  | |  . `  | |  | |  | |  | 
            |  |     |  `--'  | |  `--'  |       \    /\    /    |  | |  |\   | |__| |__| |__| 
            |__|      \______/   \______/         \__/  \__/     |__| |__| \__| (__) (__) (__)\n\n\n\n\n\n\n\n\n\n\n\n\n''')


    
    def start_game(self):
        while not self.game_won:
            self.show_board()
            self.guess()
            self.check_game_over()
        
        self.game_won_display()

    def __init__(self, *args):
        for arg in args:
            self.add_cards(Card(arg))
            self.add_cards(Card(arg))
        self.create_board()
        self.create_mapped_values()


if __name__ == '__main__':
    cards = get_cards()
    
    game = Game(*cards)
    game.start_game()


