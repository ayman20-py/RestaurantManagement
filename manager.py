from datasetManipulation import *  # access all data from dataManipulation directly
import os     #The OS module provides functions for creating and removing a directory (folder), fetching its contents, changing and identifying the current directory
from styles import *

# for validating an Email
import re
def verifyEmail(email):                                            # Login Function
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):                                    # Validating if login data is valid
        return True
    return False


def newCustomer(managerEmail):
    print()      # for leaving enpty line in between codes
    customerName = input("Enter the new customer name: ")
    while True:
        customerEmail = input("Enter the customer email: ")
        if verifyEmail(customerEmail):
            break
        else:
            print("Please enter a valid email!!")

    customerPass = input("Enter the new customer password: ")
    customerContact = input("Enter the new customer contact number: ")

    appendCredentials(f"\nCustomer {customerName} {customerEmail} {customerPass} 0 {customerContact}")


def editCustomer(managerEmail):
    info = readCredentials()
    print()
    print("Edit Customer info")
    while True:
        customizeCustomer = {}  # create a dictionary
        customizeCustomer[0] = "Cancel"  # Implementing a cancel function if a mistake was made
        Num = 1
        for email in info:
            if info[email]["Role"] in ["Customer"]:
                print(f"{Num}")

                print(" Nickname: ", end="")  # Used End for aesthethics purposes
                print(f"{info[email]["Nickname"]}")  # End will print the code starting with the other print statement in the same line


                print(" Email: ", end="")
                print(email)

                print(" Number of visits: ", end="")
                print(info[email]["NumberOfVisit"])

                print(" Contact info: ", end="")
                print(info[email]["Contact Info"])
                print()
                customizeCustomer[Num] = email

                Num += 1

        editCustomer = int(input("Enter index of the customer's information you want to edit or '0' to cancel >> "))
        if editCustomer not in customizeCustomer:  # Validating/checking if index entered is valid
            print("Invalid!!", "\nPlease select a valid index.")  # If not, it will print this
        elif editCustomer == 0:
            print("Terminating task!")
            break

        else:
            print()
            print(f"Editing {info[customizeCustomer[editCustomer]]["Nickname"]}'s information")
            selectedEmail = customizeCustomer[editCustomer]
            print(selectedEmail)
            print()
            print("\t1. Nickname")
            print("\t2. Number of visits")
            print("\t3. Contact info")
            print("\t4. Delete customer")
            print()

            editindex = int(input("Please enter index >> "))

            # Terminating the edit process

            # Editing current nickname of the customer
            if editindex == 1:
                newName = input("Please enter new name of customer: ")
                while newName in ["", " "]:  # if new name entered is blank then this block statement will be displayed
                    print()
                    print("Please enter a valid name!!")
                    newName = input("Please enter New name: ")

                info[selectedEmail]["Nickname"] = newName


            elif editindex == 2:
                NewnumVisit = int(input("Enter new number of visits: "))
                if NewnumVisit in info:
                    print()
                    print("Record already exists")
                else:
                    info[selectedEmail]["NumberOfVisit"] = NewnumVisit

            elif editindex == 3:  # Editing customer contact info
                Newcontact = int(input("Enter new contact info: "))
                if Newcontact in info:  # if contact info entered already exists in the file, it will output 'Contact info already exists'
                    print()
                    print("Contact info already exists")
                else:
                    info[selectedEmail]["Contact Info"] = Newcontact

            elif editindex == 4:  # Deleting customer
                print(f"Are you sure you want to delete {info[email]["Nickname"]} profile")
                conDelete = input(
                    "Please enter 'yes' to delete and 'no' to cancel: ")  # conDelete = variable name for confirm Delete
                if conDelete == "yes":
                    del info[selectedEmail]
                    writeCredentials(info)
                    if selectedEmail in info:
                        prRed("Delete unsuccessful!!")  # Validating if delete is successful
                        break
                    else:
                        print("Delete successful!!")


                else:
                    print("Cancelling operation")
                    break
            writeCredentials(info)


