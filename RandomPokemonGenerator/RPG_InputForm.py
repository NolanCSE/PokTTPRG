from tkinter import *
from tkinter import ttk
import time
import yaml

class InputForm():
    __pokedex = []
    __environments = ["ARCTIC", "BEACH", "CAVE", "DESERT", "FOREST", "FRESHWATER", "GRASSLANDS", "MARSH", "MOUNTAIN", "OCEAN", "RAINFOREST", "TAIGA", "TUNDRA", "URBAN"]
    __levelBoundary = [0, 100]
    __evolRange = [1, 3]
    __types = ["NORMAL", "FIRE", "WATER", "ELECTRIC", "GRASS", "ICE", "FIGHTING", "POISON", "GROUND", "FLYING", "PSYCHIC", "BUG", "ROCK", "GHOST", "DARK", "STEEL", "FAIRY", "DRAGON"]
    __quantity = 1

    def __init__(self):
        self.open()

    def open(self):
        #window = Tk()
        self.openLoader()

        #Build form        
        self.buildBasicSection()
        #window.mainloop()

    def buildBasicSection(self):
        pass

    def helper(self, window : Tk):
        print("before")
        window.after(5000, self.closeWindow(window))
        print("here")


    def openLoader(self):
        loader = Tk()
        progress = ttk.Progressbar(loader, orient=HORIZONTAL, length=300, mode='indeterminate')
        progress.pack(pady=20)
        progress.start(10)

        self.helper(progress)
        loader.mainloop()

    def closeWindow(self, window : Tk):
        window.destroy()
        window.quit()



def main():
    form = InputForm()
    pass
if __name__ == "__main__":
    main()