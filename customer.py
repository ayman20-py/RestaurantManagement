############################################################
# When editing own profile, the current email cannot be changed to the new email in the buffer itself
############################################################

############################################################
# Didn't add the discount on every 5 visits functionality
############################################################

from datasetManipulation import readMenu, appendCredentials, writeCredentials, readCredentials
from styles import *

import re
def verifyEmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False

def viewFoodMenu():

    # Reading the menu
    food_items = readMenu()
    if not food_items:
        print("No food items available.")
        return {}
    for dish_name, details in food_items.items():
        print(f"{dish_name} - ${details['Price']}")
    return food_items

def orderFood():
    food_items = viewFoodMenu()
    if not food_items:
        return

    cart = {}

    while True:
        if cart:
            print("\nYour Cart:")
            for dish_name, quantity in cart.items():
                price = float(food_items[dish_name]['Price'])
                print(f"{dish_name} - Quantity: {quantity} - Total: ${price * quantity:.2f}")
        else:
            print("\nYour Cart is empty.")

        print("\n1. Add Food to Cart")
        print("2. Edit Food in Cart")
        print("3. Delete Food from Cart")
        print("4. Confirm Order")
        print("0. Exit")

        command = input("Enter command >> ")

        if command == '1':
            dish_name = input("Enter the food name to add to cart >> ")
            if dish_name in food_items:

                try:
                    quantity = int(input("Enter quantity >> "))
                    if quantity > 0:
                        cart[dish_name] = cart.get(dish_name, 0) + quantity
                        print("Item added to cart!")
                    else:
                        print("Quantity must be greater than 0!")
                except ValueError:
                    print("Invalid quantity! Please enter a number.")
            else:
                print("Invalid food item!")

        elif command == '2':
            dish_name = input("Enter the food name to edit in cart >> ")
            if dish_name in cart:
                try:
                    quantity = int(input("Enter new quantity >> "))
                    if quantity > 0:
                        cart[dish_name] = quantity
                        print("Cart updated!")
                    else:
                        print("Quantity must be greater than 0!")
                except ValueError:
                    print("Invalid quantity! Please enter a number.")
            else:
                print("Item not in cart!")

        elif command == '3':
            dish_name = input("Enter the food name to remove from cart >> ")
            if dish_name in cart:
                del cart[dish_name]
                print("Item removed from cart!")
            else:
                print("Item not in cart!")

        elif command == '4':
            if cart:
                total_amount = sum(float(food_items[dish_name]['Price']) * quantity for dish_name, quantity in cart.items())
                print(f"Total amount to pay: ${total_amount:.2f}")
                print("Order confirmed!")
                cart.clear()
            else:
                print("Your cart is empty!")

        elif command == '0':
            break

        else:
            print("Invalid command!")

def viewOrderStatus():
    orders = {1: "Completed", 2: "Pending"}
    for order_id, status in orders.items():
        print(f"Order ID: {order_id} - Status: {status}")

def sendFeedback(customerEmail):
    feedback = input("Enter your feedback: ").strip()
    if feedback:
        appendCredentials(f"\nFeedback from {customerEmail}: {feedback}")
        print("Thank you for your feedback!")
    else:
        print("Feedback cannot be empty!")

def updateProfile(email):
    customerEmail = email
    print(customerEmail)
    info = readCredentials()
    if customerEmail not in info:
        print("Customer not found!")
        return

    while True:
        print("\nUpdate Profile:")
        print("1. Update Nickname")
        print("2. Update Email")
        print("3. Update Password")
        print("0. Save & Exit")

        command = input("Enter command >> ")

        if command == '1':
            new_nickname = input("Enter new nickname: ").strip()
            if new_nickname:
                info[customerEmail]["Nickname"] = new_nickname
                print("Nickname updated!")
            else:
                print("Nickname cannot be empty!")

        elif command == '2':
            new_email = input("Enter new email: ").strip()
            if verifyEmail(new_email):
                info[new_email] = info[customerEmail]
                # del info[customerEmail]
                info[new_email] = info.pop(customerEmail)
                customerEmail = new_email
                print(f"Current: {customerEmail}")
                print("Email updated!")
            else:
                print("Invalid email address!")

        elif command == '3':
            new_password = input("Enter new password: ").strip()
            if new_password:
                info[customerEmail]["Password"] = new_password
                print("Password updated!")
            else:
                print("Password cannot be empty!")

        elif command == '0':
            writeCredentials(info)
            break

        else:
            print("Invalid command!")

def customerFunctions(customerEmail):
    while True:
        print("\nCustomer Functions:")
        print("1. View & Order Food")
        print("2. View Order Status")
        print("3. Send Feedback")
        print("4. Update Profile")
        print("0. Logout")

        command = input("Enter command >> ")

        if command == '1':
            orderFood()

        elif command == '2':
            viewOrderStatus()

        elif command == '3':
            sendFeedback(customerEmail)

        elif command == '4':
            # To check when editing the email
            updateProfile(customerEmail)

        elif command == '0':
            print("Logging out!")
            break

        else:
            print("Invalid command!")

