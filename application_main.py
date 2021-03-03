import pymysql
import os
from dotenv import load_dotenv
import csv
import functools
from time import sleep
from datetime import datetime

# Load environment variables from .env file
load_dotenv()
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")

# Establish a database connection
connection = pymysql.connect(
    host,
    user,
    password,
    database
)
# A cursor is an object that represents a DB cursor,
# which is used to manage the context of a fetch operation.
cursor = connection.cursor()

products_list = []     
couriers_list = []
orders_list = []
product_items_list = []

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def current_time():
    now = datetime.now().time() 
    current_time = now.strftime("%H:%M")
    print("Current Time =", current_time)

def exception_command():
    print(f"{bcolors.FAIL}Incorrect Selection, Please try again!{bcolors.ENDC}")
    sleep(2)

def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')

# Load products from DB to List (Cache)
def cache_products():
    products_list.clear()
    connection = pymysql.connect(host, user, password, database) 
    with connection.cursor() as cursor:
        sql = "SELECT * FROM products"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            products_list.append(row)
    connection.close() 
    # print(products_list)

# Load couriers from DB to List (Cache)
def cache_couriers():
    couriers_list.clear()
    connection = pymysql.connect(host, user, password, database)
    with connection.cursor() as cursor:
        sql = "SELECT * FROM couriers"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            couriers_list.append(row)
    connection.close()
    # print(couriers_list)

# Load orders from DB to list (Cache)
def cache_orders():
    orders_list.clear()
    connection = pymysql.connect(host, user, password, database)
    with connection.cursor() as cursor:
        sql = "SELECT * FROM orders"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            orders_list.append(row)
    connection.close()
    # print(orders_list)

def refresh_caches():
    cache_products()
    cache_couriers()
    cache_orders()

#Divivder
def print_divider():
    print(80 * "-")

def welcome_message():
    print("""
 _  _ ____ __    ___ __  _  _ ____    ____ __     _  _  __   ___     ___     ___ _  _ ____ ____ ____ ____       
/ )( (  __(  )  / __/  \( \/ (  __)  (_  _/  \   ( \/ )/ _\ / __)   ( _ \   / __/ )( (  __(  __/ ___(  __)      
\ /\ /) _)/ (_/( (_(  O / \/ \) _)     )((  O )  / \/ /    ( (__   / _  /  ( (__) __ () _) ) _)\___ \) _)       
(_/\_(____\____/\___\__/\_)(_(____)   (__)\__/   \_)(_\_/\_/\___)  \__\_)   \___\_)(_(____(____(____(____)      
""")

def intro_menu():
    print(f"""{bcolors.OKGREEN}
    Welcome to Mac & Cheese Restaurant \n
    Choose a option from the list below \n
    (0) = Save & Exit Application
    (1) = Product Menu
    (2) = Courier Menu
    (3) = Order Menu
    {bcolors.ENDC}""")

#Start up Message Text & Calling
def intro():
    print_divider()
    current_time()
    print_divider()
    intro_menu()
    print_divider()

    #Start Menu 
    choice1 = input("Enter Option: \n")
    choice1 = int(choice1)
    if choice1 == 1:
        products_menu_function()
    elif choice1 == 2:
        courier_menu_function()
    elif choice1 == 3:
        order_menu_function()
    elif choice1 == 0:
        connection.close()
        print(f"{bcolors.HEADER}Exiting Application{bcolors.ENDC}") 
        raise SystemExit
    elif ValueError:  
        exception_command()
        screen_clear()
        intro()

def products_menu_text():
    print(f"""{bcolors.OKGREEN}
    **Products Menu** \n
    (0) = Return to Main Menu
    (1) = Print Products list
    (2) = Create New Product
    (3) = Update Product
    (4) = Delete Product
    {bcolors.ENDC}""")

#Product Menu Text
def products_menu_function():
    print_divider()
    products_menu_text()
    print_divider()

    choice2 = input("Enter Option: \n")
    choice2 = int(choice2)
    if choice2 == 0:
        intro()
    elif choice2 == 1:
        print_divider()
        print_products_table()
        products_menu_function()
    elif choice2 == 2:
        create_new_product()
    elif choice2 == 3:
        update_product()
    elif choice2 == 4:
        delete_product()
    elif ValueError:
        exception_command()
        screen_clear()
        products_menu_function()

