import db
import random

def display_title():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")


def playing_cards():
    cards = []
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9',
             '10', 'Jack', 'Queen', 'King', 'Ace']

    #Storing cards in deck
    for suit in suits:
        for rank in ranks:
            cards.append(f"{rank} of {suit}")
    return cards

#lets user enter bet and checks if money goes below 5.
def bet_amount():
    money = db.read_money_amount()
    print(f"\nMoney: {money}")
    while True:
        try:
            bet_amount = float(input("Bet amount: "))
            if bet_amount < 5 or bet_amount > money or bet_amount > 1000:
                print("Bet has to be higher than 5 and less than 1000 or your current amount of money.")
            else:
                return bet_amount
        except ValueError:
            print("Invalid input. Please enter a number.")
    

#card that is shown first
def show_dealer_card(cards, show_dealer_cards):
    print("\nDEALER'S SHOW CARD:")
    print(show_dealer_cards)

def player_hands(cards, player_hand):
    print("\nYOUR CARDS:")
    for card in player_hand:
        print(card)

def dealer_hands(cards, dealer_hand):
    print("\nDEALER'S CARDS")
    for card in dealer_hand:
        print(card)

#gives value to the ranks of cards so that you can add up points in the end to see who wins
def points(player_hand, dealer_hand):
    def calculate_hand_value(hand):
        value = 0
        ace_count = 0
        for card in hand:
            rank = card.split(' ')[0] 
            if rank in ['Jack', 'Queen', 'King']:
                value += 10
            elif rank == 'Ace':
                ace_count += 1
                value += 11
            else:
                value += int(rank)
        
        #if value > 21, turn Aces from 11 to 1 for dealer
        while value > 21 and ace_count:
            value -= 10
            ace_count -= 1
        
        return value

    
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    return player_value, dealer_value

#checks all possible win or lose or tie scenario and outputs based off score.
def winner(player_value, dealer_value, money, bet):
    
    if dealer_value > 21:
        print(f'\nYOUR POINTS:   {player_value}')
        print(f"DEALER'S POINTS {dealer_value}")
        print("\nDealer busts! You win.")
        money += bet
                   
    if player_value > dealer_value and player_value < 21:
        print(f'\nYOUR POINTS:   {player_value}')
        print(f"DEALER'S POINTS {dealer_value}")
        print("\nYou Win!")
        money += bet
                    
    elif player_value < dealer_value and dealer_value <= 21:
        print(f'\nYOUR POINTS:   {player_value}')
        print(f"DEALER'S POINTS {dealer_value}")
        print("\nSorry, you lose.")
        money -= bet
                    
    elif player_value == dealer_value:
        print(f'\nYOUR POINTS:   {player_value}')
        print(f"DEALER'S POINTS {dealer_value}")
        print("\nIt's a tie!")
    return money       

def main():
    money = db.read_money_amount()
    again = 'y'
    while again == 'y':
        display_title()
        bet = bet_amount()
    
        cards = playing_cards()
        random.shuffle(cards)
        player_hand = [cards.pop(), cards.pop()]
        dealer_hand = [cards.pop(), cards.pop()]

        show_dealer_cards = dealer_hand[0]
        show_dealer_card(cards, show_dealer_cards)
        player_hands(cards, player_hand)
        player_value, dealer_value = points(player_hand, dealer_hand)
        player_value, _ = points(player_hand, dealer_hand)

        #asks user if they want to hit or stand
        while player_value <= 21:
            action = input("\nHit or stand? (hit/stand): ").lower()
            if action == 'hit':
                new_card = cards.pop()
                player_hand.append(new_card)
                player_hands(cards, player_hand)
                player_value, _ = points(player_hand, dealer_hand)
                if new_card.split(' ')[0] == 'Ace':
                    ace_choice = input("You drew an Ace, would you like it to be worth 1 or 11?: ")
                    if ace_choice == '1':
                        player_value += 1
                    elif ace_choice == '11':
                        player_value += 11
                player_value, _ = points(player_hand, dealer_hand)
                if player_value > 21:
                    player_value, _ = points(player_hand, dealer_hand)
                    print(f'\nYOUR POINTS:   {player_value}')
                    print(f"DEALER'S POINTS {dealer_value}")
                    print("\nSorry, you busted!")
                    money -= bet
                    break
            elif action == 'stand':
                _, dealer_value = points(player_hand, dealer_hand)
                if dealer_value >= 17 and dealer_value <= 21:
                    dealer_hands(cards, dealer_hand)
                    break
                
                elif dealer_value < 17:
                    dealer_hand.append(cards.pop())
                    _, dealer_value = points(player_hand, dealer_hand)
                    dealer_hands(cards, dealer_hand)
                    break
             
        winner(player_value, dealer_value, money, bet)
        print(f"Money: {money}")     
        
        #asks user if they want to play again
        again = input("\nPlay again? (y/n): ").lower()
        if again != 'y':
            break
    print("Come back soon!")
    print("Bye!")
            
        
        
    
    

    
    

    
    





if __name__ == "__main__":
    main()
