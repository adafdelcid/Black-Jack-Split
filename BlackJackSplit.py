import random

'''
Black Jack game
By: Ada Del Cid
Based on Project 2 of the Udemy course: 'Complete Python Bootcamp: Go from zero to hero in Python 3' by Jose Portilla
'''

SUITS = ['Hearts', 'Clubs', 'Spades', 'Diamonds']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10,'Ace': 11}

playing = True

class Chips():
    def __init__(self, total=100):
        '''Player's chips and bet'''
        self.total = total
        self.bet = 0

    def win_bet(self):
        '''adjusts player's total if the player wins bet'''
        self.total += self.bet

    def lose_bet(self):
        '''adjusts player's total if the player loses bet'''
        self.total -= self.bet

class Card():
    def __init__(self, suit, rank):
        '''Creates an object card given suit and rank'''
        self.suit = suit
        self.rank = rank

    def __str__(self):
        '''returns string that describes card object'''
        return self.rank + ' of ' + self.suit

class Deck():
    def __init__(self):
        '''Creates a deck of cards'''
        self.deck = []
        for suit in SUITS:  # for each suit
            for rank in RANKS:  # for each rank
                self.deck.append(Card(suit, rank))  # add a new card to the deck

    def shuffle(self):
        '''shuffles the deck of cards'''
        random.shuffle(self.deck)

    def deal(self):
        '''deals one card from the cards remaining in the deck'''
        card_dealt = self.deck.pop()
        return card_dealt

class Hand():
    def __init__(self):
        '''Saves the player or dealer's card hand, their value and the number of aces'''
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        '''Adds a card to the player or dealer's hand'''
        self.cards.append(card)
        self.value += VALUES[card.rank]
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_aces(self):
        '''Adjusts the value if the dealer or player go over 21 and have aces'''
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

def take_bet(chips):
    '''Takes player's bet'''
    while True:
        try:
            chips.bet = int(input("Please place a bet:"))
        except:
            print("Please place a valid bet, must be an integer!")
        else:
            if chips.total >= chips.bet:
                break
            else:
                print("Sorry your bet cannot exceed your available chips " + str(chips.total))

def hit(deck, hand):
    '''Adds cards to hand and updates value'''
    card = deck.deal()
    hand.add_card(card)
    hand.adjust_for_aces()

def hit_or_stand(deck, hand):
    '''Asks player is they want to hit or stand'''
    global playing
    while True:
        user_input = input("Player, do you want to hit ('h') or stand ('s')?")

        if len(user_input) != 0 and user_input[0].lower() == 'h':
            hit(deck, hand)
        elif len(user_input) != 0 and user_input[0].lower() == 's':
            print("Player stands, Dealer is playing.")
            playing = False
        else:
            print("Sorry, please try again.")
            continue
        break

def show_some(player1, dealer, player2=None):
    '''Shows all player's card and 1 of the dealer's cards'''
    print("\nDealer's Hand:")
    print("<Hidden card>")
    print("", dealer.cards[1])
    if player2 != None:
        print("\nPlayer's 1st Hand:", *player1.cards, sep='\n')
        print("\nPlayer's 2nd Hand:", *player2.cards, sep='\n')
    else:
        print("\nPlayer's Hand:", *player1.cards, sep='\n')

def show_all(player1, dealer, player2=None):
    '''Shows all the cards of both dealer and player'''
    print("\nDealer's Hand:", *dealer.cards, sep='\n')
    print("Dealer's Hand:", dealer.value)
    if player2 != None:
        print("\nPlayer's 1st Hand:", *player1.cards, sep='\n')
        print("Player's 1st Hand:", player1.value)
        print("\nPlayer's 2nd Hand:", *player2.cards, sep='\n')
        print("Player's 2nd Hand:", player2.value)
    else:
        print("\nPlayer's Hand:", *player1.cards, sep='\n')
        print("Player's Hand:", player1.value)


def player_busts(chips):
    '''Displays that player busted and updates chips'''
    print("\nPlayer busts!")
    chips.lose_bet()

