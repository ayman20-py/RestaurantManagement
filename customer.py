from datasetManipulation import *
from styles import *
import os

###############################################
# The customer should be able to change the cart after the order has been placed and the status is still PENDING
###############################################
orders = []



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
    for index in customerOrders:
        if customerOrders[index]["Customer"] == customerEmail:
            print()
            print(f"Order {count}")
            for dish in customerOrders[index]["Dish"]:
                print(f"\tDish Name: {dish["Dish Name"]}")
                print(f"\tQuantity: {dish["Quantity"]}")
            print()
            print(f"Status: {customerOrders[index]["Status"]}")
            count += 1




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


def editOrder(customerEmail):
    orders = readOrders()
    infoCred = readCredentials()

    indexingOrders = {}

    count = 1
    for index in orders:
        if customerEmail == orders[index]["Customer"] and orders[index]["Status"] == "Pending":
            print()
            print(f"INDEX: {count}")
            print(f"STATUS: {orders[index]["Status"]}")
            print("DISH: ")
            for dish in orders[index]["Dish"]:
                print(f"\t{dish["Dish Name"]}")
                print(f"\tQuantity -> {dish["Quantity"]}")

            indexingOrders[count] = index
            count += 1


    proceed = False
    while True:
        orderIndex = int(input("Enter the index of the order you want to edit: "))
        if orderIndex in indexingOrders:
            proceed = True
            break
        else:
            print("Please enter a valid index!!")

    cart = []
    if proceed:
        food_items = viewFoodMenu()
        while True:
            dish_name = input("Enter the food name to add to cart (Leave blank to end change) >> ")
            if dish_name == "":
                del orders[orderIndex]
                writeOrders(orders)
                orders[orderIndex] = {"Customer": customerEmail, "Status": "Pending", "Dish": ",".join(str(cart))}

                with open("Dataset/orders.txt", "a") as file:
                    file.write(f"{customerEmail},Pending,{','.join(cart)}")
                
                break
            else:
                if dish_name in food_items:
                    try:
                        quantity = int(input("Enter quantity >> "))
                        if quantity > 0:
                            price = float(food_items[dish_name]['Price'].replace(',', ''))  # Remove any commas
                            # cart.append({"Dish Name": dish_name, "Quantity": quantity})
                            cart.append(f"{dish_name}:{quantity}")
                            print("Item added to cart!")
                        else:
                            print("Quantity must be greater than 0!")
                    except ValueError:
                        print("Invalid quantity! Please enter a number.")
                else:
                    print("Invalid food item!")

                #file.write(f"{customerEmail},Pending,{",".join(cartName)}\n")


def deleteOrder(customerEmail):
    orders = readOrders()
    infoCred = readCredentials()

    indexingOrders = {}

    count = 1
    for index in orders:
        if customerEmail == orders[index]["Customer"] and orders[index]["Status"] == "Pending":
            print()
            print(f"INDEX: {count}")
            print(f"STATUS: {orders[index]["Status"]}")
            print("DISH: ")
            for dish in orders[index]["Dish"]:
                print(f"\t{dish["Dish Name"]}")
                print(f"\tQuantity -> {dish["Quantity"]}")

            indexingOrders[count] = index
            count += 1


    proceed = False
    while True:
        orderIndex = int(input("Enter the index of the order you want to delete: "))
        if orderIndex in indexingOrders:
            proceed = True
            break
        else:
            print("Please enter a valid index!!")

    if proceed:
        del orders[indexingOrders[orderIndex]]
        writeOrders(orders)
        print("Order deleted!!")

def customerFunctions(customerEmail):
    """Main function for handling customer actions."""
    info = readCredentials()
    visits = info[customerEmail].get("NumberOfVisit", 0)

    while True:
        print("\nCustomer Functions:")
        print("1. View & Order Food")
        print("2. View Order Status")
        print("3. Edit Order")
        print("4. Delete Order")
        print("5. Send Feedback")
        print("6. Update Profile")
        print("0. Logout")


        command = input("Enter command >> ")

        if command == '1':
            orderFood(visits, customerEmail)
            visits += 1
            info[customerEmail]["NumberOfVisit"] = visits
            writeCredentials(info)

        elif command == '2':
            viewOrderStatus(customerEmail)

        elif command == "3":
            editOrder(customerEmail)

        elif command == "4":
            deleteOrder(customerEmail)

        elif command == '5':
            sendFeedback(customerEmail)

        elif command == '6':
            updateProfile(customerEmail)

        elif command == '0':
            print("Logging out!")
            break

        else:
            print("Invalid command!")



if __name__ == "__main__":
    customerFunctions("customer@gmail.com") 
