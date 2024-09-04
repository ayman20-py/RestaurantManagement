from datasetManipulation import readCredentials, appendCredentials, writeCredentials
import os 
from styles import *
import re
 
# for validating an Email
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

					if info[email]["Role"] in ["Chef", "Manager"]:

						print()

						print("Nickname:", end=" ")
						prGreen(f"{info[email]["Nickname"]}")

						print("Role:", end="")
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

					elif info[email]["Role"] == "Customer":

						# Customer Tim customer1@gmail.com pass 3 602858194727
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
					command = int(input("Enter the index of the staff's information you want to edit >> "))
					if command not in indexingStaff:
						prRed("Please select a valid index!!")
					elif command == 0:
						prLightGrey("Cancelling operation!!")
						break

					else:
						prGreen(f"Editing {info[indexingStaff[command]]["Nickname"]}'s information")
						selectedEmail = indexingStaff[command]
						prGreen(selectedEmail)
						break

				while True:
					print()
					print("1. Nickname")
					print("2. Email")
					print("3. Role")
					print("4. Salary")
					print("0. Save & Exit")
					print()

					command = int(input("Enter the index >> "))

					# Terminating the editing process 
					if command == 0:
						writeCredentials(info)
						break

					# Editing the nickname of the staff
					elif command == 1:
						newName = input("Enter the new nickname: ")
						while newName in ["", " "]:
							print()
							prRed("Please enter a proper nickname!!")
							newName = input("Enter the proper nickname: ")

						info[selectedEmail]["Nickname"]	= newName

					elif command == 2: 
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


					elif command == 3:
						prGreen("Select the new role!")
						print("1. Admin")
						print("2. Manager")
						print("3. Chef")
						print()
						valid = False
						while not valid:
							newRole = int(input("Enter the index >> "))
							if newRole in [1, 2, 3]:
								if newRole == 1:
									# RECHECK THIS STATEMENT
									info[selectedEmail]["Role"] = "Admin"
								elif newRole == 2:
									info[selectedEmail]["Role"] = "Manger"
								elif newRole == 3:
									info[selectedEmail]["Role"] = "Chef"
								else:
									print("An error occured!!")
										
								print(info)

							valid = True



			elif command == 4:
				info = readCredentials()
				while True:
					emailDel = input("Enter the email address of the staff you want to delete (Type '0' to cancel'): ")
					if emailDel in info or emailDel == '0':
						print("Email found deleting entity!")
						break
					else:
						prRed("This email is not found in the system!! Please try again.")

				if emailDel != "0":
					prRed(f"Deleting data about {info[emailDel]["Nickname"]}")
					del info[emailDel]

				writeCredentials(info)

			elif command == 5:
				pass

			elif command == 6:
				
				info = readCredentials()
				
				print()
				print("1. Nickname")
				print("2. Email")
				print("3. Password")
				print("4. Salary")
				print("0. Save & Exit")
				print()

				while True:
					command = int(input("Enter the index of the command you want to execute >> "))

					if command == 0:
						writeCredentials(info)
						break
					else:
						if command == 1:
							newNickname = input("Enter your new nickname: ")
							info[adminEmail]["Nickname"] = newNickname

						elif command == 2:
							newEmail = input("Enter your new email: ")
							if verifyEmail(newEmail):
								info[newEmail] = info[adminEmail]
								del info[adminEmail]
								adminEmail = newEmail
							else:
								prRed("Invalid email address!!")


						elif command == 3:
							newPassword = input("Enter your new password: ")
							info[adminEmail]["Password"] = newPassword

						elif command == 4:
							newSalary = input("Enter your new salary: ")
							info[adminEmail]["Salary"] = newSalary

						else:
							prRed("Invalid index!!")



			elif command == 7:
				os.system("cls")
				print(featuresMessage)

			# Logout of the program
			elif command == 0:
				print("Loging out of the system!")
				break

			else:
				prRed("This is an invalid command!")
				print(featuresMessage)
		except Exception as e:
			print(e)

