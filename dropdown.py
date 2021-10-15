from tkinter import *
from tkinter import ttk
import tkinter as tk

root = Tk()
root.title('Water/Sanitation/Hygiene')
#root.iconbitmap(tk.PhotoImage(file='427112.png'))
root.iconphoto(False, tk.PhotoImage(file="427112.png"))
root.geometry("500x400")


def load_variables(v1, v2, v3, dfSanitation):
	global variables_sanitation
	variables_sanitation = v1
	global variables_water
	variables_water = v2
	global variables_hygiene
	variables_hygiene = v3
	global countries
	countries = dfSanitation.iloc[:, 0].unique().tolist()

	# Creating the first list of Variables
	global Variable1
	Variable1 = []
	for key in variables_hygiene.keys():
		Variable1.append(key)
	#Variable1 = variables_sanitation.keys(), variables_hygiene.keys(), variables_sanitation.keys()
	# Create second list of Variables
	global Variable2
	Variable2 = 'variables_sanitation'

	# Create a drop box
	global my_combo
	my_combo = ttk.Combobox(root, value=Variable1)
	my_combo.current(0)
	my_combo.pack(pady=20)
	# bind the combobox
	my_combo.bind("<<ComboboxSelected>>", pick_variable)
	combo_box()





def pick_variable():
	if my_combo.get() == "Country":
		Variable1_combo.config(value="Country")
		Variable1_combo.current(0)
	list_Variable1()

#insert country selection
	for key in countries.keys():
		var1.append(key)
	master = Tk()
	var1 = IntVar()
	Checkbutton(master, text=countries, variable=var1).grid(row=0, sticky=W)
	mainloop()
	pick_variable()

def combo_box():
	#  Combo box
	global Variable1_combo
	Variable1_combo = ttk.Combobox(root, value=[" "])
	Variable1_combo.current(0)
	Variable1_combo.pack(pady=20)

	# Frame
	my_frame = Frame(root)
	my_frame.pack(pady=50)

	# List boxes
	global my_list1
	global my_list2
	my_list1 = Listbox(my_frame)
	my_list2 = Listbox(my_frame)
	my_list1.grid(row=0, column=0)
	my_list2.grid(row=1, column=0)
	#insert country selection

	#master = Tk()
	#var1 = IntVar()
	#Checkbutton(master, text=countries, variable=var1).grid(row=0, sticky=W)
	#mainloop()
	#pick_variable()

def list_Variable1():
	#my_list2.delete(0, END)
	#if my_list1.get(ANCHOR) == "Country":
	#	for item in Variable1:
	#		my_list2.insert(END, item)
	add_items_to_list1()

def add_items_to_list1():
	# add items to list1
	for item in Variable1:
		my_list1.insert(END, item)
		my_list2.insert(END, item)
		bind_the_listbox()

def bind_the_listbox():
	# Bind The Listbox
	my_list1.bind("<<ListboxSelected>>")
	my_list2.bind("<<ListboxSelected>>")

	root.mainloop()