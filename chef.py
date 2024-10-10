import os

# for data
Orders_file = 'Dataset/orders.txt'
Ingredients_file = 'ingredients.txt'
Credentials_file = 'Dataset/credentials.txt'  # Updated path for chef's profile
Sales_report_file = 'salesReport.txt'  # File to store sales data

# function to update chef profile
def update_profile():
    name = input("Enter your new name: ")
    email = input("Enter your new email: ")

    # Update profile in credentials.txt
    with open(Credentials_file, 'w') as file:
        file.write(f"Name: {name} \nEmail: {email}\n")
    print("**Profile updated successfully**")


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


# function to update the status of an ORDER and record sales if completed
def update_order_status():
    view_orders()
    order_number = input("\nEnter the order number to update status: ")
    new_status = input("Enter your choice\n1.In Progress\n2.Completed\n (1 or 2): ")

    if new_status == '1':
        new_status = 'In Progress'
    elif new_status == '2':
        new_status = 'Completed'
    else:
        print("Invalid choice. Please enter either 1 or 2.")
        return

    if os.path.exists(Orders_file):
        with open(Orders_file, 'r') as file:
            orders = file.readlines()

        with open(Orders_file, 'w') as file:
            found = False
            for order in orders:
                if order.startswith(order_number + ','):
                    order_data = order.strip().split(',')
                    order_data[3] = new_status  # Update the status

                    # If the order is marked as "Completed", log it to salesReport.txt
                    if new_status == 'Completed':
                        dish_price = order_data[2]  # Assuming price is at index 2
                        chef_name = get_chef_name()
                        with open(Sales_report_file, 'a') as sales_file:
                            sales_file.write(f"{chef_name} {dish_price}\n")
                        print(f"**Sales entry added: {chef_name} {dish_price}**")

                    file.write(','.join(order_data) + '\n')
                    found = True
                else:
                    file.write(order)

            if found:
                print(f"**Order {order_number} status updated to {new_status}**")
            else:
                print(f"Order {order_number} not found.")
    else:
        print(f"Order {order_number} not found.")


# function to add new ingredient request
def request_ingredient():
    ingredient_name = input("Enter the ingredient name: ")
    quantity = input("Enter the quantity: ")

    with open(Ingredients_file, 'a') as file:
        file.write(f"{ingredient_name},{quantity}\n")
    print(f"*Ingredient {ingredient_name} requested with quantity {quantity}.*")


# function to delete an ingredient request
def delete_ingredient_requested():
    ingredient_name = input("Enter the ingredient name to delete: ")

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
            print(f"Ingredient {ingredient_name} DELETED from the request list.")
        else:
            print(f"Ingredient {ingredient_name} not found in the request list.")


# function to display the Chef's menu
def chef_menu():
    while True:
        print("\n******** CHEF MENU ********")
        print("1. View Orders.")
        print("2. Update Order Status.")
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


# to start
if __name__ == "__main__":
    chef_menu()
