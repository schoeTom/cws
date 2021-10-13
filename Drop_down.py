import tkinter as tk
from tkinter import *

OptionList = [
"Water",
"Sanitation",
"Hygiene",

]

app = tk.Tk()

app.geometry('100x200')

variable = tk.StringVar(app)
variable.set(OptionList[0])

opt = tk.OptionMenu(app, variable, *OptionList)
opt.config(width=90, font=('Arial', 12))
opt.pack()

app.mainloop()

def show_gui():
    print("Hi, I'm useless. Im just here to show that this function is callable")


