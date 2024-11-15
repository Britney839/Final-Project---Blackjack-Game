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

#The winning player/dealer logic
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
