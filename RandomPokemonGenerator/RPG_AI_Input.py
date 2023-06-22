import tkinter as tk
from tkinter import messagebox

# Create a window
window = tk.Tk()
window.title("Random Pokemon Generator")
window.geometry("400x500")

# Function to generate Pokemon
def generate_pokemon():
    # Get user input values
    quantity = quantity_variable.get()
    min_level = min_level_entry.get()
    max_level = max_level_entry.get()
    min_evolutions = min_evolutions_entry.get()
    max_evolutions = max_evolutions_entry.get()
    selected_types = []
    for type_var, type_value in type_variables.items():
        if type_value.get():
            selected_types.append(type_var)

    # Validate user inputs
    if not quantity:
        messagebox.showerror("Error", "Please select a quantity.")
        return

    if not min_level or not max_level:
        messagebox.showerror("Error", "Please enter level range.")
        return

    if not min_evolutions or not max_evolutions:
        messagebox.showerror("Error", "Please enter evolution range.")
        return

    # Perform the necessary actions to generate Pokemon based on user input
    # ...

    # Display the generated Pokemon or perform any other desired actions
    # ...

# Labels and entry fields
quantity_label = tk.Label(window, text="Quantity:")
quantity_label.pack()
quantity_variable = tk.StringVar(window, value="1")
quantity_spinbox = tk.Spinbox(window, from_=1, to=10, textvariable=quantity_variable)
quantity_spinbox.pack()

level_label = tk.Label(window, text="Level Range:")
level_label.pack()
level_frame = tk.Frame(window)
level_frame.pack()

min_level_label = tk.Label(level_frame, text="Min:")
min_level_label.grid(row=0, column=0)
min_level_entry = tk.Entry(level_frame)
min_level_entry.grid(row=0, column=1)

max_level_label = tk.Label(level_frame, text="Max:")
max_level_label.grid(row=1, column=0)
max_level_entry = tk.Entry(level_frame)
max_level_entry.grid(row=1, column=1)

evolution_label = tk.Label(window, text="Evolution Range:")
evolution_label.pack()
evolution_frame = tk.Frame(window)
evolution_frame.pack()

min_evolutions_label = tk.Label(evolution_frame, text="Min:")
min_evolutions_label.grid(row=0, column=0)
min_evolutions_entry = tk.Entry(evolution_frame)
min_evolutions_entry.grid(row=0, column=1)

max_evolutions_label = tk.Label(evolution_frame, text="Max:")
max_evolutions_label.grid(row=1, column=0)
max_evolutions_entry = tk.Entry(evolution_frame)
max_evolutions_entry.grid(row=1, column=1)

#Button panel frame
button_panel_frame = tk.Frame(window)
button_panel_frame.pack(pady=20)

# Types fields
types_label = tk.Label(button_panel_frame, text="Types:")
types_label.grid(row=3, column=0, padx=5, pady=5)

type_variables = {}
type_options = ["Fire", "Water", "Grass", "Electric", "Rock", "Ground", "Flying"]
for i, option in enumerate(type_options):
    type_var = tk.BooleanVar()
    type_checkbutton = tk.Checkbutton(button_panel_frame, text=option, variable=type_var)
    type_checkbutton.grid(row=3 + i // 2, column=i % 2 + 1, padx=5, pady=2, sticky="w")
    type_variables[option] = type_var

# Generate button
generate_button = tk.Button(window, text="Generate", command=generate_pokemon)
generate_button.pack()

# Run the GUI
window.mainloop()