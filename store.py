import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from backend import *
from product import Product


# authentication frame, which contains the field for the admin credentials
class AuthFrame(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container)
        self['text'] = 'Admin Authentication'
        self['padding'] = 5
        self.grid(row=3, column=0, columnspan=2)

        self.user_label = ttk.Label(self, text='Username', padding=3)
        self.user_label.grid(column=0, row=0, padx=5)
        self.username = tk.StringVar()
        self.username_box = ttk.Entry(self, textvariable=self.username)
        self.username_box.grid(column=1, row=0)

        self.pass_label = ttk.Label(self, text='Password', padding=3)
        self.pass_label.grid(column=0, row=1)
        self.password = tk.StringVar()
        self.password_box = ttk.Entry(self, textvariable=self.password)
        self.password_box.grid(column=1, row=1, pady=5)

        self.cancel_button = ttk.Button(
            self,
            text='Cancel',
            command=self.cancel
        )
        self.cancel_button.grid(row=2, column=0, pady=7, padx=10)

        # next button, which calls 'credentials()' to check the credentials stored in admin_credentials.txt
        self.next_button = ttk.Button(
            self,
            text='Next',
            command=lambda: self.credentials()
        )
        self.next_button.grid(row=2, column=1, pady=7)

    def credentials(self):
        if (self.username_box.get(), self.password_box.get()) not in get_credentials():
            showerror(title='Error', message="Incorrect credentials")
        else:
            mf_admin.show_frame()

    def cancel(self):
        self.destroy()


