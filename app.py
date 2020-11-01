import datetime
import csv

from peewee import *



db = SqliteDatabase('inventory.db')

class Product(Model):
    product_id = AutoField(primary_key=True)
    product_name = TextField()
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField()

    class Meta():
        database = db

def clean_data():
    with open('inventory.csv', 'r') as file:
        items = []
        for line in file:
            if '"' in line:
                """This If statement cleans up the lines that have commas in the product_name section"""
                new_line_1 = line[1:]
                new_line_2 = new_line_1.split('"')
                new_line_3 = new_line_2[1][1:]
                new_line_4 = new_line_3.split(",")
                new_list = []
                new_list.append(new_line_2[0])
                for value in new_line_4:
                    new_list.append(value)
                items.append(new_list)
            else:
                new_line = line.split(",")
                items.append(new_line)
        items.pop(0) # removes the header from the data
        for item in items:
            Product.create(
                product_name=item[0],
                product_price=int(item[1].replace('$', '').replace('.', '')),
                product_quantity=int(item[2]),
                date_updated=item[3].replace('\n', '')
            )

def view_entry(id):
    try:
        max_length = Product.select()
        if int(id) > int(len(max_length)):
            raise ValueError
        elif  id.isdigit() == False:
            raise ValueError
        products = Product.select().where(Product.product_id == id)
        for product in products:
            print("Name: " + product.product_name)
            print("Price: " + str(product.product_price) + " Cents")
            print("Quantity: " + str(product.product_quantity))
            print("Date Updated: " + str(product.date_updated))
            return
    except ValueError:
        print("ID not found, please enter a valid product ID")


def add_entry():
    while True:
        try:
            entry = input("Please Enter Product Name: ")
            names = Product.select().order_by(Product.product_name)
            for name in names:
                if name.product_name.lower() == entry.lower():
                    raise IntegrityError
                    break
                price = input("Please Enter Product Price: ")
                if price.isdigit() == False:
                    print("Price not valid")
                    break
                quantity = input("Please Enter Product Quantity: ")
                if quantity.isdigit() == False:
                    print("Quantity not valid")
                    break
                date = datetime.datetime.now().date().strftime("%m/%d/%Y")
                Product.create(product_name=entry, product_price=price, product_quantity=quantity, date_updated=date)
                return
        except IntegrityError:
            print("\nThat item already exists within the database")
            while True:
                q = input("\nWould you like to update {}, (Y/N)> ".format(entry))
                if q.lower() == 'n':
                    return  # returns to main menu
                elif q.lower() == 'y':
                    """This grabs the data from the database and updates it"""
                    update_entry = Product.get(Product.product_name == entry)
                    price = input("\nPlease Enter Product Price: ")
                    quantity = input("\nPlease Enter Product Quantity: ")
                    date = datetime.datetime.now().date().strftime("%m/%d/%Y")
                    update_entry.product_price = price
                    update_entry.product_quantity = quantity
                    update_entry.date_updated = date
                    update_entry.save()
                    print("\nUpdates Saved Successfully")
                    return
                elif q.lower() != 'y' or 'n':
                    print("Please enter a valid value")
                
    



def backup():
    products = Product.select().order_by(Product.product_id)
    
    with open('backup.csv', 'w') as file:
        fieldnames = ['product_name', 'product_price', 'product_quantity', 'date_updated']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            writer.writerow({
                'product_name': product.product_name,
                'product_price': product.product_price,
                'product_quantity': product.product_quantity,
                'date_updated': product.date_updated
            })
    print("Data Backup Successful")



def display_menu():
    welcome = "Hello There Welcome to the Store Inventory"
    print("\n" + welcome)
    print("="*len(welcome)+"\n")
    while True:
        choice = input("Please Select one of the following menu options\n\nA) Add an Entry\nV) View Entries\nB) Backup The Database\nE) Exit\n\n>")
        if choice == 'a':
            print('\n'+"="*len(welcome))
            add_entry()
            print("="*len(welcome)+'\n')
        elif choice == 'v':
            print('\n'+"="*len(welcome))
            # Add an error catcher
            select = input("Please enter a Product ID > ")
            view_entry(select)
            print("="*len(welcome))
        elif choice == 'b':
            print('\n'+"="*len(welcome))
            backup()
            print("="*len(welcome))
        elif choice == 'e':
            print('\n'+"="*len(welcome))
            print("exiting the application")
            print("="*len(welcome))
            break

if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True) # safe=True means or at least should be that, it doesnt allow for multiple Product tables to be created
    clean_data()
    display_menu()