def menu(managerEmail):
    while True:
        print()
        print(f"Enter to \n\t1. Add \n\t2. Edit")
        print("\t0. Exit Operation")
        print()

        choice = int(input("Please enter your choice >> "))

        if choice == 0:  # will exit the program
            prRed("Exiting operation!")
            break
        else:
            if choice == 1:  # Adding new food to menu file
                dishname = input("Enter dish name: ")
                category = input("Enter dish category: ")
                price = input("Enter dish price: ")
                ingredients = input("Enter ingredients(separate by (', '): ")

                appendMenu(f"\n{category}, {dishname}, {price}, {ingredients}")

                print()
                f = open("Dataset/menu.txt", "r")
                print(f.read())


            elif choice == 2:  # To edit a dish on the menu

                info = readMenu()
                f = open("Dataset/menu.txt", "r")
                print(f.read())
                print()

                editing = input("Please enter dish name to continue or '0' to save and exit: ")
                if editing == "0":
                    break
                else:

                    while True:
                        if editing in info:
                            print()
                            print("Editing Dish")
                            print("\t1. Dish name")
                            print("\t2. Category")
                            print("\t3. Price")
                            print("\t4. Ingredients")
                            print("\t5. Delete")
                            print("\t0. Save & Exit")
                            print()

                            editdish = int(input("Please choose your index to edit >> "))

                            if editdish == 0:  # Will save and exit the program
                                writeMenu(info)
                                break
                            else:

                                if editdish == 1:  # Editing dish name
                                    print("Editing dish name.")
                                    newName = input("Enter new dish name: ")
                                    # Validate that current name entered is already exists
                                    if newName in info:
                                        print()
                                        print("Name already exists")
                                    else:
                                        # Modifying the dish name by first creating a new record with the new dish name but the same body and then
                                        # deleting the old record
                                        # only for dishname because dishname is the key here.You can't just overwrite it.
                                        info[newName] = info[editing]
                                        del info[editing]
                                        editing = newName
                                        print("Press 0 to save all the changes!!")
                                        print()

                                elif editdish == 2:
                                    print()
                                    print("Editing Category of dish")
                                    newCategory = input("Please enter new category of the dish: ")
                                    # Validate that current category entered is valid
                                    if newCategory in info:
                                        print()
                                        print("Dish is already in this category.\t")
                                    else:
                                        info[editing]["Type"] = newCategory  # Will overwrite dishtype to newCategory
                                        print()

                                elif editdish == 3:
                                    print("Editing Price of dish")
                                    newPrice = input("Please enter new price of the dish: ")
                                    # Validate that current price entered is valid
                                    if newPrice in info:
                                        print()
                                        print("Dish price is the same.\t")
                                    else:
                                        info[editing]["Price"] = newPrice
                                        print()

                                elif editdish == 4:
                                    print("Editing ingredients of dish")
                                    newIngredients = str(
                                        input("Please enter new ingredients of the dish separated by ',': "))
                                    # Validate that current category entered is valid
                                    if newIngredients in info:
                                        print()
                                        print("Ingredients already exist.\t")
                                    else:
                                        info[editing]["Ingredients"] = newIngredients.split(", ")  # .split(", ") will split the ingredients by ', '
                                        print()  # eg: ingre1, ingre2, ingre3, ingre4

                                # Delete dish on menu
                                elif editdish == 5:
                                    delet = input(
                                        "Enter 'yes' to delete or 'no' to cancel: ")  # 'delet' is variable name to continue or stop.
                                    if delet == "yes":
                                        del info[editing]
                                        writeMenu(info)
                                        break

                                    else:
                                        print("Canceling operation")
                                        break
                                else:
                                    prRed("Invalid index")

