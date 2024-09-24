from login import checkLogin
from admin import adminFunctions
from manager import managerFunctions
from customer import customerFunctions
from chef import chef_menu

from styles import *

loginStatus = checkLogin()

if loginStatus["response"]:
	if loginStatus["role"] == "Admin":
		adminFunctions(loginStatus["email"])
	elif loginStatus["role"] == "Manager":
		managerFunctions(loginStatus["email"])
	elif loginStatus["role"] == "Chef":
		chef_menu(loginStatus["email"])
	elif loginStatus["role"] == "Customer":
		customerFunctions(loginStatus["email"])
	else:
		print("Work in progress")
else:
	prRed("Error")
