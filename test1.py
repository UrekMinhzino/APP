import tkinter as tk
from tkinter import ttk

def delete_comrades(tree):
    # Get the selected row and delete it
    selected_item = tree.selection()
    tree.delete(selected_item)
    save_data_to_file(tree)  # Pass the 'tree' widget as a parameter

def add_comrades(tree):
    name = name_entry.get()
    age = age_entry.get()
    rank = rank_entry.get()
    squad = squad_entry.get()
    position = position_entry.get()
    status = status_entry.get()
    tree.insert("", "end", values=(name, age, rank,squad,position,status))
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    rank_entry.delete(0, tk.END)
    squad_entry.delete(0, tk.END)
    position_entry.delete(0 , tk.END)
    status_entry.delete(0 , tk.END)
    save_data_to_file(tree)  # Pass the 'tree' widget as a parameter

def save_data_to_file(tree):
    with open("comrades_data.txt", "w") as f:
        for comrade in tree.get_children():
            comrade_data = tree.item(comrade)["values"]
            f.write(",".join(str(x) for x in comrade_data) + "\n")

window = tk.Tk()
window.title("Comrades Management System")
notebook = ttk.Notebook(window)
notebook.pack(fill="both", expand=True)

# Create a frame for displaying the list of comrades
list_frame = ttk.Frame(notebook)
notebook.add(list_frame, text="List")

# Create a frame for adding new comrades
add_frame = ttk.Frame(notebook)
notebook.add(add_frame, text="Add")

# Create a Treeview widget to display the list of comrades
columns = ("name", "age", "rank","squad","position","status")
tree = ttk.Treeview(list_frame, columns=columns, show="headings")
tree.heading("name", text="Name")
tree.heading("age", text="Age")
tree.heading("rank", text="Rank")
tree.heading("squad",text="Squad")
tree.heading("position",text="Position")
tree.heading("status",text="Status")
tree.pack(fill="both", expand=True)

# This is sample data into the Treeview
comrades = [("Dung", 30, "Lieutenant","Alpha","Commander","Active"), 
            ("Huy", 23, "Corporal","Bravo","Soldier","Active"), 
            ("Trung", 21, "Corporal","Delta","Soldier","Active")]
for comrade in comrades:
    tree.insert("", "end", values=comrade)

# Create a Delete button to delete the selected row
delete_button = ttk.Button(list_frame, text="Delete", command=lambda: delete_comrades(tree))
delete_button.pack()

# Create Entry widgets for entering the comrades's name, age, and rank,position , status
name_entry = ttk.Entry(add_frame)
age_entry = ttk.Entry(add_frame)
rank_entry = ttk.Entry(add_frame)
squad_entry =ttk.Entry(add_frame)
position_entry=ttk.Entry(add_frame)
status_entry = ttk.Entry(add_frame)
name_entry.pack()
age_entry.pack()
rank_entry.pack()
squad_entry.pack()
position_entry.pack()
status_entry.pack()

# Create a Button widget for adding the new comrades
add_button = ttk.Button(add_frame, text="Add", command=lambda: add_comrades(tree))
add_button.pack()

window.mainloop()
