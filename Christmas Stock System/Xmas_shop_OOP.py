import sqlite3

class DatabaseManager:

    def __init__(self,db_name):
        self._db = sqlite3.connect(db_name) #connect to db
        self.cursor = self._db.cursor() #cursor connection to allow for modification to db

    def insert_data(self): #insert 
        product_type = ["Food","Decoration","Electrical","Other"]
        sql = "insert into Product (Name, Type, Stock, Price) values (?, ?, ?, ?)" #sql command to insert
        name = input("Enter the Name: ")
        type = str("")
        while True:
            try:
                type = input("Enter the category of the product: (Food, Decoration, Electrical, Other) ")
            except ValueError: #if not valid str, not accepted
                print("Please input a valid product type: ")
                continue
            if type == "Food" or type == "Decoration" or type == "Electrical" or type == "Other":
                break
                #type was successfully parsed
                #wexit the loop.
            else:
                print("Please input a valid product type: ")
                continue
        stock = int(input("Enter the stock level of this product "))
        price = float(input("Insert the price "))
        values = (name, type, stock, price)
        self.cursor.execute(sql,values) #execute the sql command
        self._db.commit() #changes committed

    def select_stock(self):
        self.cursor.execute("SELECT Name, Type, Stock, Price FROM Product WHERE Stock > 0 ORDER BY Type DESC;")#sql command
        products = self.cursor.fetchall() #select all items stock
        print("Item Name:", "", "Item Type:","", "Price:")
        print("")
        for row in products: #organised item
            print("|", row[0], " | ", row[1], " | ", row[2],"in stock", "£", row[3], "|")
        print("")

    def select_all_products(self):
        self.cursor.execute("SELECT ProductID, Name, Type, Stock, Price FROM Product ORDER BY Type DESC ")
        products = self.cursor.fetchall() #select all items
        print("Product ID:","Item Name:","","Item Type:","","Item Stock Level:","","Price:")
        print("")
        for row in products: #organise all items
            print("|",row[0],"|","|",row[1],"|",row[2],"|",row[3],"avaliable","|","£",row[4],"|")
        print("")

    def select_product(self):
        id = input("Write the product's id: ")
        self.cursor.execute("select Name, Type, Stock, Price from Product where ProductID=?",(id)) #sql selection
        product = self.cursor.fetchone() #select one item
        print("Product ID:", "Item Name:", "", "Item Type:", "", "Item Stock Level:", "", "Price:")
        print("")
        for row in product: #display item
            print("|", row[0], "|", "|", row[1], "|", row[2], "|", row[3], "avaliable", "|", "£", row[4], "|")
        print("")

    def delete_product(self):
        item = input("Enter the Product ID of the item you want to delete: ") #input product id primary key
        self.cursor.execute("DELETE FROM Product WHERE ProductID=" + item) #del item sql command
        self._db.commit() #commit changes
        print("The product has been deleted.")

    def sold(self):
        item = input("Which items stock needs updating: ")
        name = "'" + item + "'"
        sold = int(input("How much stock of the item was sold: "))
        self.cursor.execute("SELECT * FROM Product WHERE Name = " + name)
        products = self.cursor.fetchall()
        for row in products:
            stock_amount = row[3]
        total_stock = stock_amount - sold
        sql = "UPDATE Product SET Stock=? WHERE Name =?"
        data = (total_stock, item)
        self.cursor.execute(sql, data)
        self._db.commit()

    def stock_order(self):
        item = input("Which items stock needs updating: ")
        name = "'" + item + "'"
        delivered = int(input("How much stock of the item was ordered: "))
        self.cursor.execute("SELECT * FROM Product WHERE Name = " + name)
        products = self.cursor.fetchall()
        for row in products:
            stock_amount = row[3]
        total_stock = stock_amount + delivered
        sql = "UPDATE Product SET Stock =? WHERE Name =?"
        data = (total_stock, item)
        self.cursor.execute(sql, data)
        self._db.commit()

    def update_product_stock(self):
        print("Has the stock been sold or are you going to order some?")
        choice = input("(sold/order): ")
        if choice == "sold":
            self.sold()
        elif choice == "order":
            self.stock_order()

    def update_product(self):
        item = input("Which product do you want to update? (Enter the ID ")
        name = "'" + item + "'"
        new_price = float(input("Update the price: "))
        product = self.cursor.fetchone()
        sql = "UPDATE Product SET Price=? WHERE Name =?"
        data = (new_price, item)
        self.cursor.execute(sql, data)
        self._db.commit()

    #Customers Table functions

    def insert_customer(self):
        first_name = input("Enter the first name: ")
        last_name = input("Enter the last name ")
        address = input("Enter the first line of their address ")
        postcode = input("Enter the postcode they are from ")
        phone_number = int(input("Enter phone number "))
        sql = "insert into Customers (firstName, lastName, AddressLine1, Postcode, PhoneNumber) values (?, ?, ?, ?, ?)"
        values = (first_name,last_name,address,postcode,phone_number)
        self.cursor.execute(sql,values)
        self._db.commit()

    def view_all_customers(self):
        self.cursor.execute("SELECT CustomerID, firstName, lastName, AddressLine1, Postcode, PhoneNumber FROM Customers ")
        products = self.cursor.fetchall()
        print("Customer ID:","First Name:","","Last Name:","","Address Line 1","","Postcode","","Phone Number:")
        print("")
        for row in products:
            print("|",row[0],"|",row[1],"|",row[2],"|",row[3],"|",row[4],"|",row[5],"|")
        print("")

    def select_customer(self):
        id = input("Write the Customer's ID number: ")
        self.cursor.execute("select firstName, lastName, AddressLine1, Postcode, PhoneNumber from Customers where CustomerID="+ id)
        product = self.cursor.fetchone()
        print(product)

    def delete_customer(self):
        selected = input("Enter the Customer ID of the customer you want to delete: ")
        self.cursor.execute("DELETE FROM Customers WHERE CustomerID=" + selected)
        self._db.commit()
        print("The customer has been deleted. ")

    def update_postcode(self):
        id = input("Which customer's postcode do you want to update? (Enter the customer's ID) ")
        new_postcode = input("Enter the new postcode: ")
        sql = "UPDATE Customers SET Postcode=? WHERE CustomerID =?"
        data = (new_postcode, id)
        self.cursor.execute(sql, data)
        self._db.commit()

    def update_address_line(self):
        id = input("Which customer's address line do you want to update? (Enter the customer's ID)")
        new_AdLine = input("Update the price: ")
        sql = "UPDATE Customers SET AddressLine1=? WHERE CustomerID =?"
        data = (new_AdLine, id)
        self.cursor.execute(sql, data)
        self._db.commit()

    def update_phone_number(self):
        id = input("Which customer's phone number do you want to update? (Enter the customer's ID)")
        new_phone = int(input("Enter the new phone number: "))
        sql = "UPDATE Customers SET PhoneNumber=? WHERE CustomerID =?"
        data = (new_phone, id)
        self.cursor.execute(sql, data)
        self._db.commit()


    def purchase(self):
        confirm =  False
        while confirm == False:
            customerID = input("Enter your Customer ID: ")
            print("")
            self.select_stock()
            print("")
            item = input("Which item(s) would you like to purchase: ")
            name = "'" + item + "'"
            quantity = int(input("How many do you want to buy: "))
            self.cursor.execute("SELECT * FROM Product WHERE Name = " + name)
            products = self.cursor.fetchall()
            for row in products:
                stock_level = row[3]
                stock_price = row[4]
                productID = row[0]
            total_stock = stock_level - quantity
            total_price = 0
            total_price = total_price + (stock_price * quantity)
            sql = "UPDATE Product SET Stock=? WHERE Name =?"
            data = (total_stock, item)
            self.cursor.execute(sql, data)
            self._db.commit()
            print("Total £", total_price)
            choice = input("Do you want to purchase another product? (y/n)")
            if choice == "n":
                date = input("Please enter the date of Purchase: ")
                sql = "INSERT INTO CustomerOrder (Date, Price, ProductID, CustomerID) VALUES (?, ?, ?, ?) "
                data = (date, total_price, productID, customerID)
                self.cursor.execute(sql, data)
                self._db.commit()
                confirm = True
            else:
                confirm = False

    def order_history(self):
        customerID = input("Enter Customer ID: ")
        customerID = "'"+ customerID +"'"
        self.cursor.execute("SELECT * FROM CustomerOrder WHERE CustomerID ="+ customerID)
        records = self.cursor.fetchall()
        for record in records:
            print("OrderID = ", record[0], )
            print("DatePurchase = ", record[1])
            print("Price  = ", record[2])
            print("ProductID  = ", record[3])
            print("")


    def shop_options(self):
        print("Welcome to the Christmas Shop!!")
        print("")
        print("What would you like to do:")
        print("")
        print("1. See all items available")
        print("2. Create an Order ")
        print("3. View your order history")
        print("0. Return to table selection ")
        print("")
        print("Please select an option: ")

    def options1(self):
        print("Product Table Menu:")
        print("")
        print("1. Add New product ")
        print("2. Update the stock of a product ")
        print("3. Update a product's price")
        print("4. Delete existing product ")
        print("5. Select a product")
        print("6. Select all products in stock ")
        print("7. View all products ")
        print("0. Return to table selection ")
        print("")
        print("Please select an option: ")

    def options2(self):
        print("Customer Table Menu:")
        print("")
        print("1. Add New customer ")
        print("2. Update customer's Address Line ")
        print("3. Update customer's Postcode ")
        print("4. Update customer's Phone Number")
        print("5. Delete customer ")
        print("6. Select customer")
        print("7. Select all customers ")
        print("0. Return to table selection ")
        print("")
        print("Please select an option: ")

    def shop_menu(self):
        self.options2()
        leave = False

        while leave == False:
            choice = input("> ")
            if choice == "1":
                self.select_stock()
                self.shop_options()
            elif choice == "2":
                self.purchase()
                self.shop_options()
            elif choice == "3":
                self.order_history()
                self.shop_options()
            elif choice == "0":
                print("Exiting menu")
                self.menu0()

    def menu2(self):
        self.options2()
        leave = False

        while leave == False:
            choice = input("> ")
            if choice == "1":
                self.insert_customer()
                self.options2()
            elif choice == "2":
                self.update_address_line()
                self.options2()
            elif choice == "3":
                self.update_postcode()
                self.options2()
            elif choice == "4":
                self.update_phone_number()
                self.options2()
            elif choice == "5":
                self.delete_customer()
                self.options2()
            elif choice == "6":
                self.select_customer()
                self.options2()
            elif choice == "7":
                self.view_all_customers()
                self.options2()
            elif choice == "0":
                print("Exiting menu")
                self.menu0()

    def menu1(self):
        self.options1()
        leave = False

        while leave == False:
            choice = input("> ")
            if choice == "1":
                self.insert_data()
                self.options1()
            elif choice == "2":
                self.update_product_stock()
                self.options1()
            elif choice == "3":
                self.update_product()
                self.options1()
            elif choice == "4":
                self.delete_product()
                self.options1()
            elif choice == "5":
                self.select_product()
                self.options1()
            elif choice == "6":
                self.select_stock()
                self.options1()
            elif choice == "7":
                self.select_all_products()
                self.options1()
            elif choice == "0":
                print("Exiting menu")
                self.menu0()

    def menu0(self):
        print("Which table would you like to access in the christmas_shop database")
        print("")
        print("1. Products")
        print("2. Customers")
        print("3. Customer Menu")
        print("0. Exit")
        exit = False
        
        while exit == False:
            option = input("> ")
            if option == "1":
                self.menu1()
            elif option == "2":
                self.menu2()
            elif option == "3":
                self.shop_menu()
            elif option == "0":
                print("Shutting down database")
                exit = True
                break
    
    
if __name__ == "__main__":
    db_system = DatabaseManager("christmas_shop.db")
    db_system.menu0()