def courier_menu_text():
    print (f"""{bcolors.OKGREEN}
    **Courier Menu** \n
    (0) = Return to Main Menu
    (1) = Print Couriers list
    (2) = Create New Courier
    (3) = Update Courier
    (4) = Delete Courier
    {bcolors.ENDC}""")

#Courier Menu Text
def courier_menu_function():
    print_divider()
    courier_menu_text()
    print_divider()

    choice_courier_1 = input("Enter Option: \n")
    choice_courier_1 = int(choice_courier_1)
    if choice_courier_1 == 0:
        intro()
    elif choice_courier_1 == 1:
        print_divider()
        print_couriers_table()
        courier_menu_function()
    elif choice_courier_1 == 2:
        create_new_courier()
    elif choice_courier_1 == 3:
        update_courier()
    elif choice_courier_1 == 4:
        delete_courier()
    elif ValueError:
        exception_command()
        screen_clear()
        courier_menu_function()

def order_menu_text():
    print (f"""{bcolors.OKGREEN}
    **Orders Menu** \n
    (0) = Return to Main Menu
    (1) = Print Orders list
    (2) = Create New Order
    (3) = Update Order Status
    (4) = Update Order
    (5) = Delete Order
    {bcolors.ENDC}""")

#Order Menu Text
def order_menu_function():
    print_divider()
    order_menu_text()
    print_divider()

    choice_order_1 = input("Enter Option: \n")
    choice_order_1 = int(choice_order_1)
    if choice_order_1 == 0:
        intro()
    elif choice_order_1 == 1:
        print_divider()
        print_orders_table()
        order_menu_function()
    elif choice_order_1 == 2:
        create_new_order()
    elif choice_order_1 == 3:
        update_order_status()
    elif choice_order_1 == 4:
        update_order()
    elif choice_order_1 == 5:
        delete_order()
    elif ValueError:
        exception_command()
        screen_clear()
        order_menu_function()

############# Products Code ###############
#Print All Products
def print_products_table():
    with connection.cursor() as cursor:
        cursor.execute('SELECT product_id, product_name, product_price FROM products')  
        # Gets all rows from the result
        rows = cursor.fetchall()
        for row in rows:
            print(f'Index: {str(row[0])}, Product Name: {str(row[1])}, Product Price: {row[2]}')  
        cursor.close()

def create_new_product_menu():
    print (f"""{bcolors.OKGREEN}
        **Create New Product** \n
        Please enter NAME of the product you would like to add. \n
        {bcolors.ENDC}""")

#Create new product
def create_new_product():
    with connection.cursor() as cursor:
        print_divider()
        create_new_product_menu()
        print_divider()

        name_input = input("Enter Product Name: ")
        price_input = float(input("Enter Product Price: "))
        sql = "INSERT INTO products (product_name, product_price) VALUES (%s, %s)"
        val = (name_input, price_input)
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        cache_products()
        products_menu_function()

def update_product_menu():
    print (f"""{bcolors.OKGREEN}
        **Update Product** \n
        Please enter Index of the product you would like to update or 0 to CANCEL. \n
        {bcolors.ENDC}""")
#Update product
def update_product():
    with connection.cursor() as cursor:
        print_divider()
        update_product_menu()
        print_divider()
        print_products_table()
        print_divider()

        idx_input = int(input("Please Enter the ID of the Product you want to Update: "))
        if idx_input == 0:
            pass
        else:
            name_input = input("Please Enter New Product Name: ")
            if name_input != "": 
                sql = "UPDATE products SET product_name = %s WHERE product_id = %s"
                val = (name_input, idx_input)
                cursor.execute(sql, val)
                connection.commit()
            else:
                pass
            
            price_input = input("Please Enter New Product Price: ")
            if price_input != "":
                sql = "UPDATE products SET product_price = %s WHERE product_id = %s"
                val = (price_input, idx_input)
                cursor.execute(sql, val)
                connection.commit()
            else:
                pass
        cursor.close()
        cache_products()
        products_menu_function()

