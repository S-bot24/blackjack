import random
from logo import logo, end

# ASCII art for card suits
HEARTS = '♥'
DIAMONDS = '♦'
CLUBS = '♣'
SPADES = '♠'

# Card ranks and values
CARD_RANKS = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Function to create a new deck of cards
def create_deck():
    ranks = list(CARD_RANKS.keys())
    suits = [HEARTS, DIAMONDS, CLUBS, SPADES]
    return [(rank, suit) for rank in ranks for suit in suits]

# Function to shuffle the deck
def shuffle_deck(deck):
    random.shuffle(deck)

# Function to draw a card from the deck
def draw_card(deck):
    return deck.pop()

# Function to calculate the score of a hand
def calculate_score(hand):
    score = sum(CARD_RANKS[rank] for rank, _ in hand)
    # Handle Aces (count as 11 if it doesn't bust the hand)
    for rank, _ in hand:
        if rank == 'A' and score > 21:
            score -= 10
    return score

# Function to display the player's hand
def display_hand(hand):
    return ', '.join(f'{rank}{suit}' for rank, suit in hand)

# Function to prompt the player for their bet
def get_bet(balance):
    while True:
        try:
            bet = int(input(f"Place your bet (Current balance: ${balance}): "))
            if 0 < bet <= balance:
                return bet
            print("Invalid bet. Please enter a valid amount.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Function to ask the player if they want to play again
def play_again():
    while True:
        play = input("Do you want to play again? (yes/no): ").lower()
        if play in ('yes', 'no'):
            return play == 'yes'
        print("Invalid input. Please enter 'yes' or 'no'.")

# Function to run the game
def blackjack_game():
    print(logo)
    player_name = input("Enter your name: ")
    balance = 100

    while True:
        print(f"\nWelcome, {player_name}! Your current balance: ${balance}\n")
        deck = create_deck()
        shuffle_deck(deck)

        bet = get_bet(balance)  # Initialize the 'bet' variable here

        player_hand = [draw_card(deck), draw_card(deck)]
        dealer_hand = [draw_card(deck), draw_card(deck)]

        player_score = calculate_score(player_hand)
        dealer_score = calculate_score(dealer_hand)

        print(f"Dealer's Hand: {dealer_hand[0][0]}{dealer_hand[0][1]}, *")
        print(f"{player_name}'s Hand: {display_hand(player_hand)}")
        print(f"{player_name}'s Score: {player_score}\n")

        # Player's turn
        while True:
            if player_score == 21:
                print("Blackjack! You win!")
                balance += 1.5 * bet
                break

            action = input("Do you want to hit or stand? (hit/stand): ").lower()
            if action == 'hit' or action == "h":
                player_hand.append(draw_card(deck))
                player_score = calculate_score(player_hand)
                print(f"{player_name}'s Hand: {display_hand(player_hand)}")
                print(f"{player_name}'s Score: {player_score}\n")
                if player_score > 21:
                    print("Busted! You lose.")
                    balance -= bet
                    break
            elif action == 'stand' or action == "s":
                break
            else:
                print("Invalid input. Please enter 'hit' or 'stand'.")

        # Dealer's turn
        if player_score <= 21:
            print("\nDealer's turn:")
            print(f"Dealer's Hand: {display_hand(dealer_hand)}")
            print(f"Dealer's Score: {dealer_score}\n")

            while dealer_score < 17:
                dealer_hand.append(draw_card(deck))
                dealer_score = calculate_score(dealer_hand)
                print(f"Dealer's Hand: {display_hand(dealer_hand)}")
                print(f"Dealer's Score: {dealer_score}\n")

            if dealer_score > 21 or dealer_score < player_score:
                print("You win!")
                balance += bet
            elif dealer_score > player_score:
                print("Dealer wins. You lose.")
                balance -= bet
            else:
                print("It's a tie!")

        # Ask if the player wants to play again
        if balance <= 0:
            print("You have run out of money. Game over.")
            print(end)
            break

        play_more = play_again()
        if play_more:
            continue
        else:
            print(end)
            break

if __name__ == "__main__":
    blackjack_game()
