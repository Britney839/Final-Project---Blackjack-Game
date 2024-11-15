import db
import random


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


#Asks user to hit or stand
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
                
