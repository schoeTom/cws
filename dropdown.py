from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Water/Sanitation/Hygiene')
root.iconbitmap('427112.png')
root.geometry("500x400")

# Creating the first list of Variables
Variable1 ="variables_sanitation"

# Create second list of Variables
Variable2 ="variables_sanitation"

def pick_variable(e):
	if my_combo.get() == "Country":
		Variable1_combo.config(value="Country")
		Variable1_combo.current(0)


# Create a drop box
my_combo = ttk.Combobox(root, value=Variable1)
my_combo.current(0)
my_combo.pack(pady=20)
# bind the combobox
my_combo.bind("<<ComboboxSelected>>", pick_variable)

#  Combo box
Variable1_combo = ttk.Combobox(root, value=[" "])
Variable1_combo.current(0)
Variable1_combo.pack(pady=20)

# Frame
my_frame = Frame(root)
my_frame.pack(pady=50)

# List boxes
my_list1 = Listbox(my_frame)
my_list2 = Listbox(my_frame)
my_list1.grid(row=0, column=0)
my_list2.grid(row=0, column=1, padx=20)

def list_Variable1(e):
	my_list2.delete(0, END)
	if my_list1.get(ANCHOR) == "Country":
		for item in Variable1:
			my_list2.insert(END, item)

# add items to list1
for item in Variable1:
	my_list1.insert(END, item)

# Bind The Listbox
my_list1.bind("<<ListboxSelected>>", list_Variable1)

root.mainloop()