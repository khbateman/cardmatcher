import math

class Card:
    CARD_WIDTH = 9
    CARD_HEIGHT = 7
    word = None
    word_visible = False

    card_top = " " + "_" * CARD_WIDTH + " "
    card_bottom = " " + "-" * CARD_WIDTH + " "
    card_side = "|" + (" " * CARD_WIDTH ) + "|"

    def word_spacing(self, word):
        gap = self.CARD_WIDTH - len(word)
        if (gap % 2) == 0: # if total spaces are even
            first_spaces = " " * (int(gap/2)) 
            second_spaces = " " * (int(gap/2)) 
        else:
            first_spaces = " " * (int(gap/2) + 1)
            second_spaces = " " * (int(gap/2))
        
        return f'|{first_spaces}{word}{second_spaces}|'
        
    def word_line(self):
        if self.word_visible:
            return self.word_spacing(self.word)
        else:
            return self.word_spacing("???")
    
    def card_frame(self):
        return self.card_top + ("\n" + self.card_side)*(int(self.CARD_HEIGHT/2)) + "\n" + self.word_line() + ("\n" + self.card_side)*(int(self.CARD_HEIGHT/2)) + "\n" + self.card_bottom

    def __init__(self, word):
        self.word = word
        self.card_frame()
        
    def __eq__(self, other):
        return self.word == other.word
    
    def __str__(self):
        return self.card_frame()

if __name__ == '__main__':
    test_card = Card("dog")
    test_card.word_visible = False
    print(test_card)
    print(test_card.word_visible)
    test_card.word_visible = True
    print(test_card)
    print(test_card.word_visible)