def managerProfile(managerEmail):
    info = readCredentials()

    print()
    print("Editing own profile")
    print("\t1. Nickname")
    print("\t2. Email")
    print("\t3. Password")
    print("\t4. Status")
    print("\t5. Contact info")
    print("\t6. Delete own account")
    print("\t0. Save & Exit")
    print()

    while True:
        editindex = int(input("Enter the index of the command you want to execute >> "))

        if editindex == 0:
            writeCredentials(info)
            break
        else:
            if editindex == 1:  # Editing manager's own nickname
                newName = input("Enter your new name: ")
                info[managerEmail]["Nickname"] = newName

            elif editindex == 2:  # Editing own email address
                newEmail = input("Enter your new email: ")
                if verifyEmail(newEmail):  # Verifying if new email already exists
                    info[newEmail] = info[managerEmail]
                    del info[managerEmail]
                    managerEmail = newEmail
                else:
                    prRed("Invalid email address!!")

            elif editindex == 3:  # Editing own password
                newPass = input("Enter your new password: ")
                info[managerEmail]["Password"] = newPass

            elif editindex == 4:  # Updating own status about duty
                print("Please enter 'on' or 'off'")
                newStatus = input("Enter your status (on/off duty): ")
                if newStatus == "on" or "off":
                    info[managerEmail]["Status"] = newStatus
                else:
                    prRed("Invalid")

            elif editindex == 5:  # Editing own contact info
                newcontact = input("Enter your new contact info: ")
                info[managerEmail]["Contact Info"] = newcontact

            elif editindex == 6:  # Delecting own profile
                prRed("Are you sure you want to delete your profile")
                conDelete = input("Please enter 'yes' to delete or 'no' to cancel: ")
                if conDelete == "yes":
                    print(f"Deleting account with email: {managerEmail}")
                    del info[managerEmail]
                    print("Loging out of the system!")
                    writeCredentials(info)
                    return
                else:
                    prRed("Cancelling operation!")  # will not delete and restart the program

            else:
                prRed("Invalid index!!")
        print()

def viewChef(managerEmail):
    info = readCredentials()
    num = 1
    for email in info:
        if info[email]["Role"] == "Chef":
            print(f"{num}")

            print(" Nickname: ", end="")  # Used End for aesthethics purposes
            print(
                f"{info[email]["Nickname"]}")  # the end="" is used to place a space after the displayed string instead of a newline.

            print(" Email: ", end="")
            print(email)

            print(" Salary: ", end="")
            print(info[email]["Salary"])

            print(" Chef status: ", end="")
            print(info[email]["Status"])

            print(" Contact info: ", end="")
            print(info[email]["Contact Info"])

            prGreen(f"Chef {info[email]["Nickname"]} is {"on duty" if info[email]["Status"] == "on" else "off duty"}")  # Validate if chef is on/off duty and will print the result.
            print()
            num += 1



def managerFunctions(managerEmail):
    global dishname  # Variables that are created outside of a function are known as global variables.
    # Help message which will be displayed incase the user input an invalid command.

    #while True:
    featuresMessage = """
    Manager features:
    1. Add new customer.
    2. Edit information about customer.
    3. View ingredients requested by the chef.
    4. Edit information about menu.
    5. Edit own profile.
    6. View information about chefs
    7. Display manager features 
    0. Logout
    """

    print(featuresMessage)

    while True:
        index = int(input("Please enter index for manager feature>> "))

        if index == 1:
            newCustomer(managerEmail)

        elif index == 2:
            editCustomer(managerEmail)

        elif index == 3:      # Displaying ingredients requested by chef
            print(f"Ingredients requested by chef >> ")
            f = open("Dataset/ingredients.txt", "r")  # Opens dataset/ingredients.txt file
            print(f.read())
            print()

        elif index == 4:
            menu(managerEmail)

        elif index == 5:
            managerProfile(managerEmail)

        elif index == 6:
            viewChef(managerEmail)

        elif index == 7:
            os.system("cls")  # this will list the feature message again
            print(featuresMessage)

        elif index == 0:
            prRed("Loged out of the system!")
            break

        else:
            prRed("This is an invalid command!")
            print(featuresMessage)




managerFunctions("manager2@gmail.com")