def delete_product_menu():
    print(f"""{bcolors.OKGREEN}
        **Delete Product** \n
        Please Select the product you would like to delete. \n
        {bcolors.ENDC}""")

#Delete chosen item from list
def delete_product():
    with connection.cursor() as cursor:
        print_divider()
        delete_product_menu()
        print_divider()
        print_products_table()
        print_divider()

        idx_input = int(input("Please Enter the ID of the Product you want to DELETE: "))
        if idx_input == 0:
            pass
        else:
            sql = "DELETE FROM products WHERE product_id = %s"
            val = (idx_input)
            cursor.execute(sql, val)
            connection.commit()
        cursor.close()
        cache_products()
        products_menu_function()

############# Couriers Code ###############
#Print Couriers List
def print_couriers_table():
    with connection.cursor() as cursor:
        cursor.execute('SELECT courier_id, courier_name, courier_phone FROM couriers')
        # Gets all rows from the result
        rows = cursor.fetchall()
        for row in rows:
            print(f'Index: {str(row[0])}, Courier Name: {str(row[1])}, Courier Phone Number: {row[2]}')
        cursor.close()

def create_new_courier_menu():
    print(f"""{bcolors.OKGREEN}
        **Create New Courier** \n
        Please enter NAME of the courier you would like to add. \n
        {bcolors.ENDC}""")

#Create new COURIER
def create_new_courier():
    with connection.cursor() as cursor:
        print_divider()
        create_new_courier_menu()
        print_divider() 

        name_input = input("Enter Courier Name: ")
        phone_input = input("Enter Courier Phone Number: ")
        sql = "INSERT INTO couriers (courier_name, courier_phone) VALUES (%s, %s)"
        val = (name_input, phone_input)
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        cache_couriers()
        courier_menu_function()
    
def update_courier_menu():
    print (f"""{bcolors.OKGREEN}
        **Update Courier** \n
        Please enter NAME of the courier you would like to update. \n
        {bcolors.ENDC}""")

#Update COURIER
def update_courier():
    with connection.cursor() as cursor:
        print_divider()
        update_courier_menu()
        print_divider()
        print_couriers_table()
        print_divider()

        idx_input = int(input("Please Enter the ID of the Courier you want to Update: "))
        if idx_input == 0:
            pass
        else:
            name_input = input("Please Enter New Courier Name: ")
            if name_input != "":
                sql = "UPDATE couriers SET courier_name = %s WHERE courier_id = %s"
                val = (name_input, idx_input)
                cursor.execute(sql, val)
                connection.commit()
            else:
                pass
    
            phone_input = input("Please Enter New Courier Phone Number: ")
            if phone_input != "":
                sql = "UPDATE couriers SET courier_phone = %s WHERE courier_id = %s"
                val = (phone_input, idx_input)
                cursor.execute(sql, val)
                connection.commit()
            else:
                pass
        cursor.close()
        cache_couriers()
        courier_menu_function()

def delete_courier_menu():
    print (f"""{bcolors.OKGREEN}
        **Delete Courier** \n
        Please Select the courier you would like to delete. \n
        {bcolors.ENDC}""")

#Delete COURIER from list
def delete_courier():
    with connection.cursor() as cursor:
        print_divider()
        delete_courier_menu()
        print_divider()
        print_couriers_table()
        print_divider()

        idx_input = int(input("Please Enter the ID of the Courier you want to DELETE: "))
        if idx_input == 0:
            pass
        else:
            sql = "DELETE FROM couriers WHERE courier_id = %s"
            val = (idx_input)
            cursor.execute(sql, val)
            connection.commit()
            cursor.close()
        cache_couriers()
        courier_menu_function()

############# Order Code ###############
#Print Orders Table
def print_orders_table():
    with connection.cursor() as cursor:
        cursor.execute('SELECT customer_id, customer_name, customer_address, customer_phone, courier_id, status_id, items_id FROM orders')
        # Gets all rows from the result
        rows = cursor.fetchall()
        for row in rows:
            print(f'Index: {str(row[0])}, Courier Name: {str(row[1])}, Customer Address: {row[2]}, Customer Phone Number: {row[3]}, courier ID: {row[4]}, Status: {row[5]}, Ordered Items: {row[6]}')
        cursor.close()

