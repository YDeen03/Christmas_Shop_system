import sqlite3


def create_table(db_name, table_name, sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("select name from sqlite_master where name =?", (table_name,))
        result = cursor.fetchall()
        keep_table = True
        if len(result) == 1:
            response = input("The table {0} already exists, do you wish to recreate it (y/n): ".format(table_name))
            if response == "y":
                keep_table = False
                print("The {0} table will be recreated - all existing data will be lost".format(table_name))
                cursor.execute("drop table if exists {0}".format(table_name))
                db.commit()
            else:
                print("The existing table was kept")
        else:
            keep_table = False
        if not keep_table:
            cursor.execute(sql)
            db.commit()


def create_table(db_name,table_name,sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("select name from sqlite_master where name =?",(table_name,))
        result = cursor.fetchall()
        keep_table = True
        if len(result) == 1:
            response = input("The table {0} already exists, do you wish to recreate it (y/n): ".format(table_name))
            if response == "y":
                keep_table = False
                print("The {0} table will be recreated - all existing data will be lost".format(table_name))
                cursor.execute("drop table if exists {0}".format(table_name))
                db.commit()
            else:
                print("The existing table was kept")
        else:
            keep_table = False
        if not keep_table:
            cursor.execute(sql)
            db.commit()

if __name__ == '__main__':
    db_name = "christmas_shop.db"
    sql1 = """CREATE TABLE "Product" (
	            "ProductID"	INTEGER UNIQUE,
	            "Name"	TEXT,
	            "Type"	TEXT,
	            "Stock"	INTEGER,
	            "Price"	REAL,
	            PRIMARY KEY("ProductID"));"""
    sql2 = """CREATE TABLE Customers
	            ("CustomerID"	INTEGER UNIQUE,
	            "firstName"	TEXT,
	            "lastName"	TEXT,
	            "AddressLine1"	TEXT,
	            "Postcode"	TEXT,
	            "PhoneNumber"	INTEGER,
	            PRIMARY KEY("CustomerID"));"""
    sql3 = """CREATE TABLE CustomerOrder
                (OrderID INTEGER UNIQUE,
                Date TEXT,
                Price REAL,
                CustomerID INTEGER UNIQUE,
                ProductID INTEGER UNIQUE,
                Primary Key(OrderID),
                Foreign Key(ProductID) references Product(ProductID)
                ON UPDATE CASCADE ON DELETE Restrict,
                Foreign Key(CustomerID) references Customers(CustomerID)
                ON UPDATE CASCADE ON DELETE Restrict);"""
    sql4 = """CREATE TABLE OrderItem
                (OrderItemID INTEGER UNIQUE,
                OrderID INTEGER UNIQUE,
                ProductID INTEGER UNIQUE,
                Primary Key(OrderItemID),
                Foreign Key(OrderID) references CustomerOrder(OrderID)
                ON UPDATE CASCADE ON DELETE Restrict,
                Foreign Key(ProductID) references Product(ProductID)
                ON UPDATE CASCADE ON DELETE Restrict);"""
    #create_table(db_name, "Product", sql1)
    #create_table(db_name, "Customers", sql2)
    create_table(db_name, "CustomerOrder", sql3)
    #create_table(db_name, "OrderItem", sql4)