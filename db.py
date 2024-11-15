
def write_money_amount(money):
    with open("money.txt", "w", newline="") as file:
        file.write(str(money))
    return money





def read_money_amount():
    try:
        with open("money.txt", newline="") as file:
            money = float(file.read())
        return money
    except FileNotFoundError:
        print(f"Could not find the file named {money.txt}")


