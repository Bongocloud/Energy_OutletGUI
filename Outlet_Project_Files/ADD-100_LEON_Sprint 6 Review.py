"""
ASSIGNMENT 13B: SPRINT 6 Review Board
Project: Energy Outlet
Developer: Nicole Leon
"""

import datetime
from order import Order


USER_HISTORY = "order_history.txt"


def customer_name():
    # Asks for name.
    customer = input(f"Please enter your name here: ").strip()
    return customer


def choose_brand():
    #Ask customer to choose a brand and grab corresponding file.
    valid_brands = ["Monster", "Redbull", "Celsius", "Reign", "C4"]
                    
    while True:
        brand = input("Choose a brand (Monster, Redbull, Celsius, Reign, C4): ").strip().capitalize()

        if brand in valid_brands:
            return brand

        print("Invalid brand. Try again.")


def drink_choice(brand):
    # Ask for drink (shows selection based on brand choice)
    try:

        with open(
            f"{brand.lower()}.txt","r") as drink_file:

            print(f"\nAvailable {brand} Drinks:")

            for line in drink_file:

                drink_name, drink_price = (line.strip().split(","))

                print(f"- {drink_name} "f"(${drink_price})")

        drink = input("\nEnter your drink choice: ").strip()

        return drink

    except FileNotFoundError:
        print("Drink file not found.")
        return ""


def calculate_price(brand_choice, drink_choice):
    # Grabs corresponding drink price from price_file for total calculations.
    try:
        with open(f"{brand_choice.lower().strip()}.txt", "r") as drink_file:
            for line in drink_file:
                drink_request, drink_price = line.strip().split(",")
                if drink_request.upper().strip() == drink_choice.upper().strip():
                    return float(drink_price), "Price Grabbed!"
    except FileNotFoundError:
        return 0.0, "Drink not found."
    return 0.0, "Drink not found."


# Saves customer order history
def customer_history(user_name, final_price):
    #Saves customer order history
    timestamp = datetime.datetime.now()

    try:
        with open(USER_HISTORY, "a") as history_file:
            history_file.write(f"{user_name}, {timestamp}, ${final_price:.2f}\n")
    except Exception as e:
        print(f"System Error: {e}")


def edit_history_file():
    # Reads and edits customer history
    
    records = []

    try: 
        
        with open(USER_HISTORY, "r") as read_file:
            for line in read_file:
                user_name, timestamp, final_price  = line.strip().split(",")
                records.append([user_name, timestamp, final_price])
        for index, item in enumerate(records):
                print(f"ID: {index},Name: {item[0]}, Date: {item[1]}, Price: {item[2]}\n")
                      
    except FileNotFoundError:
        print(f"ERROR: File was not found!\n")  
        return       

    try:
        edit_request = int(input(f"Which ID number would you like to edit?: \n"))
        if edit_request < 0 or edit_request >= len(records):
            print(f"ID not found. Try again.")
            return
        
        new_name = input(f"What is the new name for {edit_request}?: \n")
        records[edit_request][0] = new_name
        print(f"Update successful!\n")

    except ValueError:
        print(f"Invalid input: Please enter a numeric ID.")
        return

    try:        
        with open(USER_HISTORY, "w") as write_file:
            for record in records:
                write_file.write(f"{record[0]},{record[1]},{record[2]}\n")
    except TypeError as e:
        print(f"TypeError occurred: {e}\n")
        

def receipt(user_name, final_price, timestamp):
    #Create customer receipt
    
    try:
        with open("receipt.txt", "w") as receipt_file:
                receipt_file.write(f"---------Energy Outlet---------\n")
                receipt_file.write(f"-------------------------------\n")
                receipt_file.write(f"Name: {user_name}\n")
                receipt_file.write(f"Date: {timestamp}\n")
                receipt_file.write(f"-------------------------------\n")
                receipt_file.write(f"   TOTAL: ${float(final_price):.2f}\n")
                receipt_file.write("------Enjoy your beverage!------\n")
    except Exception as e:
        print(f"Error printing receipt: {e}")

    
def main():
    

    continue_program = input("Enter Y to add to your order: ").strip().upper()
    while continue_program == "Y":

        # 1. Customer Info
        name = customer_name()
        print (f"\nName: {name}")

        # 2. Order Info
        brand = choose_brand()
        drink = drink_choice(brand)
        print(f"\nDrink: {drink}")

        # 3. Price Calculations, 4. Customer History
        final_price, status = calculate_price(brand_choice = brand, drink_choice = drink)

        if status != "Price Grabbed!":
            print(status)
        else:
            print(f"Total: ${final_price:.2f}")

        # Create Object
        customer_order = Order(
            name,
            brand,
            drink,
            final_price
        )
        
        # Display Summary
        print("\nOrder Summary:")
        print(customer_order.summary())

        # Save History
        customer_history(customer_order.get_customer_name(), customer_order.get_price())

        # Print Receipt
        timestamp = datetime.datetime.now()

        receipt(customer_order.get_customer_name(), customer_order.get_price(), timestamp)

        # Continue Program 
        continue_program = input(f"Enter 'Y' to add another drink, or 'N' to stop: ").strip().upper()

main()