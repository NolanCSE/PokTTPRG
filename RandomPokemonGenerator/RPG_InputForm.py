from tkinter import *
from tkinter import ttk
import time
import yaml
import tkinter as tk
from tkinter.font import Font
import RPG_Controller

#UI Config
DEFAULT_TEXT_PADDING = ("5", "5")

#Data Config
ENVIRONMENTS = ["ARCTIC", "BEACH", "CAVE", "DESERT", "FOREST", "FRESHWATER", "GRASSLANDS", "MARSH", "MOUNTAIN", "OCEAN", "RAINFOREST", "TAIGA", "TUNDRA", "URBAN"]
LEVEL_BOUNDARY = [0, 100]
EVOLUTION_RANGE = [1, 3]
TYPES = ["NORMAL", "FIRE", "WATER", "ELECTRIC", "GRASS", "ICE", "FIGHTING", "POISON", "GROUND", "FLYING", "PSYCHIC", "BUG", "ROCK", "GHOST", "DARK", "STEEL", "FAIRY", "DRAGON"]

#Fonts
DEFAULT_FONT_FAMILY = "HELVETICA"

#Data
pokedex = []

class PokeForm(tk.Tk):

    __stages: list[tk.BooleanVar]

    def __init__(self):
        super().__init__()
        self.title('Random Pokemon Generator')
        self.geometry("500x500")
        self.create_form()

    #Basic Info Frame
    def from_field_valid(self, from_: int, to: int, spinbox: ttk.Spinbox):
        if from_ > to:
            spinbox.set(to)
    def to_field_valid(self, from_: int, to: int, spinbox: ttk.Spinbox):
        if to < from_:
            spinbox.set(from_)

    def create_level_field(self, frame : ttk.Frame):
        global DEFAULT_TEXT_PADDING, DEFAULT_FONT_FAMILY
        level_font = Font(family=DEFAULT_FONT_FAMILY, size=10, weight="bold")
        from_to_font = Font(family=DEFAULT_FONT_FAMILY, size=10)
        level_label = ttk.Label(frame, text="Level:", padding=DEFAULT_TEXT_PADDING, font=level_font)
        from_label = ttk.Label(frame, text="From", padding=DEFAULT_TEXT_PADDING, font=from_to_font)
        to_label = ttk.Label(frame, text="To", padding=DEFAULT_TEXT_PADDING, font=from_to_font)

        from_entry = ttk.Spinbox(frame, increment=1, from_=1, to=100, justify='center',wrap=True)
        from_entry.set(1)
        
        to_entry = ttk.Spinbox(frame, increment=1, from_=1, to=100, justify='center',wrap=True)
        to_entry.set(100)

        from_entry.configure(command=lambda: self.from_field_valid(from_entry.get(), to_entry.get(), from_entry))
        to_entry.configure(command=lambda:self.to_field_valid(from_entry.get(), to_entry.get(), to_entry))

        level_label.grid(row=0, column=0)
        from_label.grid(row=0, column=1)
        from_entry.grid(row=0, column=2)
        to_label.grid(row=0, column=3)
        to_entry.grid(row=0, column=4)

        from_entry.config(width=5)
        to_entry.config(width=5)

        pass

    def create_stage_field(self, frame : ttk.Frame):
        global DEFAULT_FONT_FAMILY, DEFAULT_TEXT_PADDING
        #import pdb; pdb.set_trace()
        self.__stages = [tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()]

        stage_font = Font(family=DEFAULT_FONT_FAMILY, size=10, weight="bold")
        stage_I_label = ttk.Label(frame, text="Stage I", padding=DEFAULT_TEXT_PADDING, font=stage_font)
        stage_II_label = ttk.Label(frame, text="Stage II", padding=DEFAULT_TEXT_PADDING, font=stage_font)
        stage_III_label = ttk.Label(frame, text="Stage III", padding=DEFAULT_TEXT_PADDING, font=stage_font)

        sI_checkbox = tk.Checkbutton(frame, variable=self.__stages[0], onvalue=True, offvalue=False)
        sII_checkbox=tk.Checkbutton(frame, variable=self.__stages[1], onvalue=True, offvalue=False)
        sIII_checkbox=tk.Checkbutton(frame, variable=self.__stages[2], onvalue=True, offvalue=False)

        stage_I_label.grid(row=0, column=0)
        sI_checkbox.grid(row=0, column=1)
        stage_II_label.grid(row=0, column=2)
        sII_checkbox.grid(row=0, column=3)
        stage_III_label.grid(row=0, column=4)
        sIII_checkbox.grid(row=0, column=5)

        for i in range(len(self.__stages)):
            self.__stages[i] = False
        pass

    #Environment Frame
    def create_environment_field(self, frame : ttk.Frame):
        global ENVIRONMENTS
        self.__buttonVars = []
        self.__buttons = []
        self.__buttonLabels = []
        #import pdb; pdb.set_trace()
        per_column = int(len(ENVIRONMENTS) / 2)
        column_counter = 0
        row_counter = 0
        for index in range(len(ENVIRONMENTS)):
            self.__buttonVars.append(tk.BooleanVar())
            self.__buttons.append(ttk.Checkbutton(frame, variable=self.__buttonVars[-1], onvalue=True, offvalue=False))
            self.__buttons[-1].grid(row=row_counter, column = column_counter)
            row_counter += 1
            if (index + 1) % per_column == 0:
                column_counter += 1
                row_counter = 0
        pass

    #Quantity Frame
    def create_quantity_field(self, frame : ttk.Labelframe):
        global DEFAULT_PADDING

        quantity_label = ttk.Label(frame, text="Quantity", padding=DEFAULT_TEXT_PADDING, font=Font(family=DEFAULT_FONT_FAMILY, size=16, weight='bold'))
        quantity_label.grid(row=0, column=0)

        
        quantity_box = ttk.Spinbox(frame, increment=1, from_=1, to=20, justify='center', wrap=True, state="readonly", command=lambda: RPG_Controller.updateQuantity(quantity_box.get()))
        quantity_box.config(width=2)
        quantity_box.config(font=Font(family=DEFAULT_FONT_FAMILY, size=26, weight='bold'))
        print(quantity_box.winfo_geometry())
        quantity_box.set(1)

        quantity_box.grid(row=1, column=0)


    def create_basic_section(self, frame : ttk.Labelframe):
        #import pdb; pdb.set_trace()
        level_frame = ttk.Frame(frame)
        level_frame.grid(row=0, column=0)
        self.create_level_field(level_frame)

        stage_frame = ttk.Frame(frame)
        stage_frame.grid(row=1, column=0)
        self.create_stage_field(stage_frame)
        pass

    def create_environment_section(self, frame : ttk.Labelframe):
        environ_frame = ttk.Frame(frame)
        environ_frame.grid(row=0, column=0)
        self.create_environment_field(environ_frame)
        pass

    def create_types_section(self, frame: ttk.Labelframe):
        pass

    def create_quantity_section(self, frame: ttk.Labelframe):
        self.create_quantity_field(frame)
        pass

    def create_generate_section(self, frame: ttk.Labelframe):
        pass

    def create_form(self):
        global LEVEL_BOUNDARY, ENVIRONMENTS, EVOLUTION_RANGE, TYPES, pokedex, quantity

        basic_frame = ttk.Labelframe(self, text="Basic Information")
        basic_frame.grid(row=0, column=1)
        self.create_basic_section(frame=basic_frame)

        environment_frame = ttk.Labelframe(self, text="Environments")
        environment_frame.grid(row=0, column=0)
        self.create_environment_section(frame=environment_frame)
        
        types_frame = ttk.Labelframe(self, text="Types")
        types_frame.grid(row=1, column=1)
        self.create_types_section(frame=types_frame)

        quantity_frame = ttk.Labelframe(self, text="")
        quantity_frame.grid(row=2, column=0)
        self.create_quantity_section(frame=quantity_frame)

        generate_frame = ttk.Labelframe(self, text="")
        generate_frame.grid(row=2, column=1)
        self.create_generate_section(frame=generate_frame)

def load_pokedex():
    global pokedex
    with open("pokedex_rpg.yml", "r") as poke_file:
        pokedex = yaml.safe_load(poke_file)


def main():
    global pokedex
    #load_pokedex()
    #print(pokedex)
    formApp = PokeForm()
    formApp.mainloop()

if __name__ == "__main__":
    main()

