from peewee import *
import datetime

db = SqliteDatabase('inventory.db')

class Product(Model):
    product_id = PrimaryKeyField()
    product_name = TextField()
    prodcut_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField()

    class Meta:
        database = db

def read():
    with open('inventory.csv', 'r') as file:
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
                print(new_list)
            else:
                new_line = line.split(",")
                print(new_line)

if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True) # safe=True means or at least should be that, it doesnt allow for multiple Product tables to be created
    read()