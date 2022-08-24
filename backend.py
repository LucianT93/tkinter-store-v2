import tkinter.messagebox
from sqlalchemy.orm import sessionmaker
from model import Base, Admin, Product

from sqlalchemy import create_engine

host = '127.0.0.1'
username = 'root'
password = 'lukasporsche911'
database = 'db_store'

CONNECTION_STRING = f"mysql+pymysql://{username}:{password}@{host}/{database}"

engine = create_engine(CONNECTION_STRING)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_elements():
    session.add_all(
        [
            Admin(
                username='luciant93',
                password='pas1234'
            ),
            Product(
                name='Tomatoes',
                qty=100,
                price=4.5
            ),
            Product(
                name='Cucumbers',
                qty=30,
                price=5
            ),
            Product(
                name='Peppers',
                qty=45,
                price=6
            ),
            Product(
                name='Onions',
                qty=30,
                price=2.5
            ),
        ]
    )
    session.commit()


# add_elements()


def get_credentials():
    credentials_list = []
    credentials = session.query(Admin).all()
    for credential in credentials:
        credentials_list.append((credential.username, credential.password))

    return credentials_list


def create_product_list():
    products = session.query(Product).all()
    return products



# depending on where it's called (admin or customer), this function receive a different number of arguments
# it updates the products.txt
def update_products(*args):
    if args[0] == 'Add':
        if args[1] != '' and args[3] != '' and args[4] != '':
            session.add(Product(
                name={args[1]},
                qty={args[3]},
                price={args[4]}
            ))
        else:
            tkinter.messagebox.showerror(title="Error", message='Invalid input')
    elif args[2]:
        updated_product = args[2].split(',')  # args[2] here is the listbox selection to be modified as admin

        if args[0] == 'price':  # arg[0] is the 'price' or the 'quantity' in admin frame
            try:
                # updated_product[2] = float(args[1])  # arg[1] is the value from the entry to be used
                update_price = session.query(Product).filter(Product.name == updated_product[0]).first()
                update_price.price = float(args[1])
                session.commit()
            except ValueError:
                tkinter.messagebox.showerror(title="Error", message='Invalid input')

        elif args[0] == 'quantity':
            try:
                # updated_product[1] = float(args[1])
                update_qty = session.query(Product).filter(Product.name == updated_product[0]).first()
                update_qty.qty = float(args[1])
                session.commit()
            except ValueError:
                tkinter.messagebox.showerror(title="Error", message='Invalid input')
        elif args[0] == 'Buy':  # arg[0] is 'Buy' is the customer frame
            try:
                update_buy_price = session.query(Product).filter(Product.name == updated_product[0]).first()
                if update_buy_price.qty >= float(args[1]) > 0:
                    update_buy_price.qty -= float(args[1])
                    session.commit()
                elif update_buy_price.qty > 0:
                    tkinter.messagebox.showerror(title="Error", message="Please insert a value less the quantity"
                                                                        "and greater than 0")
                else:
                    tkinter.messagebox.showerror(title="Error", message="Product unavailable")
            except ValueError:
                tkinter.messagebox.showerror(title="Error", message='Invalid input')


def delete_product(item):
    print(type(item))
    session.query(Product).filter(Product.name == item.split(',')[0]).delete()
    session.commit()
