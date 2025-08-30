from VividText import VividText as vt
import random
from rich.console import Console

from .utils import cc

class Game:
    def __init__(self, player_pocket):
        self.player_money = player_pocket
        self.bet = 0

        self.tp = vt(bold=True, sleep=.03)
        self.deck_color = Console()

        self.cards = {
            '2': 4, '3': 4, '4': 4,
            '5': 4, '6': 4, '7': 4, '8': 4,
            '9': 4, '10': 4, 'Jack': 4, 'Queen': 4,
            'King': 4, 'Ace': 4
        }

        self.card_value = {
            '2': 2, '3': 3, '4': 4,
            '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, '10': 10, 'Jack': 11,
            'Queen': 12, 'King': 13, 'Ace': [1, 11]
        }

        self.card_names = list(self.cards.keys())
        self.current_deck = self.cards.copy()

        self.dealer_deck = []
        self.player_deck = []

    #* Grab the player's winnings
    def get_winnings(self) -> float:
        return self.player_money

    #* Reset player pocket
    def reset_player_pocket(self, new_amount):
        self.player_money = new_amount

    #* Draw a card
    def draw_card(self):
        available_cards = [card for card in self.card_names if self.current_deck[card] > 0]
        if not available_cards:
            return None        # Check if the deck is empty

        choice = random.choice(available_cards)
        self.current_deck[choice] -= 1
        return choice

    #* Get the score of x's card
    def calculate_score(self, cards) -> int:
        score = 0
        ace_count = 0

        for card in cards:
            if card == 'X':
                continue

            if card == 'Ace':
                ace_count += 1
                score += 11
            
            else:
                score += self.card_value[card]
        
        while score > 21 and ace_count > 0:
            score -= 10
            ace_count -= 1
        
        return score

    #* Draw the table
    def draw_table(self, dealer_cards, player_cards):
        length_of_deck = 18
        rows = '-' * length_of_deck
        inner_width = length_of_deck - 2

        #* Map full card names to initials
        def card_to_initial(card):
            initials = {
                'Ace': 'A',
                'Queen': 'Q',
                'King': 'K',
                'Jack': 'J',
            }
            return initials.get(card, card)  # default to card itself if not a face card

        #* Convert cards to initials first
        dealer_display = [card_to_initial(c) for c in dealer_cards]
        player_display = [card_to_initial(c) for c in player_cards]

        #* Join cards with space, plain text
        dealer_plain = ' '.join(dealer_display)
        player_plain = ' '.join(player_display)

        #* Center plain text strings
        dealer_centered = dealer_plain.center(inner_width)
        player_centered = player_plain.center(inner_width)

        def add_markup(text):
            return ''.join(
                f'[bold white]{c}[/]' if c != ' ' else ' '
                for c in text
            )

        dealer_row = add_markup(dealer_centered)
        player_row = add_markup(player_centered)

        self.deck_color.print(rows, style='bold white')
        self.deck_color.print(f"|{dealer_row}|", markup=True)
        self.deck_color.print(rows, style='bold white')
        self.deck_color.print(f"|{player_row}|", markup=True)
        self.deck_color.print(rows, style='bold white')

        dealer_score = self.calculate_score(dealer_cards)
        player_score = self.calculate_score(player_cards)

        self.deck_color.print(f"[bold white]Your bet: {self.bet}[/]", markup=True)
        self.deck_color.print(f"[bold white]Dealer Score: {dealer_score}[/]", markup=True)
        self.deck_color.print(f"[bold white]Your Score: {player_score}[/]", markup=True)

    #* Config Player wallet
    def winnings(self, bet, multi):
        if type(multi) != int:
            if multi == 'Draw':
                self.player_money += bet
                return
            self.player_money -= bet

        else:
            bet *= multi
            self.player_money += bet

    #* Make the dealer draw till blackjack or bust or higher cards
    def dealer_draw(self, player_score):
        self.dealer_deck.remove("X")

        done = False
        won = False
        draw = False
        while not done:
            card = self.draw_card()
            self.dealer_deck.append(card)

            score = self.calculate_score(self.dealer_deck)
            if score > player_score and score < 22:
                won = True
                done = True

            elif score > 22:
                done = True
            
            elif score == 21 and score == player_score:
                draw = True
                done = True

            else:
                pass

        self.draw_table(self.dealer_deck, self.player_deck)

        if won:
            self.tp.typewriter("The dealer has won!")
            if score == 21 and self.bet_on_black:
                self.tp.typewriter("You earned money on your side bet!")
                self.winnings(self.side_bet, 1.5)
        
        elif draw:
            self.tp.typewriter("You have drawed!")
            self.winnings(self.bet, 'Draw')

        else:
            self.tp.typewriter("You have won!")
            self.winnings(self.bet, 2)

    #* Get the player bet
    def get_bet(self):
        run = True
        while run:
            self.tp.typewriter(f"Amount of money in your wallet: ${self.player_money:.2f}")
            bet_amount = self.tp.inputTypewriter("Enter an amount of money you would like to bet")

            if bet_amount.isdigit():
                bet_amount = int(bet_amount)
                if bet_amount <= self.player_money:
                    self.bet = bet_amount
                    self.player_money -= self.bet
                    cc()
                    run = False

                else:
                    self.tp.typewriter("You don't have that much money in your wallet!")
                    self.tp.inputTypewriter("Press Enter to continue.", end='')
                    cc()
            
            else:
                self.tp.typewriter('You have to enter in a amount of money! (x.xx)')
                self.tp.inputTypewriter("Press Enter to continue.", end='')
                cc()

    #* Play a round of blackjack
    def play(self):
        #* Get the bet amount
        self.get_bet()

        #* Reset Player / Dealer Deck
        self.dealer_deck = []
        self.player_deck = []

        #* Start with setting up player / dealer deck
        for _ in range(2):
            card = self.draw_card()
            self.player_deck.append(card)
        
        card = self.draw_card()
        self.dealer_deck.append(card)
        self.dealer_deck.append("X")

        #* Game Variables
        self.insurance = False
        self.bet_on_black = False
        self.side_bet = 0
        self.five_card = False
        self.instant_win = False
        self.lost = False

        #* Check if the player has blackjack right away
        if self.calculate_score(self.player_deck) == 21:
            self.instant_win = True

        if self.instant_win:
            self.tp.typewriter("You hit blackjack!")
            self.winnings(self.bet, 3)
            return
    
        if self.calculate_score(self.dealer_deck) == 11:
            self.insurance = True

        run = True
        while run:
            self.draw_table(self.dealer_deck, self.player_deck)

            if self.calculate_score(self.player_deck) > 21:
                self.tp.typewriter("You have busted!")
                self.lost = True
                self.winnings(self.bet, None)
                run = False
                continue

            print()

            if self.insurance:
                choice = self.tp.inputTypewriter("Would you like to hit, stand, or ask for insurance?")

                if choice == 'Hit' or choice.startswith("H"):
                    new_card = self.draw_card()
                    self.player_deck.append(new_card)
                    self.insurance = False
                    cc()

                elif choice == 'Stand' or choice.startswith("S"):
                    cc()
                    run = False
                    self.insurance = False

                elif choice == 'Insurance' or choice.startswith("I"): 
                    self.insurance = False
                    self.bet_on_black = True
                    while True:
                        amt = self.tp.inputTypewriter("Enter amount of money you would like to put on insurance").title()

                        if amt.isdigit():
                            if amt <= self.player_money:
                                self.player_money -= amt
                                self.side_bet = amt
                            
                            else:
                                self.tp.typewriter("You don't have that much money!")
                                self.tp.inputTypewriter("Press Enter to continue.", end='')
                                cc()

                        else:
                            self.tp.typewriter("That is not a valid option.")
                            self.tp.inputTypewriter("Press Enter to continue.", end='')
                            cc()

                else:
                    self.tp.typewriter("That is not an option.")
                    self.tp.inputTypewriter("Press Enter To Continue.")
                    cc()

            else:
                choice = self.tp.inputTypewriter("Would you like to hit or stand?").title()

                if choice == 'Hit' or choice.startswith("H"):
                    new_card = self.draw_card()
                    self.player_deck.append(new_card)
                    cc()

                elif choice == 'Stand' or choice.startswith("S"):
                    cc()
                    run = False

                else:
                    self.tp.typewriter("That is not an option.")
                    self.tp.inputTypewriter("Press Enter To Continue.")
                    cc()
        
        if not self.lost:
            self.dealer_draw(self.calculate_score(self.player_deck))

    #* Main game loop
    def main(self):
        if self.player_money == 0:
            self.tp.typewriter("You need to have money to play!")
            return
        
        run = True
        while run:
            if self.player_money == 0:
                self.tp.typewriter("You need to have money to play!")
                run = False
                continue

            option = self.tp.inputTypewriter("Would you like to play a round of blackjack?").title()

            if option.startswith("Y"):
                cc()
                self.play()
            
            elif option.startswith("N"):
                run = False
                continue
            
            else:
                self.tp.typewriter("That is not a valid option. (Y/N)")

            self.tp.inputTypewriter("Press Enter to continue.", end='')
            cc()
