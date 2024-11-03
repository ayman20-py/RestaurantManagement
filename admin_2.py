from datasetManipulation import *
import os 
from styles import *


# for validating an Email
import re
def verifyEmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False


def viewStaff():

    info = readCredentials() # Read the credentials from the credentials.txt

    for email in info:

        # Managers and chefs both have the same type of metadata
        # However customers don't which means managers/chefs have to be processed differently from customers

        # Checking if the roles are chef and manager 
        if info[email]["Role"] in ["Chef", "Manager"]:

            print()

            print("Nickname:", end=" ")
            prGreen(f"{info[email]["Nickname"]}")

            print("Role:", end=" ")
            prPurple(info[email]["Role"])

            print("Email:", end=" ")
            prYellow(email)

            print("Salary:", end=" ")
            prRed(info[email]["Salary"])

            print("Contact Information:", end=" ")
            prGreen(info[email]["Contact Info"])

            print("Status: ", end=" ")
            if info[email]["Status"] == "offduty":
                prRed("Off Duty")
            else:
                prGreen("On Duty")


def addNewStaff():
    print("Adding new staff")
    print("Chose the role")
    print("\t1. Admin")
    print("\t2. Manager")
    print("\t3. Chef")
    print("\t0. Cancel")

    error = True
    cancelled = False
    newRole = ""
    while error:
        try:
            newRoleIndex = int(input("Enter the index >> "))
            if newRoleIndex == 0:
                error = False
                cancelled = True
                prPurple("Cancelled!!")
            elif newRoleIndex == 1:
                newRole = "Admin"
                error = False
            elif newRoleIndex == 2:
                newRole = "Manager"
                error = False
            elif newRoleIndex == 3:
                newRole = "Chef"
                error = False
            else:
                prRed("Please enter a valid index!!")

        except Exception as e:
            newRole = None
            prRed(e)

    if not cancelled:
        newNickname = input("enter the new staff's nickname: ")	

        # Checks if the email already exists.
        while True:
            info = readCredentials()
            newEmail = input("enter the new staff's email: ")	
            if newEmail in info:
                prRed("Email already exists in the system")
            else:
                break
            
        newPassword = input("enter the new staff's password: ")	
        newSalary = input("enter the new staff's salary: ")	
        newContactInfo = input("Enter the new staff's contact number: ")	

        data = f"\n{newRole} {newNickname} {newEmail} {newPassword} offduty {newSalary} {newContactInfo}"
        appendCredentials(data)


def editStaff():
    
    info = readCredentials();
    prRed("Edit staff information")

    indexingStaff = {}
    indexingStaff[0] = "Cancel" # Implementing a cancel function if the user has wrongly typed
    index = 1
    for email in info:
        if info[email]["Role"] in ["Manager", "Chef"]:
            print("Here")
            prLightPurple(f"{index}")

            print(" Nickname:", end="")
            prGreen(f"{info[email]["Nickname"]}")

            print(" Role:", end="")
            prPurple(info[email]["Role"])

            print(" Email:", end="")
            prYellow(email)

            indexingStaff[index] = email
            index += 1

    while True:
        staffEdit = int(input("Enter the index of the staff's information you want to edit >> "))
        if staffEdit not in indexingStaff:
            prRed("Please select a valid index!!")
            proceed = False
        elif staffEdit == 0:
            prLightGray("Cancelling operation!!")
            proceed = False
            break

        else:
            prGreen(f"Editing {info[indexingStaff[staffEdit]]["Nickname"]}'s information")
            selectedEmail = indexingStaff[staffEdit]
            prGreen(selectedEmail)
            proceed = True
            break

    if proceed:
        while True:
            print()
            print("\t1. Nickname")
            print("\t2. Email")
            print("\t3. Role")
            print("\t4. Salary")
            prRed("\t5. Delete current staff")
            print("\t0. Save & Exit")
            print()

            editCommand = int(input("Enter the index >> "))

            # Terminating the editing process 
            if editCommand == 0:
                writeCredentials(info)
                break

            # Editing the nickname of the staff
            elif editCommand == 1:
                newName = input("Enter the new nickname: ")
                while newName in ["", " "]:
                    print()
                    prGreen("Please enter a proper nickname!!")
                    newName = input("Enter the proper nickname: ")

                info[selectedEmail]["Nickname"]	= newName

            elif editCommand == 2: 
                newEmail = input("Enter the new email: ")
                if verifyEmail(newEmail):
                    while True:
                        if newEmail.find("@") and newEmail.find(".") and newEmail.strip():
                            info[newEmail] = info[selectedEmail]
                            del info[selectedEmail]
                            selectedEmail = newEmail
                            break

                        print()
                        prRed("Please enter a valid email!!")
                        newEmail = input("Enter the new email: ")

                        # Modifying the email by first creating a new record with the new email but the same body and then 
                        # deleting the old record

                else:
                    prRed("Invalid email address!!")


            # Changing the role of the staff
            elif editCommand == 3:
                prGreen("Select the new role!")
                print("\t1. Manager")
                print("\t2. Chef")
                print("\t0. Cancel")
                print()
                valid = False

                while True:
                    newRole = int(input("Enter the index >> "))

                    if newRole == 1:
                        info[selectedEmail]["Role"] = "Manager"
                        break
                    elif newRole == 2:
                        info[selectedEmail]["Role"] = "Chef"
                        break
                    elif newRole == 0:
                        prRed("Cancelling operation!")
                        break
                    else:
                        prRed("Please input a valid index!!")


            # Editing the salary
            elif editCommand == 4:
                while True:
                    try:
                        newSalary = int(input("Please enter the new salary: "))
                        info[selectedEmail]["Salary"] = newSalary
                        break
                    except Exception as e:
                        prRed("Please enter a valid number!!")


            elif editCommand == 5:
                confirmation = input("Are you sure you want to delete your account(Y/N): ").lower()
                if confirmation == "y":
                    del info[selectedEmail]
                    prLightPurple(f"Deleting account with email: {adminEmail}")
                else:
                    prRed("Cancelled operation!")


