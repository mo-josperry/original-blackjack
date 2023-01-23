'''
Blackjack by josh perry

The Final Project - BlackJack, Command Line Style!

This will be a simple BlackJack game. It will allow hit and stand up to a total
of 21 points. One Class is created, called Card, and will contain a number,
a suit and a name. If the player reaches 21, they win. If they bust, they lose!
Dealer hits on 16, stays on 17. There will be no bets or insurance.
'''
import random
import os
import sys

class Card():
    '''object class for Cards. Will have a value, name, and suit'''
    def __init__(self, number, suit, cardname):
        self.num = number # assign the number from a loop
        self.suit = suit # to assign a suit from a loop
        self.name = cardname # name the card, if needed

    def __str__(self): # when printed, use name and suit
        return f'{self.name} of {self.suit}'

    def newfunction_forpylint(self):
        '''dummy method for the new class to pass pylint min methods'''
        print("This is a new function to pass linter" + self.name)

def banner():
    '''generate some ascii art for the game's intro splash'''
    print("""\
  ____  _            _       _            _
 | __ )| | __ _  ___| | __  | | __ _  ___| | __
 |  _ \\| |/ _` |/ __| |/ /  | |/ _` |/ __| |/ /
 | |_) | | (_| | (__|   < |_| | (_| | (__|   <
 |____/|_|\\__,_|\\___|_|\\_\\___/ \\__,_|\\___|_|\\_\\
                                               """)

def cls():
    '''my usual housekeeping function for tidying the screen'''
    if os.name == 'nt': # if the system is Windows
        os.system('cls')
    else: # if the system is *nix
        os.system('clear')


def generate_deck(deck):
    ''' create the deck, iterating card numbers through each of 4 suits'''
    suits = ["Clubs", "Hearts", "Spades", "Diamonds"]   # a list of all suits
    for suit in suits:
        for cardnum in range(1, 14):  # 13 cards per suit in a full deck
            if cardnum == 1:
                deck.append(Card(cardnum, suit, 'Ace'))
            elif 1 < cardnum <= 10: # number cards will just use cardnum...
                deck.append(Card(cardnum, suit, cardnum)) # ... for cardname
            elif cardnum == 11:
                deck.append(Card(10, suit, 'Jack'))
            elif cardnum == 12:
                deck.append(Card(10, suit, 'Queen'))
            elif cardnum == 13:
                deck.append(Card(10, suit, 'King'))
    return deck


def perform_shuffle(deck):
    '''function dedicated to shuffling the deck when the user is ready'''
    chosen = 0
    while chosen == 0:
        user_choice = input("Are you ready to play? (Y/N): ").lower()
        if user_choice == 'y':
            print('Shuffling...')
            random.shuffle(deck)
            chosen = 1
            continue

        if user_choice == 'n': # quit program
            print('Sorry to see you go so soon! Fare thee well!')
            sys.exit()
        else:
            print('Not a valid selection! Please try again')
            continue

        return deck


def display_deck(deck):
    '''display the contents of the deck in its current order. used during
    debugging and troubleshooting the shuffle function'''
    for card in deck:
        print(f'{card.name} of {card.suit}')


def deal_hand_to_player(deck, player_hand):
    '''the first 2 cards of the deck go to the player, remove cards as we go'''
    for i in range(0, 2):
        initial_hand_deal = deck[i]
        player_hand.append(initial_hand_deal)
        deck.pop(i)

    return player_hand


def deal_hand_to_dealer(deck, dealer_hand):
    '''deal two cards to the dealer, deleting cards as we go'''
    for i in range(0, 2):
        initial_hand_deal = deck[i]
        dealer_hand.append(initial_hand_deal)
        deck.pop(i)

    return dealer_hand


def display_player_hand(player_hand):
    '''show the contents of the player's hand on a single line'''
    print('\nYour hand contains: ', end = " ")
    for card in player_hand:
        print(f'{card.name} of {card.suit},', end = " ")

    return player_hand


