from login import checkLogin
from admin import adminFunctions
from styles import *

loginStatus = checkLogin()

if loginStatus["response"]:
	if loginStatus["role"] == "Admin":
		adminFunctions(loginStatus["email"])
	else:
		print("Work in progress")
else:
	prRed("Error")