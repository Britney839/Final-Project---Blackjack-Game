import db
import random

def display_menu():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")

#A deck of cards
def playing_cards():
    cards = []
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
#Storing cards in the deck
    for suit in suits:
        for rank in ranks:
            cards.append(f"{rank} of {suit}")
    random.shuffle(cards)
    return cards

#Store the bet amount
def bet_amount():
    money = db.read_money_amount()
    print(f"\nMoney: {money}")
    while True:
        try:
            bet_amount = float(input("Bet amount: "))
            if bet_amount < 5 or bet_amount > money or bet_amount > 1000:
                print("Bet has to be either higher than 5, less than 1000, or within what you have in money/chips.")
            else:
                return float(bet_amount)
        except ValueError:
            print("Invalid input. Please enter a number.")

# Ask if the player wants to buy more chips if they are running low
def buy_chips():
    money = db.read_money_amount()
    if money < 5:
        num_chips = input("Running out of money! Want to buy more chips? (y/n): ").lower()
        if num_chips == "y":    
            try:
                amount = float(input("How much would you like to buy? "))
                money += amount
                db.write_money_amount(money)
                print(f"You now have ${money} worth of chips.")
                print()
            except ValueError:
                print("Invalid amount entered.")
       
    return money

#card that is shown first
def show_dealer_card(show_dealer_cards):
    print("\nDEALER'S SHOW CARD:")
    print(show_dealer_cards)

def player_hands(player_hand):
    print("\nYOUR CARDS:")
    for card in player_hand:
        print(card)

def dealer_hands(dealer_hand):
    print("\nDEALER'S CARDS:")
    for card in dealer_hand:
        print(card)

# Calculate the point value of a hand
def point_value(hand):
    value = 0
    for card in hand:
        card_value = card.split(' ')[0]
        if card_value in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            value += int(card_value)
        elif card_value in ['Jack', 'Queen', 'King']:
            value += 10
        elif card_value == 'Ace':
            value += 11
            if value > 21:
                value -= 11
                value += 1
    return value

def hit_stand(player_hand, dealer_hand, cards):
    player_value = point_value(player_hand)
    dealer_value = point_value(dealer_hand)
    while True:
        action = input("\nHit or Stand?: ").lower()
        if action == 'hit':
            new_card = cards.pop()
            player_hand.append(new_card)
            player_hands(player_hand)
            player_value = point_value(player_hand)
            if new_card.split(' ')[0] == 'Ace':
                choice = input("\nDrew an Ace from the deck. Assign it a value of 1 or 11?: ")
                if choice == '1':
                    player_value += 1
                else:
                    player_value += 11
            if player_value > 21:
                break
        elif action == 'stand':
            while dealer_value < 17:
                new_card = cards.pop()
                dealer_hand.append(new_card)
                dealer_value = point_value(dealer_hand)
            break

    return player_value, dealer_value


def main():
    money = db.read_money_amount()
    money = buy_chips()  #this will ensure the player has enough money to play!
    while True:
        display_menu()
        bet = bet_amount() #Get the bet amount from the player
        cards = playing_cards()

        player_hand = [cards.pop(), cards.pop()]
        dealer_hand = [cards.pop(), cards.pop()]

        show_dealer_cards = dealer_hand[0]
        show_dealer_card(show_dealer_cards)
        player_hands(player_hand)

        player_value, dealer_value = hit_stand(player_hand, dealer_hand, cards)
        if player_value > 21:
            dealer_hands(dealer_hand)
            print("\nYou bust! You went over 21 pts.")
            money -= bet
        elif dealer_value > 21:
            print()
            dealer_hands(dealer_hand)
            player_hands(player_hand)
            print("\nDealer busts! You win!")
            money += round(bet * 1.5, 2)                         #3:2 payout for Blackjack
        elif player_value > dealer_value and player_value <= 21:
            dealer_hands(dealer_hand)
            player_hands(player_hand)
            print("\nYou win!")
            money += round(bet * 1.5, 2)
        elif player_value < dealer_value:
            print()
            dealer_hands(dealer_hand)
            player_hands(player_hand)
            print("\nSorry. You lose.")
            money -= bet
        else:
            print()
            dealer_hands(dealer_hand)
            player_hands(player_hand)
            print("\nIt's a tie! Nothing changes with bets.")

        print(f"\nYOUR POINTS: {player_value}\nDEALER'S POINTS: {dealer_value}")
        print()
        db.write_money_amount(float(money))
        print(f"Money: {money}")
        money = buy_chips()

        #Ask if the player wants to play again
        play_again = input("\nPlay again? (y/n): ").lower()
        print()
        if play_again != 'y':
            print("Come back soon!")
            print("Bye!")
            break

if __name__== "__main__":
    main()
                
