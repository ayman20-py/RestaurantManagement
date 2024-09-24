from datasetManipulation import * # access all data from dataManipulation directly
import os     #The OS module provides functions for creating and removing a directory (folder), fetching its contents, changing and identifying the current directory
from styles import *

# for validating an Email
import re
def verifyEmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False


def managerFunctions(managerEmail):
    # Help message which will be displayed incase the user input an invalid command.
    global dishname
    featuresMessage = """
    Manager features:
    1. View the staff information (Chef-on/off duty).
    2. View ingredients requested by the chef. 
    3. Edit information about menu.
    4. Edit information about customer.
    5. Display the command message
    0. Logout
    """

    print(featuresMessage)

    while True:
        try:
            command = int(input("Enter command >> "))   #view which chef is on duty or off duty.
            if command == 1:
                info = readCredentials()
                for email in info:
                    if info[email]["Role"] == "Chef":
                        print(info[email]["Nickname"])
                        print(info[email]["Status"])



            elif command ==2:
                print(f"Ingredients requested by chef >> ")

            elif command == 3:
                print(f"Enter to:\n1.Add \n2.Edit \n3.Delete")
                choice = int(input("Please enter your choice >> "))
                if choice == 1:                                     #Adding new food to menu file
                    dishname = input("Enter name: ")
                    category = input("Enter category: ")
                    price = input("Enter price: ")
                    ingredients = input("Enter ingredients(separate by (', '): ")

                    appendMenu(f"\n{category}, {dishname}, {price}, {ingredients}")

                    f = open("Dataset/menu.txt", "r")
                    print(f.read())


                    # TO RE-WRITE
                elif choice == 2:         # To edit a dish on the menu

                    print("1.Dish Name")    # editing Dish name on menu file
                    info = readMenu()
                    editing = input("Do you want to edit the name (Y/N): ").lower()
                    if editing == "y":
                        currentName = input("Enter current name: ")
                        newName = input("Enter new name: ")

                        if newName == currentName:
                            print("Name already exists")

                        else:

                            # Validate that current name entered is valid
                            info[newName] = info[currentName]
                            del info[currentName]
                            writeMenu(info)

                        print("2. Category of dish")  # edit dish category on menu file
                        info = readMenu()
                        editing = int(input("Enter index '2' to edit or other index to Terminate >> "))
                        if editing == 2:
                            currentCategory = input("Enter current category: ")
                            newCategory = input("Enter new category: ")

                            if newCategory == currentCategory:
                                print("Name already exists")

                            else:

                                # Validate that current name entered is valid
                                info[newCategory] = info[currentCategory]
                                del info[currentCategory]
                                writeMenu(info)

                            print("3.Dish Price")     # edit dish price on menu file
                            info = readMenu()
                            editing = int(input("Enter index '3' to edit or other index to Terminate >> "))
                            if editing == 3:
                                currentPrice = input("Enter current price >> ")
                                newPrice = input("Enter new price >> ")

                                if newPrice == currentPrice:
                                    print("Name already exists")

                                else:

                                  # Validate that current price entered is valid
                                    info[newName] = info[currentName]
                                    del info[currentPrice]
                                    print(info)
                                    writeMenu(info)

                            print("4.Ingredients")    # edit ingredients on menu file.
                            info = readMenu()
                            editing = int(input("Enter index '4' to edit or other index to Terminate >> "))
                            if editing == 4:
                                currentIngredients = input("Enter current ingredients: ")
                                newIngredients = input("Enter new ingredients: ")

                                if newIngredients == currentIngredients:
                                    print("Name already exists")

                                else:

                                    # Validate that current ingredients entered is valid
                                    info[newIngredients] = info[currentIngredients]
                                    del info[currentIngredients]
                                    print(info)
                                    writeMenu(info)

            # Delete dish on menu
            elif command == 3:
                info = readMenu()
                delete = str(input("Enter dish name to delete: "))
                if delete in info :
                    print("Are you sure")
                    delet = int(input("Enter '1' to continue or '2' to Stop >> "))     # 'delet' is variable name to continue or stop.
                    if delet == 1:
                        del info[delete]
                        writeMenu(info)
                        print(info)



            # TO RE-WRITE
            # Edit customer info
            elif command == 4:
                info = readCredentials()

                print()   #leave empty line for more aesthetic view
                print("Editing Customer information")
                print("\t1. Nickname")
                print("\t2. Email")
                print("\t3. Delete customer account")
                print("\t0. Save & Exit")
                print()

                while True:
                    editCommand = int(input("Enter the index of the command: "))

                    if editCommand == 0:
                        writeCredentials(info)
                        break
                    else:
                        if editCommand == 1:
                            new_Nickname = input("Enter customer's new nickname: ")  # editing customer Name
                            info[email]["Nickname"] = new_Nickname

                        elif editCommand == 2:
                            newEmail = input("Enter new email: ")  #edit customer email
                            if verifyEmail(newEmail):
                                info[newEmail] = info[email]
                                del info[email]
                                email = newEmail
                            else:
                                print("Invalid email address!!")


                        elif editCommand == 3:        # Delete customer account
                            Customer = str(input("Write customer name which you want to delete: "))
                            if Customer == info[email]["Nickname"]:

                                confirmation = input("Are you sure you want to delete customer account(Y/N): ").lower()  #.lower() will print the uppercase string to lowercase string
                                if confirmation == "yes or Yes":
                                    print(f"Deleting account with email: {email}")
                                    del info[email]
                                    print("Loging out of the system!")
                                    writeCredentials(info)
                                    return
                                else:
                                    print("Terminating operation!")

                            else:
                                print("Invalid index!")

            elif command == 5:
                os.system("cls") #this will lists dictionary contents
                print(featuresMessage)

            # Logout of the program
            elif command == 0:
                prRed("Loging out of the system!")
                break

            else:
                prRed("This is an invalid command!")
                print(featuresMessage)

        except Exception as e:
                print(e)
