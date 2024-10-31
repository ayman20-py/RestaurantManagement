import os
from datasetManipulation import *
import datetime

# for data
Orders_file = 'Dataset/orders.txt'
Ingredients_file = 'Dataset/ingredients.txt'
Credentials_file = 'Dataset/credentials.txt'  # Updated path for chef's profile
Sales_report_file = 'Dataset/salesreport.txt'  # File to store sales data

# function to update chef profile


def update_profile(chef_email):
    infoCred = readCredentials()
    name = input("Enter your new name: ")
    email = input("Enter your new email: ")

    # Update profile in credentials.txt
    newRecord = infoCred[chef_email]
    infoCred[email] = newRecord
    infoCred[email]["Nickname"] = name

    del infoCred[chef_email]
    writeCredentials(infoCred)



# function to get the chef's name from credentials.txt
def get_chef_name():
    if os.path.exists(Credentials_file):
        with open(Credentials_file, 'r') as file:
            for line in file:
                if line.startswith("Name:"):
                    return line.split(":")[1].strip()
    return "Unknown Chef"


# function to view orders placed by CUSTOMERS
def view_orders():
    orders = readOrders()
    print("\n*** Customer Orders ***")
    if orders:
        for index in orders:
            if orders[index]["Status"] == "Pending":
                print(orders[index]["Customer"])
                print(f"Status: {orders[index]["Status"]}")
                for dish in orders[index]["Dish"]:
                    print(
                        f"{dish["Dish Name"]} -> Quantity: {dish["Quantity"]}")
                print()

    else:
        print("No orders to be processed!")


# function to update the status of an ORDER and record sales if completed
def update_order_status(chef_email):

    orders = readOrders()
    menu = readMenu()

    indexingMenu = {}
    indexingPrice = {}

    indexingMenu[0] = "Cancel"


    index = 1
    exists = False

    for count in orders:
        if orders[count]["Status"] == "Pending":
            total_price = 0
            exists = True

            print()
            print(f"INDEX: {index}")
            print(f"STATUS: {orders[count]["Status"]}")
            print("DISH: ")
            for dish in orders[count]["Dish"]:
                print(f"\t{dish["Dish Name"]}")
                print(f"\tQuantity -> {dish["Quantity"]}")

                total_price += float(menu[dish["Dish Name"]]["Price"]) * float(dish["Quantity"])

            print(f"\t{total_price}")
            print()
            indexingPrice[index] = total_price

            indexingMenu[index] = index
            index += 1

    if not exists:
        print("No orders to be cooked!!!")

    while exists:
        statusEdit = int(input("Enter the index of order you want to edit: "))
        if statusEdit not in indexingMenu:
            print("Please select a valid index!!")
            proceed = False
        elif statusEdit == 0:
            print("Cancelling operation")
            proceed = False
            exists = False
        else:
            proceed = True
            selectedOrder = indexingMenu[statusEdit]
            exists = False

    if proceed:
        current_time = datetime.datetime.now()
        current_month = current_time.month


        with open("Dataset/salesreport.txt", "a") as file:
            line = f"{chef_email},{current_month},{indexingPrice[statusEdit]}\n"
            file.write(line)


        orders[selectedOrder]["Status"] = "Finished"
        writeOrders(orders)
        print("Order finished")


# function to add new ingredient request
def request_ingredient(chef_email):
    ingredient_name = input("Enter the ingredient name: ")
    quantity = input("Enter the quantity: ")

    infoCred = readCredentials()
    chefName = infoCred[chef_email]["Nickname"]


    with open(Ingredients_file, 'a') as file:
        file.write(f"{chefName},{ingredient_name},{quantity}\n")
    print(f"*Ingredient {ingredient_name} requested with quantity {quantity}.*")


# function to delete an ingredient request
def delete_ingredient_requested(chef_email):
    indexingIngredients = {}
    indexingIngredients[0] = "Cancel"

    ingredients = readIngredients()

    infoCred = readCredentials()

    count = 1
    for index in ingredients:
        if ingredients[index]["Chef"] == infoCred[chef_email]["Nickname"]:

            currentIngredient = ingredients[index]
            print(f"INDEX: {count}")
            print(f"INGREDIENT: {currentIngredient["Ingredient"]}")
            print(f"QUANTITY: {currentIngredient["Quantity"]}")
            indexingIngredients[count] = index
            count += 1
            print()

    proceed = False
    while True:
        indexIngre = int(input("Enter the index of the ingredient you want to delete: "))
        if indexIngre not in indexingIngredients:
            print("Please insert a valid index!!")
        elif indexIngre == 0:
            print("Cancelling operation!!")
            break
        else:
            proceed = True
            break

    if proceed:
        del ingredients[indexingIngredients[indexIngre]]

        writeIngredients(ingredients)
        print("Item deleted!!")

def edit_ingredient(chef_email):

    indexingIngredients = {}
    indexingIngredients[0] = "Cancel"

    ingredients = readIngredients()

    infoCred = readCredentials()

    count = 1
    for index in ingredients:
        if ingredients[index]["Chef"] == infoCred[chef_email]["Nickname"]:

            currentIngredient = ingredients[index]
            print(f"INDEX: {count}")
            print(f"INGREDIENT: {currentIngredient["Ingredient"]}")
            print(f"QUANTITY: {currentIngredient["Quantity"]}")
            indexingIngredients[count] = index
            count += 1
            print()

    proceed = False

    while True:
        indexIngre = int(input("Enter the index of the ingredient you want to edit: "))
        if indexIngre not in indexingIngredients:
            print("Please insert a valid index!!")
        elif indexIngre == 0:
            print("Cancelling operation!!")
            break
        else:
            proceed = True
            break

    if proceed:
        editedIngre = input("Enter the new ingredient: ")
        editedQuantity = input("Enter the new quantity: ")

        ingredients[indexIngre] = {"Chef": infoCred[chef_email]["Nickname"], "Ingredient": editedIngre, "Quantity": editedQuantity}

        writeIngredients(ingredients)
        print("Changes saved!!")


# function to display the Chef's menu
def chef_menu(chef_email):
    while True:
        print("\n******** CHEF MENU ********")
        print("1. View Orders.")
        print("2. Update Order Status.")
        print("3. Request Ingredients.")
        print("4. Delete Ingredient Request.")
        print("5. Edit Requested Ingredients")
        print("6. Update Profile.")
        print("7. Exit")

        choice = input("Enter your Choice: ")

        if choice == '1':
            view_orders()
        elif choice == '2':
            update_order_status(chef_email)
        elif choice == '3':
            request_ingredient(chef_email)
        elif choice == '4':
            delete_ingredient_requested(chef_email)
        elif choice == '5':
            edit_ingredient(chef_email)
        elif choice == '6':
            chef_email =  update_profile(chef_email)
        elif choice == '7':
            break
        else:
            print("Incorrect Choice!!, Please try again.")


chef_menu("chris1@gmail.com")