def player_wins(chips):
    '''Displays that player wins and updates chips'''
    print("\nPlayer wins!")
    chips.win_bet()

def dealer_busts(chips):
    '''Displays that dealer busts and updates player's chips'''
    print("\nDealer busts!")
    chips.win_bet()

def dealer_wins(chips):
    '''Displays that dealer wins and updates player's chips'''
    print("\nDealer wins!")
    chips.lose_bet()

def push():
    '''Displays that it's a tie'''
    print("\nDealer and Player tie! It's a push.")

def split_prompt():
    '''Asks player if they would like to split their hand'''
    while True:
        split_input = input("Player would you like to split? Enter 'y' or 'n'. ")

        if len(split_input) != 0 and split_input[0].lower() == 'y':
            print("Player splits. Doubling bet.")
            return True
        elif len(split_input) != 0 and split_input[0].lower() == 'n':
            print("Player does not split.")
            return False
        else:
            print("Invalid entry, please try again.")
            continue

if __name__ == "__main__":
    # Saves if current play is the first play or restart
    first = True

    while True:
        print('\nWelcome to BlackJack! Get as close to 21 as you can without going over!')
        print('Dealer hits until she reaches 17. Aces count as 1 or 11.')

        # Create & shuffle the deck, deal two cards to each player
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Set up the Player's chips on first play
        if first:
            player_chips = Chips()  # remember the default value is 100

        # Prompt the Player for their bet
        take_bet(player_chips)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)


        split_input = False  # variable to check if hand was split

        # If player's first two cards are the same, ask player if they wish to split
        if len(player_hand.cards) == 2 and player_hand.cards[0].rank == player_hand.cards[1].rank:
            split_input = split_prompt()
            if split_input:  # double bet
                player_chips.bet *= 2
                if player_chips.bet > player_chips.total:  # if not enough chips to split
                    player_chips.bet /= 2  # reverse bet doubling
                    split_input = False
                    print("Unable to split not enough chips to double bet!")
                else:  # split into two hands
                    player_hand1 = Hand()
                    player_hand1.add_card(player_hand.cards.pop())

                    player_hand2 = Hand()
                    player_hand2.add_card(player_hand.cards.pop())

                    show_some(player_hand1, dealer_hand, player_hand2)

        if split_input:  # run this if the initial hand was split
            while playing:
                # Prompt for Player to Hit or Stand
                print("\nPlayer's 1st Hand")
                hit_or_stand(deck, player_hand1)

                # Show cards (but keep one dealer card hidden)
                show_some(player_hand1, dealer_hand, player_hand2)

                # If player's hand exceeds 21, run player_busts() and break out of loop
                if player_hand1.value > 21:
                    print('\nPlayer busts with Hand 1!')
                    break

            playing = True
            while playing:
                print("\nPlayer's 2nd Hand")
                hit_or_stand(deck, player_hand2)

                # Show cards (but keep one dealer card hidden)
                show_some(player_hand1, dealer_hand, player_hand2)

                # If player's hand exceeds 21, run player_busts() and break out of loop
                if player_hand2.value > 21:
                    print('\nPlayer busts with Hand 2!')
                    break

            # If player's hand exceeds 21, run player_busts() and break out of loop
            if player_hand1.value > 21 and player_hand2.value > 21:
                player_busts(player_chips)

            # If at least one hand did not bust
            else:
                # if one of the split hands busts, reduce bet
                if player_hand1.value > 21 or player_hand2.value > 21:
                    player_chips.bet /= 2
                    player_chips.lose_bet()

                # dealer's turn
                while dealer_hand.value < 17:
                    hit(deck, dealer_hand)

                # Show all cards
                show_all(player_hand1, dealer_hand, player_hand2)

                # Run different winning scenarios
                if dealer_hand.value > 21:  # dealer busts
                    dealer_busts(player_chips)

                # dealer's hand is greater than both of the player's hands
                elif dealer_hand.value > player_hand1.value and dealer_hand.value > player_hand2.value:
                    dealer_wins(player_chips)

                # dealer's hand is less than both of the player's hands
                elif dealer_hand.value < player_hand1.value and dealer_hand.value < player_hand2.value:
                    player_wins(player_chips)  # both of the player's hands win

                # dealer's hand is greater than hand1 and smaller than hand2
                elif dealer_hand.value > player_hand1.value and dealer_hand.value < player_hand2.value:
                    # if the larger hand was a bust (>21)
                    if player_hand2.value > 21:  # bet was already reduced line 260-262
                        dealer_wins(player_chips)
                    # if larger hand did not go over 21
                    else:
                        player_chips.bet /= 2  # half bet, because only one hand won
                        player_wins(player_chips)
                        player_chips.lose_bet()

                # dealer's hand is greater than hand2 and smaller than hand1
                elif dealer_hand.value < player_hand1.value and dealer_hand.value > player_hand2.value:
                    # if the larger hand was a bust (>21)
                    if player_hand1.value > 21:  # bet was already reduced line 260-262
                        dealer_wins(player_chips)
                    # if larger hand did not go over 21
                    else:
                        player_chips.bet /= 2  # half bet, because only one hand won
                        player_wins(player_chips)
                        player_chips.lose_bet()

                # if both of the player's hands and dealer's hand are equal
                elif dealer_hand.value == player_hand1.value and dealer_hand.value == player_hand2.value:
                    push()

                # if dealer's hand is equal to one of the player's hand
                elif dealer_hand.value == player_hand1.value or dealer_hand.value == player_hand2.value:
                    player_chips.bet /= 2  # half bet because one hand was a push
                    # if dealer's hand is greater than the other player's hand
                    if dealer_hand.value > player_hand1.value or dealer_hand.value > player_hand2.value:
                        dealer_wins(player_chips)
                    else:
                        if player_hand1.value > 21 or player_hand2.value > 21:  # if the other player's hand is a bust
                            push()  # bet lost was already reduce lines 260-262
                        else:  # if dealer's hand is less than the other player's hand
                            player_wins(player_chips)

        else:  # run this if initial hand wasn't split
            while playing:  # recall this variable from our hit_or_stand function

                # Prompt for Player to Hit or Stand
                hit_or_stand(deck, player_hand)

                # Show cards (but keep one dealer card hidden)
                show_some(player_hand, dealer_hand)

                # If player's hand exceeds 21, run player_busts() and break out of loop
                if player_hand.value > 21:
                    player_busts(player_chips)
                    break

            # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
            if player_hand.value <= 21:

                # dealer's turn
                while dealer_hand.value < 17:
                    hit(deck, dealer_hand)

                # Show all cards
                show_all(player_hand, dealer_hand)

                # Run different winning scenarios
                if dealer_hand.value > 21:
                    dealer_busts(player_chips)

                elif dealer_hand.value > player_hand.value:
                    dealer_wins(player_chips)

                elif dealer_hand.value < player_hand.value:
                    player_wins(player_chips)

                else:
                    push()

        # Inform Player of their chips total
        print("\nPlayer's winnings stand at", player_chips.total)

        # Check if player wants to play again
        while True:
            # Ask to play again
            new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")

            if new_game[0].lower() == 'y':
                if player_chips.total > 0:  # if player still has chips
                    first = False
                    playing = True
                    player_chips = Chips(player_chips.total)
                else:  # if player has no chips left, ask if they would like to restart
                    replay = input("Player is out of chips! Would you like to reset and play again? Enter 'y' or 'n'")
                    if replay[0].lower() == 'y':
                        first = True
                        playing = True
                    else:  # set no new game
                        new_game = 'n'
                break  # break from second while loop

            elif new_game[0].lower() == 'n':
                break
            else:
                print("Invalid input, try again!")
                continue

        if new_game[0].lower() == 'y':  # restart new game
            continue
        elif new_game[0].lower() == 'n':  # break out of main while loop, no new game
            print("Thanks for playing!")
            break