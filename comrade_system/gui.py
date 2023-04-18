import tkinter as tk
import os
from tkinter import ttk
from management_system import Comrade_Information_Management_System, decompress_data, compress_data


class Comrade_Information_Management_System_GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Comrade Information Management System")
        self.master.geometry("800x600")
        self.management_system = Comrade_Information_Management_System()

        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill="both", expand=True)

        self.list_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.list_frame, text="List")

        self.add_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_frame, text="Add")

        columns = ("name", "age", "rank", "squad", "position", "status")
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show="headings")
        self.tree.heading("name", text="Name")
        self.tree.heading("age", text="Age")
        self.tree.heading("rank", text="Rank")
        self.tree.heading("squad", text="Squad")
        self.tree.heading("position", text="Position")
        self.tree.heading("status", text="Status")
        self.tree.pack(fill="both", expand=True)

        self.refresh_treeview()

        self.delete_button = ttk.Button(self.list_frame, text="Delete", command=self.delete_comrades)
        self.delete_button.pack()

        self.name_entry = ttk.Entry(self.add_frame)
        self.age_entry = ttk.Entry(self.add_frame)
        self.rank_entry = ttk.Entry(self.add_frame)
        self.squad_entry = ttk.Entry(self.add_frame)
        self.position_entry = ttk.Entry(self.add_frame)
        self.status_entry = ttk.Entry(self.add_frame)
        self.name_entry.pack()
        self.age_entry.pack()
        self.rank_entry.pack()
        self.squad_entry.pack()
        self.position_entry.pack()
        self.status_entry.pack()

        self.add_button = ttk.Button(self.add_frame, text="Add", command=self.add_comrades)
        self.add_button.pack()

    def delete_comrades(self):
        selected_item = self.tree.selection()
        selected_comrade = self.tree.item(selected_item)['values'][0]
        self.management_system.delete_comrade(selected_comrade)
        self.refresh_treeview()
        self.save_data()

    def add_comrades(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        rank = self.rank_entry.get()
        squad = self.squad_entry.get()
        position = self.position_entry.get()
        status = self.status_entry.get()
        self.management_system.input_comrade(name, age, rank, squad, position, status)
        self.refresh_treeview()
        self.save_data()

        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.rank_entry.delete(0, tk.END)
        self.squad_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)

    def refresh_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for comrade in self.management_system.comrades:
            self.tree.insert("", "end", values=(comrade.name, comrade.age, comrade.rank, comrade.squad, comrade.position, comrade.status))

    def load_data(self):
        data_file = "data.pickle.gz"
        data = []

        try:
            with gzip.open(data_file, "rb") as f:
                data = pickle.load(f)
        except FileNotFoundError:
            print("Data file not found. Starting with empty data.")
        
    if len(data) == 4:
        self.management_system.comrades, self.management_system.commanders, self.management_system.missions, self.management_system.squads = data
    else:
        self.management_system.comrades = []
        self.management_system.commanders = []
        self.management_system.missions = []
        self.management_system.squads = []




    def save_data(self):
        data = [self.management_system.comrades, self.management_system.commanders, self.management_system.missions, self.management_system.squads]
        data_file = "data.pickle.gz"
        compress_data(data, data_file)


if __name__ == "__main__":
    root = tk.Tk()
    app = Comrade_Information_Management_System_GUI(root)
    root.mainloop()

