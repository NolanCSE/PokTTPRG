from tkinter import *
from tkinter import ttk
import time
import yaml

#Config
ENVIRONMENTS = ["ARCTIC", "BEACH", "CAVE", "DESERT", "FOREST", "FRESHWATER", "GRASSLANDS", "MARSH", "MOUNTAIN", "OCEAN", "RAINFOREST", "TAIGA", "TUNDRA", "URBAN"]
LEVEL_BOUNDARY = [0, 100]
EVOLUTION_RANGE = [1, 3]
TYPES = ["NORMAL", "FIRE", "WATER", "ELECTRIC", "GRASS", "ICE", "FIGHTING", "POISON", "GROUND", "FLYING", "PSYCHIC", "BUG", "ROCK", "GHOST", "DARK", "STEEL", "FAIRY", "DRAGON"]

#Data
pokedex = []

#instance vars subject to change
quantity = 1
environments_to_generate = []
acceptable_levels = []
acceptable_evol_stages = []
acceptable_types = []

def create_basic_section(frame : ttk.Frame):
    quantity_label = ttk.Label(frame, text="Quantity")
    quantity_label.pack(padx=5, pady=5)

    quantity_box = ttk.Spinbox(frame, increment=1, to=20)
    quantity_box.pack(padx=5, pady=5)
    pass

def create_form():
    global LEVEL_BOUNDARY, ENVIRONMENTS, EVOLUTION_RANGE, TYPES, pokedex, quantity
    window = Tk(className=" Random Pokemon Generator", height=500, width=500)
    frame = ttk.Frame(window)
    frame.grid(row=0, column=0)
    create_basic_section(frame=frame)

    window.mainloop()

def load_pokedex():
    global pokedex
    with open("pokedex_rpg.yml", "r") as poke_file:
        pokedex = yaml.safe_load(poke_file)


def main():
    global pokedex
    load_pokedex()
    print(pokedex)
    create_form()

if __name__ == "__main__":
    main()

