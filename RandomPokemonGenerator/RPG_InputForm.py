from tkinter import *
from tkinter import ttk
import time
import yaml
import tkinter as tk
import RPG_Controller

#UI Config
DEFAULT_TEXT_PADDING = ("5", "5")

#Data Config
ENVIRONMENTS = ["ARCTIC", "BEACH", "CAVE", "DESERT", "FOREST", "FRESHWATER", "GRASSLANDS", "MARSH", "MOUNTAIN", "OCEAN", "RAINFOREST", "TAIGA", "TUNDRA", "URBAN"]
LEVEL_BOUNDARY = [0, 100]
EVOLUTION_RANGE = [1, 3]
TYPES = ["NORMAL", "FIRE", "WATER", "ELECTRIC", "GRASS", "ICE", "FIGHTING", "POISON", "GROUND", "FLYING", "PSYCHIC", "BUG", "ROCK", "GHOST", "DARK", "STEEL", "FAIRY", "DRAGON"]

#Data
pokedex = []

def create_quantity_field(frame : ttk.Labelframe):
    global DEFAULT_PADDING

    quantity_label = ttk.Label(frame, text="Quantity", padding=DEFAULT_TEXT_PADDING)
    quantity_label.grid(row=0, column=0)

    
    quantity_box = ttk.Spinbox(frame, increment=1, from_=1, to=20, justify='center', wrap=True, state="readonly", command=lambda: RPG_Controller.updateQuantity(quantity_box.get()))
    quantity_box.config(width=5)
    quantity_box.set(1)

    quantity_box.grid(row=0, column=1)


def create_basic_section(frame : ttk.Labelframe):
    create_quantity_field(frame)
    pass

def create_form():
    global LEVEL_BOUNDARY, ENVIRONMENTS, EVOLUTION_RANGE, TYPES, pokedex, quantity
    window = Tk(className=" Random Pokemon Generator")
    window.geometry("500x500")
    frame = ttk.Labelframe(window, text="Basic Information")
    frame.grid(row=0, column=0)
    create_basic_section(frame=frame)

    window.mainloop()

def load_pokedex():
    global pokedex
    with open("pokedex_rpg.yml", "r") as poke_file:
        pokedex = yaml.safe_load(poke_file)


def main():
    global pokedex
    #load_pokedex()
    #print(pokedex)
    create_form()

if __name__ == "__main__":
    main()