# menu frame, which can be an admin frame or customer frame, based on the button in the welcome frame
# menu frame is controlled in the main using 'menu_type' as control parameter
class MenuFrame(ttk.Frame):
    def __init__(self, container, menu_type, attributes):
        super().__init__(container)
        self.grid(row=0, column=0, sticky='nsew')
        self.menu_type = menu_type
        self['padding'] = 25
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        self.select_label = ttk.Label(self, text=f"Select a product to: ",
                                      padding=2)
        self.select_label.grid(row=0, column=0, sticky='w')

        self.attributes_label = ttk.Label(self, text=f'Name | Quantity (kg) | Price (RON/Kg)', padding=2)
        self.attributes_label.grid(row=1, column=0, sticky='w')

        # add/buy button, which calls a methods to create an option label frame
        # if in admin frame, the button is 'add'; if in customer, 'buy'
        self.button_add_buy = ttk.Button(self,
                                         text=attributes['option_action_type'],
                                         command=lambda: CreateOptionsLabelFrame(
                                             self,
                                             {'menu_type': attributes['option_menu_type'],
                                              'action_type': attributes['option_action_type']}
                                         ).add_buy_option()
                                         )
        self.button_add_buy.grid(row=2, column=2)

        # modify and delete buttons are for admin frame only
        if self.menu_type == 'admin':
            # modify button
            self.button_modify = ttk.Button(self,
                                            text="Modify",
                                            command=lambda: CreateOptionsLabelFrame(
                                                self,
                                                {'menu_type': attributes['option_menu_type'],
                                                 'action_type': attributes['option_action_type']}
                                            ).modify_option()
                                            )
            self.button_modify.state(['disabled'])
            self.button_modify.grid(row=1, column=2)

            self.button_delete = ttk.Button(self,
                                            text='Delete',
                                            command=lambda: [delete_product(
                                                mf_admin.get_listbox_value()
                                            ), mf_admin.create_listbox(),
                                                mf_customer.create_listbox()
                                            ]
                                            )
            self.button_delete.grid(row=3, column=2)

        # back button
        self.button_back = ttk.Button(self,
                                      text='Back',
                                      command=lambda: wf.show_frame()
                                      )
        self.button_back.grid(row=4, column=2)

        # listbox
        self.create_listbox()

    # function to create the listbox; it's called at the beginning and each time the items in it are modified, added
    # or deleted
    def create_listbox(self):
        self.listbox = tk.Listbox(
            self,
            height=5,
        )
        for index, product in enumerate(create_product_list(Product)):
            self.listbox.insert(index, f'{product.name},{product.quantity}, {product.price_per_kg}')

        if self.menu_type == 'admin':
            self.listbox.bind('<<ListboxSelect>>', self.modify_button_enable)
        self.listbox.grid(row=2, column=0, rowspan=3, sticky='nsew')

        scrollbar = ttk.Scrollbar(
            self,
            orient='vertical',
            command=self.listbox.yview
        )
        self.listbox['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=2, column=1, rowspan=3, sticky='nws')

    # enables the modify button each time an item from listbox is selected
    def modify_button_enable(self, event):
        selection = self.listbox.curselection()
        if selection:
            self.button_modify.state(['!disabled'])

    def get_listbox_value(self):
        try:
            return self.listbox.get(self.listbox.curselection())
        except:
            tkinter.messagebox.showinfo(title="Info", message='Please select a product')

    def show_frame(self):
        self.tkraise()


# class that creates the option frame in admin or customer frames
class CreateOptionsLabelFrame(ttk.LabelFrame):
    def __init__(self, container, option_attributes):
        super().__init__(container)
        self.option_attributes = option_attributes
        self.grid(row=5, column=0, columnspan=3, pady=15)
        self.grid_propagate(False)
        self['padding'] = 10
        self['height'] = 110
        self['width'] = 290
        self.new_value = tk.StringVar()
        self.selected_value = tk.StringVar()

    # called by modify button to create the modify option frame
    def modify_option(self):
        self['text'] = 'Please write the quantity you want to modify'

        # Quantity button
        quantity = ttk.Radiobutton(
            self,
            text='Quantity',
            value='quantity',
            variable=self.selected_value,
            command=lambda: submit_button.state(['!disabled'])
        )
        quantity.grid(column=0, row=0, columnspan=3, sticky='w')

        # Price button
        price = ttk.Radiobutton(
            self,
            text='Price',
            value='price',
            variable=self.selected_value,
            command=lambda: submit_button.state(['!disabled'])
        )
        price.grid(column=0, row=2, columnspan=3, sticky='w')

        new_value_request_label = ttk.Label(self, text='Please input new value: ')
        new_value_request_label.grid(row=3, column=0)

        new_value_box = ttk.Entry(
            self,
            textvariable=self.new_value,
            width=5
        )
        new_value_box.grid(row=3, column=1)

        # SUBMIT BUTTON, calls update_products function which gets the value and modify it in the products.txt
        # also, calls the function to refresh the listbox with the new values
        submit_button = ttk.Button(
            self,
            text='Submit',
            command=lambda: [update_products(
                self.selected_value.get(),
                self.new_value.get(),
                mf_admin.get_listbox_value()
            ), mf_admin.create_listbox(),
                mf_customer.create_listbox(),
                new_value_box.delete(0, 'end')]
        )
        submit_button.state(['disabled'])
        submit_button.grid(row=3, column=2)

    # add/buy function, called by add/buy button depending on the frame (admin or customer)
    # add and buy are using the same button widget, and they are switched based on admin or customer
    def add_buy_option(self):
        self['text'] = self.option_attributes['menu_type']
        new_value = tk.StringVar()
        new_value_box = ttk.Entry(
            self,
            textvariable=new_value,
            width=10
        )
        new_value_box.grid(row=0, column=1, padx=10)
        new_value_name_label = ttk.Label(self, text='Name:')

        new_value_quantity = tk.StringVar()
        new_value_quantity_box = ttk.Entry(
            self,
            textvariable=new_value_quantity,
            width=5
        )
        new_value_quantity_label = ttk.Label(self, text='Quantity:')

        new_value_price = tk.StringVar()
        new_value_price_box = ttk.Entry(
            self,
            textvariable=new_value_price,
            width=5
        )
        new_value_price_label = ttk.Label(self, text='Price:')
        if self.option_attributes['action_type'] == 'Add':
            new_value_name_label.grid(row=0, column=0, padx=10)
            new_value_quantity_label.grid(row=1, column=0, padx=10)
            new_value_quantity_box.grid(row=1, column=1, pady=5)
            new_value_price_label.grid(row=2, column=0, padx=10)
            new_value_price_box.grid(row=2, column=1)

        # add/buy button (option label frame). It calls the update_products function to either add a product
        # as admin, or lower the quantity of a product when a customer buys a product
        # same as modify button, it updates the listbox with the new values
        add_buy_button = ttk.Button(
            self,
            text=self.option_attributes['action_type'],
            command=lambda: [update_products(
                self.option_attributes['action_type'],
                new_value.get(),
                mf_customer.get_listbox_value()
                if self.option_attributes['action_type'] == 'Buy' else None,
                new_value_quantity.get() if self.option_attributes['action_type'] == 'Add' else None,
                new_value_price.get() if self.option_attributes['action_type'] == 'Add' else None,
            ),
                mf_admin.create_listbox(),
                mf_customer.create_listbox(),
                new_value_box.delete(0, 'end'),
                new_value_quantity_box.delete(0, 'end'),
                new_value_price_box.delete(0, 'end')
            ],
        )

        add_buy_button.grid(row=0, column=2, rowspan=3, padx=10)


# main frame
class WelcomeFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self['padding'] = (70, 40)
        self.grid(row=0, column=0, sticky='nsew')
        self.label_welcome = ttk.Label(self, text='Welcome to the store!', font=('Arial', 19), padding=3)
        self.label_welcome.grid(row=0, column=0, columnspan=2)
        self.label_guide = ttk.Label(self, text='Please select one of the options below', font=('Arial', 10), padding=3)
        self.label_guide.grid(row=1, column=0, columnspan=2)

        # admin button, calls the creation of the authentication frame
        self.admin_button = ttk.Button(
            self,
            text='Admin',
            command=lambda: AuthFrame(self)
        )
        self.admin_button.grid(row=2, column=0, pady=10)

        # customer button
        self.customer_button = ttk.Button(
            self,
            text='Customer',
            command=lambda: mf_customer.show_frame()
        )
        self.customer_button.grid(row=2, column=1, pady=10)
        self.customer_button.focus()

    def show_frame(self):
        self.tkraise()


class Store(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Store')
        self.geometry('400x300')
        self.resizable(False, False)


if __name__ == '__main__':
    store = Store()

    # dictionaries that are used for creating the admin or the customer frames
    customer_options = {
        'option_menu_type': 'Please write the quantity you want to buy',
        'option_action_type': 'Buy',
    }
    admin_options = {
        'option_menu_type': 'Please write the item you want to add',
        'option_action_type': 'Add'
    }

    # mf_customer = MenuFrame(store, 'customer', customer_options)
    # mf_admin = MenuFrame(store, 'admin',admin_options)

    def update_frames():
        customer = MenuFrame(store, 'customer', customer_options)
        admin = MenuFrame(store, 'admin', admin_options)
        return customer, admin


    mf_customer, mf_admin = update_frames()
    wf = WelcomeFrame(store)
    store.mainloop()
