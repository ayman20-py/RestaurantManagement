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

# Writing functions will take in a dictionary itself and break it down before writing in the file
def writeCredentials(newData):
	with open("Dataset/credentials.txt", "w") as file:
		infoList = []

		# Break down every 
		for email in newData:
			data = newData[email]
			if data["Role"] == "Admin":
				buffer = f"{data["Role"]} {data["Nickname"]} {email} {data["Password"]} {data["Salary"]} {data["Contact Info"]}"
			elif data["Role"] == "Manager":
				buffer = f"{data["Role"]} {data["Nickname"]} {email} {data["Password"]} {data["Status"]} {data["Salary"]} {data["Contact Info"]}"
			elif data["Role"] == "Chef":
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

	return info

def appendMenu(data):
	with open("Dataset/menu.txt", "a") as file:
		file.write(str(data))

# Writing functions will take in a dictionary itself and break it down before writing in the file
def writeMenu(newData):
	with open('Dataset/menu.txt', "w") as file:
		infoList = []
		for dish in newData:
			data = newData[dish]
			line = f"{data["Type"]}, {dish}, {data["Price"]}, {", ".join(data["Ingredients"])}"
			infoList.append(line)
			
			print(line)
		

		file.write("\n".join(infoList))

	prGreen("Data has successfully been modified!!")


def readOrders():
    orders = {}
    index = 1
    with open("Dataset/orders.txt", "r") as file:
    	buffer = file.read()
    	rawData = [i for i in buffer.split("\n") if i != ""]

    	for lines in rawData:
    		data = lines.split(",")
    		orders[index] = {"Customer": data[0], "Status": data[1], "Dish": []}
    		for dishes in data[2:]:
    			foods = [i for i in dishes.split(":") if i != ""] 
    			if foods != []:
	    			orders[index]["Dish"].append({"Dish Name": foods[0], "Quantity": foods[1]})

	    	index += 1
    return orders


# customer@gmail.com,Pending,Chicken Achari:2,Fatimah Butter:3
def writeOrders(orders):
	with open("Dataset/orders.txt", "w") as file:
		for index in orders:
			line = f"{orders[index]["Customer"]},{orders[index]["Status"]},"
			for i in orders[index]["Dish"]:
				line = f"{line}{i["Dish Name"]}:{i["Quantity"]},"

			
			file.write(f"{line}\n")

def readIngredients():
	ingredients = {}
	index = 1
	with open("Dataset/ingredients.txt", "r") as file:
		rawData = file.read()
		data = [i for i in rawData.split("\n") if i != ""]
		for rawLine in data:
			line = rawLine.split(",")
			ingredients[index] = {"Chef": line[0], "Ingredient": line[1], "Quantity": line[2]}
			index += 1

	return ingredients

def writeIngredients(ingredients):
	with open("Dataset/ingredients.txt", "w") as file:
		for index in ingredients:
			currentIngredient = ingredients[index]
			line = f"{currentIngredient["Chef"]},{currentIngredient["Ingredient"]},{currentIngredient["Quantity"]}"
			print(line)
			file.write(f"{line}\n")

def readSales():
	sales = {}
	index = 1
	with open("Dataset/salesreport.txt", "r") as file:
		rawData = file.read()
		data = [i for i in rawData.split("\n") if i != ""]
		for rawLine in data:
			line = rawLine.split(',')
			sales[index] = {"Chef": line[0], "Month": line[1], "Amount": line[2]}
			index += 1

	return sales

def writeSales(sales):
	with open("Dataset/salesreport.txt", "w") as file:
		for index in sales:
			currentSale = sales[index]
			line = f"{currentSale["Chef"]},{currentSale["Month"]},{currentSale["Amount"]}"
			file.write(f"{line}\n")
