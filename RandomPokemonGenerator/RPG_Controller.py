from RPG_InputForm import *

#instance vars subject to change
quantity = 1
environments_to_generate = []
acceptable_levels = []
acceptable_evol_stages = []

def updateQuantity(q : int):
    global quantity
    print("Updating Quantity: {}".format(q))
    quantity = q
    pass