def adding_product_function():
    product_items_list.clear()
    while True:
        try:  
            items_input = int(input("Enter Product(s) index to add to this order, when finished enter 0: "))
            if items_input == 0:
                print("\nYou have stopped adding products")
                break
            product_items_list.append(items_input)
        except ValueError:
            print("\nInvalid Input (please enter a number)\n")
            continue    
    print(("Products chosen {}").format(product_items_list))
    return str(product_items_list)

def updating_product_function():
    product_items_list.clear()
    while True: 
        try:
            items_input = int(input("Enter Product(s) index to add to this order, when finished enter 0: "))
            # cached_products_items_list = product_items_list.copy(items_input)
            if items_input == 0:
                print("\nYou have stopped adding products\n")
                break
            product_items_list.append(items_input)
        except ValueError:
            print("\nLeft Blank, Skipping\n")
            break 
    print(("Products chosen {}\n").format(product_items_list))
    print_divider()
    return str(product_items_list) 

def get_order_status():
    while True:
        try:
            print(f"{bcolors.BOLD}\nOrder Statuses\n{bcolors.ENDC}")
            order_status = ["Preparing", "Quality Control", "Ready", "Collected", "Delivering", "Delivered"]

            for index, status in enumerate(order_status, start = 1):
                print(f'{index}: {status}')

            updated_status_input = int(input("\nChoose new order status from options: "))
            if updated_status_input < 1 or updated_status_input > len(order_status):
                print(f"{bcolors.FAIL}\nInvalid status option chosen, Please try again! \n{bcolors.ENDC}")
                continue
            else:
                break
        except ValueError:
            exception_command()

    if updated_status_input == 1:
        chosen_status = order_status[0]
    elif updated_status_input == 2:
        chosen_status = order_status[1]
    elif updated_status_input == 3:
        chosen_status = order_status[2]
    elif updated_status_input == 4:
        chosen_status = order_status[3]
    elif updated_status_input == 5:
        chosen_status = order_status[4]
    elif updated_status_input == 6:
        chosen_status = order_status[5]
    return chosen_status

def create_new_order_menu():
    print (f"""{bcolors.OKGREEN}
        **Create New Order** \n
        Please enter NEW ORDER information. \n
        {bcolors.ENDC}""")

#Create new order
def create_new_order():
    with connection.cursor() as cursor:
        print_divider()
        create_new_order_menu()
        print_divider()

        name_input = input("Enter Customer Name: ")
        address_input = input("Enter Customer Address: ")
        phone_input = input("Enter Customer Phone Number: ")
        print_divider()
        print(f"{bcolors.BOLD}\nCOURIERS\n{bcolors.ENDC}")
        print_couriers_table()
        print_divider()
        courier_id_input = input("Enter Courier ID: ")
        order_status_input = "Preparing"
        print_divider()
        print(f"{bcolors.BOLD}\nPRODUCTS\n{bcolors.ENDC}")
        print_products_table()
        print_divider()

        adding_product = adding_product_function()
        sql = "INSERT INTO orders (customer_name, customer_address, customer_phone, courier_id, status_id, items_id) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (name_input, address_input, phone_input, courier_id_input, order_status_input, adding_product)
        cursor.execute(sql, val)
        connection.commit()
        cache_orders()
        cursor.close()
        order_menu_function()

def update_order_menu():
    print (f"""{bcolors.OKGREEN}
        **Update Order** \n
        Please enter Update Order information. \n
        {bcolors.ENDC}""")

def idx_chosen():
    print_divider()
    idx_chosen_input = int(input("Please Enter the ID of the Order you want to Update: "))
    return idx_chosen_input

def customer_name_update_order(idx_chosen_input):
    name_input = input("\nEnter Customer Name: ")
    if name_input != "":
        sql = "UPDATE orders SET customer_name = %s WHERE customer_id = %s"
        val = (name_input, idx_chosen_input)
        cursor.execute(sql, val)
        connection.commit()
    else: 
        pass
    return name_input