def deleteStaff():
    info = readCredentials()
    change = False
    while True:
        emailDel = input("Enter the email address of the staff you want to delete (Type '0' to cancel'): ")
        if emailDel in info:
            print("Email found, deleting entity!")
            change = True 
            break
        else:
            prRed("This email is not found in the system!! Please try again.")

    if emailDel != "0" and change:
        prRed(f"Deleting data about {info[emailDel]["Nickname"]}")
        del info[emailDel]
        writeCredentials(info)

    if emailDel == "0":
        prRed("Cancelling operation!!")


def viewFeedback():
    prGreen("Customer feedbacks\n")
    with open("Dataset/feedback.txt", "r") as file:
        feedbacks = [i for i in file.read().split("\n") if i != ""]
        for line in feedbacks:
            data = line.split(": ")
            prLightPurple(data[0])
            print(data[1])
            print()



def editOwnProfile(adminEmail):

    info = readCredentials()

    print()
    prGreen("Editing own information")
    print("\t1. Nickname")
    print("\t2. Email")
    print("\t3. Password")
    print("\t4. Salary")

    prRed("\t5. Delete own account")
    print("\t0. Save & Exit")
    print()

    while True:
        editCommand = int(input("Enter the index of the command you want to execute >> "))

        if editCommand == 0:
            writeCredentials(info)
            break
        else:
            if editCommand == 1:
                newNickname = input("Enter your new nickname: ")
                info[adminEmail]["Nickname"] = newNickname

            elif editCommand == 2:
                newEmail = input("Enter your new email: ")
                if verifyEmail(newEmail):
                    info[newEmail] = info[adminEmail]
                    del info[adminEmail]
                    adminEmail = newEmail
                else:
                    prRed("Invalid email address!!")


            elif editCommand == 3:
                newPassword = input("Enter your new password: ")
                info[adminEmail]["Password"] = newPassword

            elif editCommand == 4:
                newSalary = input("Enter your new salary: ")
                info[adminEmail]["Salary"] = newSalary

            elif editCommand == 5:
                confirmation = input("Are you sure you want to delete your account(Y/N): ").lower()
                if confirmation == "y":
                    prLightPurple(f"Deleting account with email: {adminEmail}")
                    del info[adminEmail]
                    prRed("Loging out of the system!")
                    writeCredentials(info)
                    quit()
                else:
                    prRed("Cancelling operation!")

            else:
                prRed("Invalid index!!")
    return adminEmail

def viewSales():
    sales = readSales()
    infoCred = readCredentials()

    indexingChef = {}
    index = 1
    indexingChef[0] = "Cancel"

    for email in infoCred:
        if infoCred[email]["Role"] == "Chef":

            prLightPurple(f"{index}")
            print("Name: ", end='')
            prGreen(infoCred[email]["Nickname"])

            indexingChef[index] = email
            index += 1

    prRed("0")
    prRed("Cancel")

    proceed = False
    while True:
        selectedChef = int(input("\nEnter the index of the chef you want to view: "))
        if selectedChef not in indexingChef:
            prRed("Please select a valid index!!")
        elif selectedChef == 0:
            print("Cancelling operation!!")
            break
        else:
            proceed = True 
            break

    if proceed:
        while True:
            month = int(input("Enter the month index: "))
            if month not in range(1, 13):
                prRed("Please select a valid month index!!")
            else:
                break

        print("\nName: ", end="")
        prLightPurple(f"{infoCred[indexingChef[selectedChef]]["Nickname"]}")

        total_sales = 0

        for index in sales:
            if sales[index]["Chef"] == indexingChef[selectedChef] and int(sales[index]["Month"]) == month:
                total_sales += float(sales[index]["Amount"])

        print("Total Sales: ", end="")
        prRed(total_sales)

def adminFunctions(adminEmail):
    featuresMessage = """
    Admin features:
    1. View all the staff information (Manager, Chef).

    2. Add a new staff.
    3. Edit information about an existing staff.
    4. Delete a staff.

    5. View the monthly sales report.
    6. View customer feedbacks.

    7. Edit own profile.

    8. Display the command message

    0. Logout
    """
    print(featuresMessage)

    while True:
        try:
            command = int(input("\033[93m {}\033[00m".format("\nEnter the command index >>  ")))

            if command == 1:
                viewStaff()

            elif command == 2:
                addNewStaff()

            elif command == 3:
                editStaff()

            elif command == 4:
                deleteStaff()

            elif command == 5:
                viewSales()

            elif command == 6:
                viewFeedback()

            elif command == 7:
                adminEmail = editOwnProfile(adminEmail)

            elif command == 8:
                os.system("cls")
                print(featuresMessage)

            elif command == 0:
                prRed("Logging out of the system!")
                break

        except Exception as e:
            print(e)

adminFunctions("sk")