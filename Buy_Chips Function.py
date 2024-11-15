# Ask if the player wants to buy more chips if they are running low
def buy_chips():
    money = db.read_money()
    if money < 5:
        num_chips = input("Running out of money! Want to buy more chips? (y/n): ").lower()
        if num_chips == "y":    
            try:
                amount = float(input("How much would you like to buy? "))
                money += amount
                db.write_money(money)
                print(f"You now have ${money} worth of chips.")
                print()
            except ValueError:
                print("Invalid amount entered.")
       
    return money

