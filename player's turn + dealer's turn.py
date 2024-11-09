# Handle player’s turn
def player_turn(player_hand, dealer_hand, cards):
    player_score = point_value(player_hand)
    dealer_score = point_value(dealer_hand)
    while player_score < 21:
        move = input("\nHit or Stand? (hit/stand): ").lower()
        if move == "hit":
            new_card = cards.pop()
            player_hand.append(new_card)
            player_hands(player_hand)
            player_score = point_value(player_hand)
            if player_score >= 21:
                print(f"\nYOUR POINTS: {player_score}\nDEALER'S POINTS: {dealer_score}")
                print()
            return player_score
        elif move == "stand":
            break
        else:
            print("Invalid input, please type 'hit' or 'stand'.")
    return player_score

# Handle dealer’s turn
def dealer_turn(dealer_hand, cards):
    dealer_score = point_value(dealer_hand)
    dealer_hands(dealer_hand, show_all=True)  # Show both dealer cards
    while dealer_score < 17:
        new_card = cards.pop()
        dealer_hand.append(new_card)
        dealer_score = point_value(dealer_hand)
        dealer_hands(dealer_hand, show_all=True)
    return dealer_score

