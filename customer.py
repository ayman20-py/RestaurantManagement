from datasetManipulation import readMenu, appendCredentials, writeCredentials, readCredentials, readOrders
from styles import *
import os

###############################################
# The customer should be able to change the cart after the order has been placed and the status is still PENDING
###############################################
orders = []


def checkLogin():
    credentials = readCredentials()
    os.system("cls")

    print("\nWelcome to the restaurant!!")
    print("Please login to the system\n")

    emailInput = input("Please enter your email: ")

    if emailInput in credentials:
        currentRole = credentials[emailInput]["Role"]
        nickname = credentials[emailInput]["Nickname"]
        os.system("cls")
        print()
        prGreen("Login Successful!")
        prLightPurple(f"Role: {currentRole}")
        print(f" Hi {nickname}!")
        return {"email": emailInput, "response": True, "role": currentRole}
    else:
        print("Error, email not found")
        return {"response": False}


def applyDiscount(visits):
    """Apply discount if customer has visited more than 5 times."""
    if visits >= 5:
        print("You've qualified for a 10% discount on your total!")
        return 0.10
    return 0.0


def viewFoodMenu():
    """Displays the food menu."""
    food_items = readMenu()
    if not food_items:
        print("No food items available.")
        return {}

    print("Curry")
    for food in food_items:
        if food_items[food]["Type"] == "Curry":
           print(f"\t{food} - RM{food_items[food]["Price"]}") 

    print("Flat Breads")
    for food in food_items:
        if food_items[food]["Type"] == "Flat Breads":
           print(f"\t{food} - RM{food_items[food]["Price"]}") 

    print("Rice")
    for food in food_items:
        if food_items[food]["Type"] == "Rice":
           print(f"\t{food} - RM{food_items[food]["Price"]}") 

    print("Beverage")
    for food in food_items:
        if food_items[food]["Type"] == "Beverage":
           print(f"\t{food} - RM{food_items[food]["Price"]}") 

    return food_items


def orderFood(visits, customerEmail):
    """Handles the food ordering process."""
    food_items = viewFoodMenu()
    if not food_items:
        return

    cart = []
    cartName = []
    discount = applyDiscount(visits)

    while True:

        if cart:
            print("\nYour Cart:")
            for item in cart:
                print(f"{item['name']} - Quantity: {item['quantity']} - Total: ${item['price'] * item['quantity']:.2f}")
        else:
            print("\nYour Cart is empty.")


        print("\n1. Add Food to Cart")
        print("2. Edit Food in Cart")
        print("3. Delete Food from Cart")
        print("4. Confirm & Exit")
        print("0. Exit without saving")


        command = input("Enter command >> ")

        if command == '1':
            dish_name = input("Enter the food name to add to cart >> ")
            if dish_name in food_items:
                try:
                    quantity = int(input("Enter quantity >> "))
                    if quantity > 0:
                        price = float(food_items[dish_name]['Price'].replace(',', ''))  # Remove any commas
                        cart.append({"name": dish_name, "quantity": quantity, "price": price})
                        print("Item added to cart!")
                    else:
                        print("Quantity must be greater than 0!")
                except ValueError:
                    print("Invalid quantity! Please enter a number.")
            else:
                print("Invalid food item!")

        elif command == '2':
            dish_name = input("Enter the food name to edit in cart >> ")
            for item in cart:
                if item['name'] == dish_name:
                    try:
                        quantity = int(input("Enter new quantity >> "))
                        if quantity > 0:
                            item['quantity'] = quantity
                            print("Cart updated!")
                        else:
                            print("Quantity must be greater than 0!")
                    except ValueError:
                        print("Invalid quantity! Please enter a number.")
                    break
            else:
                print("Item not in cart!")

        elif command == '3':
            dish_name = input("Enter the food name to remove from cart >> ")
            for item in cart:
                if item['name'] == dish_name:
                    cart.remove(item)
                    print("Item removed from cart!")
                    break
            else:
                print("Item not in cart!")

        elif command == '4':
            if cart:
                for items in cart:
                    cartName.append(f"{items["name"]}:{items["quantity"]}") 

                total_amount = sum(item['price'] * item['quantity'] for item in cart)
                total_amount *= (1 - discount)
                print(f"Total amount to pay (after discount, if applicable): ${total_amount:.2f}")

                with open("Dataset/orders.txt", "a") as file:
                    # Format for the orders
                    # customerEmail, status, ...orders
                    file.write(f"{customerEmail},Pending,{",".join(cartName)}\n")

                print("Order confirmed!")
                cart.clear()
                break
            else:
                print("Your cart is empty!")


        elif command == "0":
            print("Exit without saving")
            break
        
        else:
            print("Invalid command!")


def viewOrderStatus(customerEmail):
    customerOrders = readOrders()
    count = 1
    for customers in customerOrders:
        if customers == customerEmail:
            print()
            print(f"Order {count}")
            for dish in customerOrders[customers]["Dish"]:
                print(f"\tDish Name: {dish["Dish Name"]}")
                print(f"\tQuantity: {dish["Quantity"]}")
            print()
            print(f"Status: {customerOrders[customers]["Status"]}")




def sendFeedback(customerEmail):
    """Handles feedback submission."""
    feedback = input("Please enter your feedback: ")

    with open("Dataset/feedback.txt", "a") as feedback_file:
        feedback_file.write(f"{customerEmail}: {feedback}\n")

    prGreen("Thank you for your feedback! We appreciate your input and will use it to improve our service.")

def updateProfile(customerEmail):
    """Handles profile update."""
    info = readCredentials()
    customer_data = info.get(customerEmail, {})

    if not customer_data:
        print("Customer not found!")
        return

    print(f"Current Nickname: {customer_data['Nickname']}")
    print(f"Current Contact Info: {customer_data['Contact Info']}")

    new_nickname = input("Enter new nickname (or press Enter to keep current): ")
    new_contact_info = input("Enter new contact info (or press Enter to keep current): ")


    if new_nickname:
        customer_data["Nickname"] = new_nickname
    if new_contact_info:
        customer_data["Contact Info"] = new_contact_info


    info[customerEmail] = customer_data
    writeCredentials(info)
    prGreen("Profile updated successfully!")



def customerFunctions(customerEmail):
    """Main function for handling customer actions."""
    info = readCredentials()
    visits = info[customerEmail].get("NumberOfVisit", 0)

    while True:
        print("\nCustomer Functions:")
        print("1. View & Order Food")
        print("2. View Order Status")
        print("3. Send Feedback")
        print("4. Update Profile")
        print("0. Logout")


        command = input("Enter command >> ")

        if command == '1':
            orderFood(visits, customerEmail)
            visits += 1
            info[customerEmail]["NumberOfVisit"] = visits
            writeCredentials(info)

        elif command == '2':
            viewOrderStatus(customerEmail)

        elif command == '3':
            sendFeedback(customerEmail)

        elif command == '4':
            updateProfile(customerEmail)

        elif command == '0':
            print("Logging out!")
            break

        else:
            print("Invalid command!")



if __name__ == "__main__":
    customerFunctions("customer@gmail.com") 
