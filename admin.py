from datasetManipulation import readCredentials, appendCredentials, writeCredentials
import os 
from styles import *
 
# for validating an Email
import re
def verifyEmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False

def adminFunctions(adminEmail):

	# Help message which will be displayed incase the user input an invalid command.
	featuresMessage = """
	Admin features:
	1. View all the staff information (Manager, Chef).

	2. Add a new staff.
	3. Edit information about an existing staff.
	4. Delete a staff.

	5. View the monthly sales report.

	6. Edit own profile.

	7. Display the command message

	0. Logout
	"""

	print(featuresMessage)

	while True:
		try:
			# The message displayed will be of yellow-ish color`
			command = int(input("\033[93m {}\033[00m".format("\nEnter the command index >>  ")))

			if command == 1:

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

					# Checking if the role is customer
					elif info[email]["Role"] == "Customer":

						print()

						print("Nickname:", end=" ")
						prGreen(f"{info[email]["Nickname"]}")

						print("Role:", end=" ")
						prPurple(info[email]["Role"])

						print("Email:", end=" ")
						prYellow(email)

						print("Number of visits:", end=" ")
						prRed(info[email]["NumberOfVisit"])

						print("Contact Information:", end=" ")
						prGreen(info[email]["Contact Info"])


					print() # Empty line for display purposes

			elif command == 2:
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
					newNickname = input("Enter the new staff's nickname: ")	
					newPassword = input("Enter the new staff's password: ")	
					newEmail = input("Enter the new staff's email: ")	
					newSalary = input("Enter the new staff's salary: ")	
					newContactInfo = input("Enter the new staff's contact number: ")	

					print(newRole)
					data = f"\n{newRole} {newNickname} {newEmail} {newPassword} offduty {newSalary} {newContactInfo}"
					appendCredentials(data)

			# Command 3 >> Editing a particular staff data
			elif command == 3:
				info = readCredentials();
				prRed("Edit staff information")

				indexingStaff = {}
				indexingStaff[0] = "Cancel" # Implementing a cancel function if the user has wrongly typed
				index = 1
				for email in info:
					if info[email]["Role"] in ["Manager", "Chef"]:
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
					elif staffEdit == 0:
						prLightGray("Cancelling operation!!")
						break

					else:
						prGreen(f"Editing {info[indexingStaff[staffEdit]]["Nickname"]}'s information")
						selectedEmail = indexingStaff[staffEdit]
						prGreen(selectedEmail)
						break

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
									break
								print()
								prRed("Please enter a valid email!!")
								newEmail = input("Enter the new email: ")

							# Modifying the email by first creating a new record with the new email but the same body and then 
							# deleting the old record
							info[newEmail] = info[selectedEmail]
							del info[selectedEmail]
							selectedEmail = newEmail

						else:
							prRed("Invalid email address!!")


					# Changing the role of the staff
					elif editCommand == 3:
						prGreen("Select the new role!")
						print("\t1. Admin")
						print("\t2. Manager")
						print("\t3. Chef")
						print()
						valid = False

						while not valid:
							newRole = int(input("Enter the index >> "))
							if newRole in [1, 2, 3]:
								if newRole == 1:
									tempBuffer = info[selectedEmail]
									info[selectedEmail] = {"Role": "Admin", "Nickname": tempBuffer["Nickname"], "Salary": tempBuffer["Salary"], "Contact Info": tempBuffer["Contact Info"], "Password": tempBuffer["Password"]}

								elif newRole == 2:
									info[selectedEmail]["Role"] = "Manger"
								elif newRole == 3:
									info[selectedEmail]["Role"] = "Chef"
								else:
									prRed("Please input a valid index!!")
										
								print(info)

							valid = True

					# Editing the salary
					elif editCommand == 4:
						while True:
							try:
								newSalary = int(input("Please enter the new salary: "))
								break
							except Exception as e:
								prRed("Please enter a valid number!!")
						info[selectedEmail]["Salary"] = newSalary


					elif editCommand == 5:
						confirmation = input("Are you sure you want to delete your account(Y/N): ").lower()
						if confirmation == "y":
							del info[selectedEmail]
							prLightPurple(f"Deleting account with email: {adminEmail}")
						else:
							prRed("Cancelled operation!")

			elif command == 4:
				info = readCredentials()
				while True:
					emailDel = input("Enter the email address of the staff you want to delete (Type '0' to cancel'): ")
					if emailDel in info or emailDel == '0':
						print("Email found, deleting entity!")
						break
					else:
						prRed("This email is not found in the system!! Please try again.")

				if emailDel != "0":
					prRed(f"Deleting data about {info[emailDel]["Nickname"]}")
					del info[emailDel]

				# Re-writing all the data with the updated value
				writeCredentials(info)


			# Yet to be implemented
			elif command == 5:
				pass

			elif command == 6:
				
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
								return
							else:
								prRed("Cancelling operation!")

						else:
							prRed("Invalid index!!")


			elif command == 7:
				os.system("cls")
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

