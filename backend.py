import tkinter.messagebox


def get_credentials():
    credentials = []
    with open('admin_credentials.txt') as f:
        for line in f:
            username, password = line.split(',')
            credentials.append((username, password.strip()))
    return credentials


def create_product_list(product):
    product_list = []
    with open('products.txt') as f:
        for line in f:
            line = line.split(',')
            product_list.append(product(line[0], line[1], line[2].strip()))
    return product_list


# depending on where it's called (admin or customer), this function receive a different number of arguments
# it updates the products.txt
def update_products(*args):
    if args[0] == 'Add':
        if args[1] != '' and args[3] != '' and args[4] != '':
            with open('products.txt', 'a') as f:
                f.write('\n' + f'{args[1]}, {float(args[3])}, {float(args[4])}')
        else:
            tkinter.messagebox.showerror(title="Error", message='Invalid input')
    elif args[2]:
        updated_product = args[2].split(',')  # args[2] here is the listbox selection to be modified as admin

        if args[0] == 'price':  # arg[0] is the 'price' or the 'quantity' in admin frame
            try:
                updated_product[2] = float(args[1])  # arg[1] is the value from the entry to be used
            except ValueError:
                tkinter.messagebox.showerror(title="Error", message='Invalid input')

        elif args[0] == 'quantity':
            try:
                updated_product[1] = float(args[1])
            except ValueError:
                tkinter.messagebox.showerror(title="Error", message='Invalid input')
        elif args[0] == 'Buy':  # arg[0] is 'Buy' is the customer frame
            try:
                updated_product[1] = float(updated_product[1])
                if updated_product[1] >= float(args[1]):
                    updated_product[1] -= float(args[1])
                elif updated_product[1] > 0:
                    tkinter.messagebox.showerror(title="Error", message="Please insert a value less the quantity")
                else:
                    tkinter.messagebox.showerror(title="Error", message="Product unavailable")
            except ValueError:
                tkinter.messagebox.showerror(title="Error", message='Invalid input')

        product_string = updated_product[0] + ', ' + str(updated_product[1]) + ', ' + str(updated_product[2])

        with open('products.txt', 'r') as f:
            product_list = []
            for line in f:
                product_list.append(line)
            for index, item in enumerate(product_list):
                if updated_product[0] in item:
                    product_list[index] = product_string + '\n'
        with open('products.txt', 'w') as f:
            for item in product_list:
                f.write(item)


def delete_product(item):
    with open('products.txt', 'r') as f:
        product_list = []
        for line in f:
            product_list.append(line)
    if item in product_list:
        product_list.remove(item)
    product_list[-1] = product_list[-1].strip('\n')
    with open('products.txt', 'w') as f:
        for elem in product_list:
            f.write(elem)
