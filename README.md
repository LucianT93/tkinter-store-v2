# tkinter-market
This is a version 2 of the market store using Tkinter GUI

The main script, `store.py`, uses `backend.py` script to connect to a 
mySql database containing the tables `administrators` and `products`
These tables contains the login information for the admin and the products.

The Tkinter GUI calls the functions in the `backend.py` to make all the CRUD operation needed in the application