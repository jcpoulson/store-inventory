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
            new_line = line.split('')
            print(new_line)

if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True) # safe=True means or at least should be that, it doesnt allow for multiple Product tables to be created
    read()