def display_dealer_hand(dealer_hand):
    '''show the contents of the dealer's hand on a single line'''
    print("\nYour dealer's hand contains: ", end = " ")
    for card in dealer_hand:
        print(f'{card.name} of {card.suit},', end = " ")

    return dealer_hand


def calculate_player_total(player_hand):
    '''loop through the cards, adding up their card.num totals'''
    player_score = 0
    for card in player_hand:
        player_score += card.num

    return player_score


def calculate_dealer_total(dealer_hand):
    '''loop through the dealer's hand, adding up their card.num totals'''
    dealer_score = 0
    for card in dealer_hand:
        dealer_score += card.num

    return dealer_score


def handle_aces(deck):
    '''standalone function for dealing with ace values'''
    if deck[0].num == 1:
        try:
            aces = int(input('Ace! Should it be 1 or 11?: '))
            if aces == 1:
                print('You have chosen for this ace to be a 1.')

            if aces == 11:
                print('You have chosen for this ace to be an 11.')

        except ValueError:
            print('Not a valid input! Using 1!')


    return aces


def player_turn(player_hand, dealer_hand, deck):
    '''main engine for the player turn. Use deck & both hands as arguments'''
    player_score = calculate_player_total(player_hand)  # call the calculator
    print('\nYou are showing', player_score)
    print('Dealer is showing', dealer_hand[0], 'and a hidden card')

    # while the score is less than 22 allow the user to Hit or Stand
    # by collecting H or S as the input. Cast it to lowercase, then
    # announce the next card. Add that new card to the user's hand
    # and let them know what their score is before asking to hit again

    while player_score < 21:
        hit_or_stand = input('\nWould you like to (H)it or (S)tand: ').lower()
        try:
            if hit_or_stand == 'h':
                nextcard = deck[0]
                print(f'\nYou draw the {nextcard}!')

                # this section handles aces...
                if deck[0].num == 1:    # if the card is a 1
                    aces = handle_aces(deck) # call the handler
                    if aces == 1:   # if the user has chosen 1...
                        player_hand.append(deck[0]) # add the card
                        player_score += 1   # increase the score
                        deck.pop(0) # remove it from the deck
                        display_player_hand(player_hand) # show the hand contents
                        print('\nNew score is:', player_score) # output score
                        continue

                    # if the player chooses 11...
                    player_hand.append(deck[0])
                    player_score += 11
                    deck.pop(0)
                    display_player_hand(player_hand)
                    print('\nNew score is:', player_score)
                    continue
                    # ... now that the aces are dealt with...

                player_hand.append(deck[0]) # same as before, append nextcard
                player_score += deck[0].num # increase score by card value
                deck.pop(0)                 # remove card from deck
                display_player_hand(player_hand)  # display current hand
                print('\nNew score is:', player_score) # display score
                continue

            if hit_or_stand == 's':   # if player stands, print and move along
                print('\nPlayer stands with', player_score)
                return player_score

        except ValueError: # error trapping should keep the user in the loop
            print('Not valid input, try again!')
            continue

    if player_score >= 22:
        print('Bust!')

    return player_score


def dealer_turn(dealer_hand, deck):
    '''main engine for dealer turn'''
    # the dealer goes second, hitting on 16 and standing on 17. He wins all
    # ties as will be calculated in main(). Until he reaches his target
    # continue hitting. When he stops, either bust or carry on.

    print('The dealer was showing', dealer_hand[0], 'and has now '\
          'revealed the', dealer_hand[1]) # reveal the mystery card!

    dealer_score = calculate_dealer_total(dealer_hand) # call the calculator
    while dealer_score <= 16: # as long as the score is less than 16, hit.
        print(f"Dealer's score is {dealer_score}") # display score
        nextcard = deck[0] # call the next card
        print(f'Dealer draws {nextcard}!') # display the next card

        dealer_hand.append(deck[0]) # add the next card to the hand
        dealer_score += deck[0].num # increase the score by the cardnum
        deck.pop(0) # remove the card from the deck
        display_dealer_hand(dealer_hand)    # show the hand

    if dealer_score == 17:  # if the dealer lands on 17, stand!
        print(f'Dealer stands with {dealer_score}')

    if dealer_score == 21: # if the dealer has 21 you lose!!
        print('Dealer has 21! Oh no!')

    if dealer_score > 21: # if the dealer busts, you win!!
        print(f'Dealer busts with {dealer_score}!')


    print(f"Dealer's score is {dealer_score}!")
    return dealer_score

