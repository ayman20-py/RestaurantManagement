from styles import *

def readCredentials():
	info = {}
	with open("Dataset/credentials.txt", "r") as file: # Open the file for read
		buffer = file.read() # Reading the file's contents
		rawData = [i for i in buffer.split("\n") if i != ""] # Splitting the content by lines and ignoring any blank lines in the textfile
		for stringData in rawData:
			data = stringData.split(" ") # Splitting each lines by the whitespace

			currentRole = data[0]
			currentEmail = data[2]
			# Creates an Admin record
			if currentRole == "Admin":
				info[currentEmail] = {"Role": currentRole, "Nickname": data[1], "Password": data[3], "Salary": data[4], "Contact Info": data[5]}

			# Creates a Manager record
			if currentRole == "Manager": 
				info[currentEmail] = {"Role": currentRole, "Nickname": data[1], "Password": data[3], "Status": data[4], "Salary": data[5], "Contact Info": data[6]}

			# Creates a Chef record
			if currentRole == "Chef": 
				info[currentEmail] = {"Role": currentRole, "Nickname": data[1], "Password": data[3], "Status": data[4], "Salary": data[5], "Contact Info": data[6]}

			# Creates a Customer record
			if currentRole == "Customer":
				info[currentEmail] = {"Role": currentRole, "Nickname": data[1], "Password": data[3], "NumberOfVisit": int(data[4]), "Contact Info": data[5]}

	# Returns all the informations in a dictionary format
	return info
	

def appendCredentials(data):
	with open("Dataset/credentials.txt", "a") as file:
		file.write(str(data))

def writeCredentials(newData):
	with open("Dataset/credentials.txt", "w") as file:
		infoList = []
		for email in newData:
			data = newData[email]
			if data["Role"] == "Admin":
				buffer = f"{data["Role"]} {data["Nickname"]} {email} {data["Password"]} {data["Salary"]} {data["Contact Info"]}"
			elif data["Role"] == "Manager" or data["Role"] == "Chef":
				buffer = f"{data["Role"]} {data["Nickname"]} {email} {data["Password"]} {data["Status"]} {data["Salary"]} {data["Contact Info"]}"
			elif data["Role"] == "Customer":
				buffer = f"{data["Role"]} {data["Nickname"]} {email} {data["Password"]} {data["NumberOfVisit"]} {data["Contact Info"]}"

			infoList.append(buffer)

		infoString = "\n".join(infoList)

		file.write(infoString)
		prGreen("Data has successfully been modified!!")

def readMenu():
	with open("Dataset/menu.txt", "r") as file:
		info = {}
		buffer = file.read()
		rawData = [i for i in buffer.split("\n") if i != ""]
		for i in rawData:
			data = i.split(", ")
			dishType = data[0]
			dishName = data[1]
			dishPrice = data[2]
			ingredients = data[3:]

			info[dishName] = {"Type": dishType, "Price": dishPrice, "Ingredients": ingredients}

	print(info)
	return info

def appendMenu(data):
	with open("Dataset/menu.txt", "w") as file:
		file.write(str(data))
