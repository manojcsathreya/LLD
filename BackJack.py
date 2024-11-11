import random
import uuid

# Card Class
class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
    
    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def value(self):
        """Returns the value of the card for scoring purposes."""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)


# Deck Class
class Deck:
    def __init__(self):
        self.cards = self.create_deck()
        self.shuffle()

    def create_deck(self):
        """Creates a standard deck of 52 cards."""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [Card(rank, suit) for suit in suits for rank in ranks]

    def shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)

    def deal_card(self):
        """Deals a card from the deck."""
        return self.cards.pop()
    
    def cards_left(self):
        """Returns the number of cards left in the deck."""
        return len(self.cards)


# Player Class
class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = []

    def add_card(self, card: Card):
        """Adds a card to the player's hand."""
        self.hand.append(card)

    def hand_value(self):
        """Calculates the value of the player's hand."""
        value = sum(card.value() for card in self.hand)
        ace_count = sum(1 for card in self.hand if card.rank == 'A')

        # Adjust for aces being worth 1 instead of 11
        while value > 21 and ace_count:
            value -= 10
            ace_count -= 1
        
        return value

    def __repr__(self):
        return f"{self.name}: {', '.join(str(card) for card in self.hand)}"


# Dealer Class
class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")

    def play_turn(self, deck: Deck):
        """Dealer's turn to play. The dealer must hit until they have at least 17."""
        while self.hand_value() < 17:
            print(f"Dealer's hand value is {self.hand_value()}. Dealer hits.")
            self.add_card(deck.deal_card())
        print(f"Dealer's hand value is {self.hand_value()}. Dealer stands.")


# Blackjack Game Class
class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Player")
        self.dealer = Dealer()

    def deal_initial_cards(self):
        """Deals two cards to both the player and the dealer."""
        for _ in range(2):
            self.player.add_card(self.deck.deal_card())
            self.dealer.add_card(self.deck.deal_card())

    def display_hands(self):
        """Displays both the player's and dealer's hands."""
        print(f"Player's hand: {self.player}")
        print(f"Dealer's hand: {self.dealer.hand[0]} and [hidden card]")

    def play(self):
        """Plays the game."""
        self.deal_initial_cards()
        self.display_hands()

        # Player's turn
        while self.player.hand_value() < 21:
            action = input("Do you want to [H]it or [S]tand? ").lower()
            if action == 'h':
                self.player.add_card(self.deck.deal_card())
                print(f"Player's hand: {self.player}")
            elif action == 's':
                break
            else:
                print("Invalid choice. Please choose 'H' to hit or 'S' to stand.")

        # If the player busts
        if self.player.hand_value() > 21:
            print(f"Player busts with {self.player.hand_value()}! Dealer wins.")
            return

        # Dealer's turn
        self.dealer.play_turn(self.deck)
        print(f"Dealer's hand: {self.dealer}")

        # Determine the winner
        player_value = self.player.hand_value()
        dealer_value = self.dealer.hand_value()

        if dealer_value > 21:
            print("Dealer busts! Player wins.")
        elif player_value > dealer_value:
            print("Player wins!")
        elif player_value < dealer_value:
            print("Dealer wins!")
        else:
            print("It's a tie!")


# Main Function
def main():
    print("Welcome to Blackjack!")
    game = BlackjackGame()
    game.play()

if __name__ == "__main__":
    main()
