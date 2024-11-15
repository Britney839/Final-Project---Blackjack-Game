import db
import random

def display_menu():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")
    print()

#a deck of cards
def playing_cards():
    cards = []
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    for suit in suits:
        for rank in ranks:
            cards.append(f"{rank} of {suit}")
    return cards

#bet amount
def bet_amount():
    money = db.read_money()
    print(f"Money: {money}")
    while True:
        try:     
            bet = int(input("Bet amount: "))
            if bet < 5 or bet > money:
                print("Bet must be between 5 and your available money.")
            else:
                return bet
        except ValueError:
            print("Invalid input. Please enter a number.")
    if money < 5:
        num_chips = input("Running out of money! Want more chips? (y/n): ").lower()
        try:
            amount = float(input("How much would you like to buy?"))
            money += amount
            db.write_money(money)
            print(f"You have ${amount}'s worth of chips. You have {num_chips}")
        except ValueError:
            print("That's an invalid value for chips.")
                           
            

# Show player’s cards
def player_hands(player_hand):
    print("\nYOUR CARDS:")
    for card in player_hand:
        print(card)

# Show dealer's cards
def dealer_hands(dealer_hand, show_all=False):
    if not show_all:
        print("\nDEALER'S SHOW CARD:")
        print(dealer_hand[0])
    if show_all:
        print("\nDEALER'S CARDS:")
        for card in dealer_hand:
            print(card)


# Dealing cards in the deck
def deal_cards(cards, hand):
    if cards:
        card_pick = cards.pop()
        hand.append(card_pick)

# Assigning point values to the cards picked
def point_value(cards):
    value = 0
    aces = 0
    for card in cards:     
        rank = card.split(' ')[0]
        if rank in ['Jack', 'Queen', 'King']:
            value += 10
     #   elif rank == "Ace":
        #    aces += 1
        #    choice = int(input("Assign a point value of 1 or 11?: "))
         #   if choice == 11 and value + 11 <= 21:
         #       value += 11
         #       break
        #    else:
          #      value += 1
          #      break
        

    return value

def main():
    money = db.read_money()
    while True:
        display_menu()
        bet = bet_amount()
        cards = playing_cards()
        random.shuffle(cards)

        player_hand = [cards.pop(), cards.pop()]
        dealer_hand = [cards.pop(), cards.pop()]

        dealer_hands(dealer_hand)
        player_hands(player_hand)
        player_score = point_value(player_hand)
        dealer_score = point_value(dealer_hand)

        # Player's turn (evaluates the player's score)
        player_score = point_value(player_hand)
        while player_score <= 21:    
            move = input("\nHit or Stand? (hit/stand): ").lower()
            if move == "hit":
                deal_cards(cards, player_hand)
                player_hands(player_hand)
                player_score = point_value(player_hand) 
                if player_score > 21:
                    player_score = point_value(player_hand)
                    print(f"\nYOUR POINTS: {player_score}\nDEALER'S POINTS: {dealer_score}")
                    print()
                    print("You busted!")
                    money -= bet
                    db.write_money(money)
                    break     
            elif move == "stand":
                dealer_score = point_value(dealer_hand)
                if dealer_score >= 17 and dealer_score <= 21:
                    dealer_hands(dealer_hand, show_all=True)
                    break
                elif dealer_score < 17:
                    dealer_hand.append(cards.pop())
                    dealer_score = point_value(dealer_hand)
                    dealer_hands(dealer_hand, show_all=True)
                    break
            else:
                print("Invalid input. Please try typing 'hit' or 'stand'.")


        if dealer_score > 21:
            print(f"\nYOUR POINTS: {player_score}\nDEALER'S POINTS: {dealer_score}")
            print()
            print("YAY! you win. Dealer busts.")
            money += bet
            db.write_money(money)
        elif player_score > dealer_score and player_score < 21:
            print(f"\nYOUR POINTS: {player_score}\nDEALER'S POINTS: {dealer_score}")
            print()
            print("You win!")
            money += bet
            db.write_money(money)
        elif player_score < dealer_score and dealer_score < 21:
            print(f"\nYOUR POINTS: {player_score}\nDEALER'S POINTS: {dealer_score}")
            print()
            print("Sorry, you lose.")
            money -= bet
            db.write_money(money)
        elif player_score == dealer_score:
            print(f"\nYOUR POINTS: {player_score}\nDEALER'S POINTS: {dealer_score}")
            print()
            print("It's a tie!")
            
        print(f"Money: {money}")
        play_again = input("\nPlay again? (y/n): ").lower()
        print()
        if play_again != 'y':
            print("Come back soon!")
            print("Bye!")
            break

if __name__ == "__main__":
    main()

