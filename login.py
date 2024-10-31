from datasetManipulation import readCredentials
from styles import *
import os

def checkLogin():
	credentials = readCredentials() # Reading the credentials file
	os.system("cls") # Clear the terminal

	print("\nWelcome to the restaurant!!")
	print("Please login to the system\n")

	chances = 3
	response = False

	while chances > 0:
		emailInput = input("Please enter your email: ")

		if emailInput in credentials: # Checking if the email the user has input indeed is registered or not
			# These 2 variables are used in order to create a loop to allow the user to have a max of 3 attempts
			response = True
			currentRole = credentials[emailInput]["Role"]
			nickname = credentials[emailInput]["Nickname"]
			count = 1
			# The loop will verify if count is < or equal to 3 which refers to the max attemps
			while count <= 3:
				passwInput = input("Please enter your password: ")
				if passwInput == credentials[emailInput]["Password"]: # Verify if the password entered matches the password stored
					os.system("cls")
					print()
					prGreen("Login Successful!") # Print this statement in green
					prLightPurple(f"Role: {currentRole}")
					print(f" Hi {nickname}!")
					break  # This will break the loop at any times if ever the password is correct, this will prevent the loop from running again if the password was found and the user had some attempts left

				# If the password as incorrect then an appropriate message is displayed and count is incremented by one which means that the user has used an attempt
				else: 
					print("Incorrect password!")
					count += 1 
			# If the user has used all 3 attemps then an error message is sent
			else:
				prRed("Too many failed attemps, closing program")
		else:
			print("Error, email not found")
			chances -= 1
			return {"email": emailInput, "response": response, "role": "None"}
		return {"email": emailInput, "response": response, "role": currentRole}
