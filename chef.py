import os
# for data
Chef_profile = 'chef_profile.txt'
Orders_file = 'orders.txt'
Ingredients_file = 'ingredients.txt'

# function to update chef profile
def update_profile():
    name = input("Enter your new name: ")
    email = input("Enter your new email: ")

    with open (Chef_profile, 'w') as file:
          file.write(f"Name: {name} \nEmail: {email}\n")
    print("**Profile update successfully**")


# function to view orders placed by CUSTOMERS
def view_orders():
    print("\n*** Customer Orders ***")
    if os.path.exists(Orders_file):
        with open(Orders_file, 'r') as file:
            orders = file.readlines()
            if orders:
                for order in orders:
                    print(order.strip())
            else:
                print("NO Orders Available.")
    else:
        print("Orders File Doesn't Exist.")

# function to update the statue of an ORDER
def update_order_status():
    view_orders()
    order_number = input("\nEnter the order number to update status: ")
    new_status = input("Enter the new status (In Progress/Completed): ")

    if os.path.exists(Orders_file):
        with open(Orders_file, 'r') as file:
            orders = file.readlines()

        with open(Orders_file, 'w') as file:
            for order in orders:
                if order.startswith(order_number):
                    order_data = order.strip().split(',')
                    order_data[2] = new_status
                    file.write(','.join(order_data) + '\n')
                else:
                    file.write(order)
        print(f"**Order {order_number} status update to {new_status}**")
    else:
        print("Orders File Doesn't Exist")

# function t add new ingredient request
def request_ingredient():
    ingredient_name = input("Enter the ingredient name: ")
    quantity = input("Enter the quantity: ")

    with open(Ingredients_file, 'a') as file:
        file.write(f"{ingredient_name},{quantity}\n")
    print(f"*Ingredient {ingredient_name} requested with quantity {quantity}.*")
# function t delete
def delete_ingredient_requested():
    ingredient_name = input("Enter the ingredient name to delete!!:")

    if os.path.exists(Ingredients_file):
        with open(Ingredients_file, 'r') as file:
            ingredients = file.readlines()

        with open(Ingredients_file, 'w') as file:
            found = False
            for ingredient in ingredients:
                if ingredient.startswith(ingredient_name):
                    found = True
                else:
                    file.write(ingredient)
        if found:
            print(f"Ingredient {ingredient_name} DELETE from the request list!!.")
        else:
            print(f"Ingredient File Doesn't Exist!.")
# function  display the Chef's menu
def chef_menu():
    while True:
         print("\n******** CHEF MENU ********")
         print("1. View Orders.")
         print("2. Update Order Statues.")
         print("3. Request Ingredients.")
         print("4. Delete Ingredient Request.")
         print("5. Update Profile.")
         print("6. Exit")

         choice = input("Enter your Choice: ")

         if choice == '1':
             view_orders()
         elif choice == '2':
             update_order_status()
         elif choice == '3':
             request_ingredient()
         elif choice == '4':
             delete_ingredient_requested()
         elif choice == '5':
             update_profile()
         elif choice == '6':
             break
         else:
             print("Incorrect Choice!!, Please try again.")