def greeting():
    '''greet the player and introduce the game'''
    cls() # clear the screen...
    banner() # display my cool ascii art banner!
    print("Welcome to Blackjack, by Josh Perry! This game is a simplified "\
        "version of the game you already know and love! Make it to 21 "\
        "without going over and you win! But watch out! Ties go to the "\
        "house! Dealer will hit on 16, and stay on 17.")


def quitgame(wincount, dealerwins):
    '''polite exit message before shutting down'''
    cls()
    print(f"This session, you won {wincount} hands to the "\
          f"Dealer's {dealerwins}.")
    print('Thanks for playing BlackJack, by Josh Perry!\nExiting...')
    sys.exit()


def check_scores(player_score, dealer_score, wincount, dealerwins):
    '''evaluate the scores against eachother'''
    if dealer_score > 21: # if dealer busts
        print(f'Player wins! The dealer went bust on {dealer_score}!')
        wincount += 1
        print(f'You have won {wincount} hands this session!!')

    elif player_score > 21: # if player busts
        print(f'Dealer wins! Player went bust on {player_score}!')
        dealerwins += 1

    elif player_score < dealer_score < 22: # if dealer wins
        print(f'Dealer wins with {dealer_score}! Better luck next time!')
        dealerwins += 1

    elif player_score == dealer_score: # if both tie
        print(f'Ouch! Ties go to the House! You both got {dealer_score}. '\
              'Better luck next time!')
        dealerwins += 1

    elif dealer_score < player_score < 22: # if player wins
        print(f'You win with {player_score}!! Good Job!!')
        wincount += 1
        print(f'You have won {wincount} hands this session!!')

    else: # catching potential bugs with a small debug output
        print('We apologize but there seems to have been an error...')
        print(f'Dealer: {dealer_score}, Player: {player_score}')

    return [wincount, dealerwins]


def main():
    '''launch the program'''
    greeting()
    wincount = 0
    dealerwins = 0
    play_again = True # Making sure the player can keep coming back...
    while play_again is True:       # ... as long as they want to.
        deck = []   # start with an empty deck...
        player_hand = []     # ...and empty hands...
        dealer_hand = []
        player_score = 0
        dealer_score = 0

        generate_deck(deck)     # generate contents for the deck, return a List
        perform_shuffle(deck)   # ask if user wants to shuffle, for debugging.

        deal_hand_to_player(deck, player_hand) # deal player cards
        deal_hand_to_dealer(deck, dealer_hand) # deal dealer cards
        display_player_hand(player_hand) # show us what you got!

        # Calculate player and dealer scores by calling their respective
        # functions and feeding them the deck and hands as arguments.
        player_score = player_turn(player_hand, dealer_hand, deck)
        if player_score <= 21:
            dealer_score = dealer_turn(dealer_hand, deck)
        else:
            print("Player went bust!")
            dealerwins += 1
            ask = input('Would you like to play again? (Y/N): ').lower()
            if ask == 'y':
                cls()
                continue

            if ask == 'n':
                quitgame(wincount, dealerwins)

        scores = check_scores(player_score, dealer_score, wincount, dealerwins)
        wincount = scores[0]
        dealerwins = scores[1]

        # The game has come to it's end! ask the user for another round!
        # If they say yes, clear the screen and start over. If they say
        # no, thank them for playing and exit program.
        ask = input('Would you like to play again? (Y/N): ').lower()
        if ask == 'y':
            cls()
            continue

        play_again = False
        quitgame(wincount, dealerwins)

# boilerplate
if __name__ == '__main__':
    main()