def customer_address_update_order(idx_chosen_input):
    address_input = input("\nEnter Customer Address: ")
    if address_input != "":
        sql = "UPDATE orders SET customer_address = %s WHERE customer_id = %s"
        val = (address_input, idx_chosen_input)
        cursor.execute(sql, val)
        connection.commit()
    else: 
        pass
    return address_input

def customer_phone_update_order(idx_chosen_input):
    phone_input = input("\nEnter Customer Phone Number: ")
    if phone_input != "":
        sql = "UPDATE orders SET customer_phone = %s WHERE customer_id = %s"
        val = (phone_input, idx_chosen_input)
        cursor.execute(sql, val)
        connection.commit()
    else: 
        pass
    return phone_input

def customer_courier_update_order(idx_chosen_input):
    print_divider()
    print_couriers_table()
    print_divider()
    courier_id_input = input("\nEnter Courier ID: ")
    if courier_id_input != "":
        sql = "UPDATE orders SET courier_id = %s WHERE customer_id = %s"
        val = (courier_id_input, idx_chosen_input)
        cursor.execute(sql, val)
        connection.commit()
    else: 
        pass
    return courier_id_input

def customer_status_update_order(idx_chosen_input):
    order_status_input = get_order_status()
    print_divider()
    print_products_table()
    print_divider()
    if order_status_input != "":
        sql = "UPDATE orders SET status_id = %s WHERE customer_id = %s"
        val = (order_status_input, idx_chosen_input)
        cursor.execute(sql, val)
        connection.commit()
    else: 
        pass
    return order_status_input

def customer_items_update_order(idx_chosen_input):
    adding_product = updating_product_function()
    sql = "UPDATE orders SET items_id = %s WHERE customer_id = %s"
    val = (adding_product, idx_chosen_input)
    cursor.execute(sql, val)
    connection.commit()
    return adding_product
    
def update_order_status_menu():
    print(f"""{bcolors.OKGREEN}
        **Update Order Status** \n
        Please enter Update Order Status information. \n
        {bcolors.ENDC}""")


def update_order_status():
    with connection.cursor() as cursor:
        print_divider()
        update_order_status_menu()
        print_divider()
        print_orders_table()
        print_divider()

        idx_input = int(input("Please Enter the ID of the Order Status you want to Update: "))
        print_divider()
        if idx_input == 0:
            pass
        else:
            order_status_input = get_order_status()
            sql = "UPDATE orders SET status_id = %s WHERE customer_id = %s"
            val = (order_status_input, idx_input)
            cursor.execute(sql, val)
            connection.commit()
            cursor.close()
        cache_orders()
        order_menu_function()

def update_order():
    with connection.cursor() as cursor:
        print_divider()
        update_order_menu()
        print_divider()
        print("Please select Order to Update \n")
        print_orders_table()

        idx_chosen_input = idx_chosen()
        if idx_chosen_input == 0:
            pass
        else:
            name_input = customer_name_update_order(idx_chosen_input)
            address_input = customer_address_update_order(idx_chosen_input)
            phone_input = customer_phone_update_order(idx_chosen_input)
            courier_id_input = customer_courier_update_order(idx_chosen_input)
            order_status_input = customer_status_update_order(idx_chosen_input)
            adding_product = customer_items_update_order(idx_chosen_input)
        cursor.close()
        cache_orders()
        order_menu_function()

def delete_order_menu():
    print (f"""{bcolors.OKGREEN}
        **Delete Order** \n
        Please enter Delete Order information. \n
        {bcolors.ENDC}""")
        
def delete_order():
    with connection.cursor() as cursor:
        print_divider()
        delete_order_menu
        print_divider()
        print_orders_table()
        print_divider()

        idx_input = int(input("Please Enter the ID of the Order you want to Delete: "))
        if idx_input == 0:
            pass
        else:
            sql = "DELETE FROM orders WHERE customer_id = %s"
            val = (idx_input)
            cursor.execute(sql, val)
            connection.commit()
            cursor.close()
        cache_orders()
        order_menu_function()

if __name__ == "__main__":
    print(f"{bcolors.HEADER}IN MAIN{bcolors.ENDC}")
    refresh_caches()
    welcome_message()
    intro()