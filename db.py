def read_money():
    try:
        with open("money.txt", "r", newline="") as file:
            money = float(file.read())
        return money
    except FileNotFoundError:
        print(f"Could not find the file named {money.txt}")
    


def write_money(money):
    with open("money.txt", "w", newline="") as file:
        file.write(str(money))
        
        
