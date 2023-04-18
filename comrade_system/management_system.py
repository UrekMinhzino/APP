import csv
from datetime import datetime
from classes import Rank, Comrade, Commander, Mission, Squad
import zipfile
import pickle
import gzip
import threading
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


DATA_ARCHIVE = "comrades_system.dat"

def compress_data(data, file_name):
    with gzip.open(file_name, 'wb') as f:
        pickle.dump(data, f)

def decompress_data(file):
    data = None
    with gzip.open(file, 'rb') as f:
        if f.peek(1):
            data = pickle.load(f)
        else:
            data = []
    return data


def export_data(self):
    return {
        "comrades": self.comrades,
        "commanders": self.commanders,
        "missions": self.missions,
        "squads": self.squads,
    }


class Comrade_Information_Management_System:
    def __init__(self, data=None):
        self.comrades = data.get("comrades", []) if data else []
        self.commanders = data.get("commanders", []) if data else []
        self.missions = data.get("missions", []) if data else []
        self.squads = data.get("squads", []) if data else []


    def input_comrade(self):
        print("Comrade:")
        while True:
            name = input("Enter name (or leave blank to exit): ")
            if name == "":
                break
            rank_name = input("Enter rank name: ")
            rank = Rank(rank_name)
            date_of_birth = datetime.strptime(input("Enter date of birth (YYYY-MM-DD): "), "%Y-%m-%d")
            date_of_join = datetime.strptime(input("Enter date of join (YYYY-MM-DD): "), "%Y-%m-%d")
            status = input("Enter status: ")
            comrade = Comrade(name, rank, date_of_birth, date_of_join, status, self.squads)
            self.comrades.append(comrade)

        with open("comrades.txt", "w", newline = '') as f:
            writer = csv.writer(f)
            for comrade in self.comrades:
                writer.writerow([comrade.name, comrade.rank.name, comrade.date_of_birth, comrade.date_of_join, comrade.status])
   
    def input_commander(self):
        print("Commander:")
        while True:
            name = input("Enter name (or leave blank to exit): ")
            if name == "":
                break
            rank_name = input("Enter rank name: ")
            rank = Rank(rank_name)
            date_of_birth = datetime.strptime(input("Enter date of birth (YYYY-MM-DD): "), "%Y-%m-%d")
            date_of_join = datetime.strptime(input("Enter date of join (YYYY-MM-DD): "), "%Y-%m-%d")
            status = input("Enter status: ")
            commander = Commander(name, rank, date_of_birth, date_of_join, status, [])
            self.commanders.append(commander)

        with open("commanders.txt", "w", newline='') as f:
            writer = csv.writer(f)
            for commander in self.commanders:
                writer.writerow([commander.name, commander.rank.name, commander.date_of_birth, commander.date_of_join, commander.status])

    def input_mission(self):
        print("Mission:")
        num_mission = int(input("Enter number of mission: "))
        with open("missions.txt", "w") as missions_file:
            pass

        for mission in range(num_mission):
            name = input("Enter mission name: ")
            status = input("Enter status: ")
            squad_name = input("Assign squad for this mission: ")
            squad = next((s for s in self.squads if s.name == squad_name), None)
            if squad:
                mission = Mission(name, status, squad)
                squad.commander.add_mission(mission)
                self.missions.append(mission)
                print("Mission added successfully!")

                with open("missions.txt", "a") as missions_file:
                    missions_file.write(f"{name},{status},{squad_name}\n")

                with open("commander_missions.txt", "w") as cmd_missions_file:
                    for commander in self.commanders:
                        for m in commander.mission:
                            cmd_missions_file.write(f"{commander.name},{m.name}\n")

                for comrade in squad.members:
                    with open("comrade_missions.txt", "w") as c_missions_file:
                        for m in comrade.squads[0].mission:
                            c_missions_file.write(f"{comrade.name},{m.name}\n")
            else:
                print("Squad not found.")


                
    def input_squad(self):
        print("Squad:")
        num_squad = int(input("Enter number of squad: "))

        squads = []
        for i in range(num_squad):
            squad_name = input(f"Enter squad {i + 1} name: ")
            while True:
                commander_name = input(f"Enter commander who will lead squad {i + 1}: ")
                commander = next((c for c in self.commanders if c.name == commander_name), None)
                if commander:
                    is_assigned = any(squad.commander == commander for squad in self.squads)
                    if is_assigned:
                        print("This commander is already assigned to another squad.")
                    else:
                        break
                else:
                    print("Commander not found.")
        
            squad = Squad(squad_name, commander, [])
            squads.append(squad)
            self.squads.append(squad)
            print(f"Squad {squad_name} created with commander {commander_name}")

        for i, squad in enumerate(squads):
            print(f"Input members to squad {i + 1} ({squad.name}):")
            while True:
                member_name = input("Enter member name (or leave blank to exit):")
                if member_name == "":
                    break
                comrade = next((c for c in self.comrades if c.name == member_name), None)
                if comrade:
                    squad.add_member(comrade)
                    print(f" + {comrade.name}")
                else:
                    print("Comrade not found.")

        print(f"Members added to squad {squad_name} with commander {squad.commander.name}:")
        for member in squad.members:
            print(f" + {member.name}")
    
        print("List squad(s) created:")
        for squad in squads:
                print(f"{squad}")

        with open("squads.txt", "w") as f:
            for squad in self.squads:
                f.write(f"{squad.name},{squad.commander.name},{','.join([m.name for m in squad.members])}\n")

    def list_comrades(self):
        print("Comrades:")
        with open("comrades.txt", "r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                name, rank, date_of_birth, date_of_join, status = row
                rank_obj = Rank(rank)
                date_of_birth_obj = datetime.strptime(date_of_birth, "%Y-%m-%d %H:%M:%S")
                date_of_join_obj = datetime.strptime(date_of_join, "%Y-%m-%d %H:%M:%S")
                comrade = Comrade(name, rank_obj, date_of_birth_obj, date_of_join_obj, status, self.squads)
                self.comrades.append(comrade)
                print(f"{name}, {rank}, {date_of_birth}, {date_of_join}, {status}")


    def list_commanders(self):
        print("Commanders:")
        with open("commanders.txt", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                name, rank, date_of_birth, date_of_join, status = row
                rank_obj = Rank(rank)
                date_of_birth_obj = datetime.strptime(date_of_birth, "%Y-%m-%d %H:%M:%S")
                date_of_join_obj = datetime.strptime(date_of_join, "%Y-%m-%d %H:%M:%S")
                commander = Commander(name, rank_obj, date_of_birth_obj, date_of_join_obj, status, [])
                self.commanders.append(commander)
                print(f"{name}, {rank}, {date_of_birth}, {date_of_join}, {status}")

    def list_missions(self):
        print("Missions:")
        with open("missions.txt", "r") as file:
            for line in file.readlines():
                name, status, squad_name = line.strip().split(",")
                print(f"{name}, {status}, assigned to {squad_name}")

    def create_squad(self):
        self.input_squad()
        print("Squad created successfully!")

    def commander_without_squad(self):
        print("Commander(s) who is(are) inactive:")
        with open("commanders.txt", "r") as file:
            for line in file.readlines():
                name, rank, date_of_birth, date_of_join, status = line.strip().split(",")
                commander = next((c for c in self.commanders if c.name == name), None)
                if commander and not commander.has_mission():
                    print(f"{name}, {rank}, {status}")


    def comrade_without_squad(self):
        print("Comrade(s) who is(are) inactive:")
        with open("comrades.txt", "r") as file:
            for line in file.readlines():
                name, rank, date_of_birth, date_of_join, status = line.strip().split(",")
                comrade = next((c for c in self.comrades if c.name == name), None)
                if comrade and not comrade.has_mission():
                    print(f"{name}, {rank}, {status}")

    def add_comrade_to_file(name, age, rank, squad):
        with open("comrade.txt", "a") as file:
            file.write(f"{name},{age},{rank},{squad}\n")

    def read_comrades_from_file():
        comrades = []
        with open("comrade.txt", "r") as file:
            for line in file:
                name, age, rank, squad = line.strip().split(",")
                comrades.append((name, age, rank, squad))
        return comrades

    def add_commander_to_file(name, age, rank, squad):
        with open("commander.txt", "a") as file:
            file.write(f"{name},{age},{rank},{squad}\n")

    def read_commanders_from_file():
        commanders = []
        with open("commander.txt", "r") as file:
            for line in file:
                name, age, rank, squad = line.strip().split(",")
                commanders.append((name, age, rank, squad))
        return commanders
    
    def add_squad_to_file(name, commander, members):
        with open("squads.txt", "a") as file:
            file.write(f"{name},{commander},{members}\n")
    
    def read_squads_from_file():
        squads = []
        with open("squads.txt", "r") as file:
            for line in file:
                name, commander, members = line.strip().split(",")
                squads.append((name, commander, members))
        return squads
    
    def add_mission_to_file(name, squad):
        with open("missions.txt", "a") as file:
            file.write(f"{name},{squad}\n")

    def read_mission_from_file():
        missions = []
        with open("missions.txt", "r") as file:
            for line in file:
                name, squad = line.strip().split(",")
                missions.append((name, squad))
        return missions

class Comrade_Information_Management_System_GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Comrade Information Management System")
        self.master.geometry("800x600")
        self.management_system = Comrade_Information_Management_System()

        self.run_please()
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.comrades_tab = ttk.Frame(self.notebook)
        self.commanders_tab = ttk.Frame(self.notebook)
        self.missions_tab = ttk.Frame(self.notebook)
        self.squads_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.comrades_tab, text="Comrades")
        self.notebook.add(self.commanders_tab, text="Commanders")
        self.notebook.add(self.missions_tab, text="Missions")
        self.notebook.add(self.squads_tab, text="Squads")

        # Populate each tab with necessary widgets and layout
        self.create_comrades_tab()
        self.create_commanders_tab()
        self.create_missions_tab()
        self.create_squads_tab()

    def create_comrades_tab(self):
        # Add widgets and layout for the comrades tab
        self.add_comrade_button = ttk.Button(self.comrades_tab, text="Add Comrade", command=self.management_system.input_comrade)
        self.add_comrade_button.pack(pady=10)
        
        self.list_comrades_button = ttk.Button(self.comrades_tab, text="List Comrades", command=self.management_system.list_comrades)
        self.list_comrades_button.pack(pady=10)
        
    def create_commanders_tab(self):
        # Add widgets and layout for the commanders tab
        self.add_commander_button = ttk.Button(self.commanders_tab, text="Add Commander", command=self.management_system.input_commander)
        self.add_commander_button.pack(pady=10)
        
        self.list_commanders_button = ttk.Button(self.commanders_tab, text="List Commanders", command=self.management_system.list_commanders)
        self.list_commanders_button.pack(pady=10)

    def create_missions_tab(self):
        # Add widgets and layout for the missions tab
        self.add_mission_button = ttk.Button(self.missions_tab, text="Add Mission", command=self.management_system.input_mission)
        self.add_mission_button.pack(pady=10)
        
        self.list_missions_button = ttk.Button(self.missions_tab, text="List Missions", command=self.management_system.list_missions)
        self.list_missions_button.pack(pady=10)

    def create_squads_tab(self):
        # Add widgets and layout for the squads tab
        self.squads_listbox = tk.Listbox(self.squads_tab)
        self.squads_listbox.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.squads_scrollbar = tk.Scrollbar(self.squads_tab, orient=tk.VERTICAL, command=self.squads_listbox.yview)
        self.squads_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.squads_listbox.config(yscrollcommand=self.squads_scrollbar.set)

        self.squads_buttons_frame = tk.Frame(self.squads_tab)
        self.squads_buttons_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_squad_button = tk.Button(self.squads_buttons_frame, text="Add Squad", command=self.add_squad)
        self.add_squad_button.pack(fill=tk.X)

        self.remove_squad_button = tk.Button(self.squads_buttons_frame, text="Remove Squad", command=self.remove_squad)
        self.remove_squad_button.pack(fill=tk.X)

        self.list_squads_button = tk.Button(self.squads_buttons_frame, text="List Squads", command=self.list_squads)
        self.list_squads_button.pack(fill=tk.X)

    def add_squad(self):
        self.management_system.input_squad()
        self.refresh_squads()

    def remove_squad(self):
        selected_squad = self.squads_listbox.get(self.squads_listbox.curselection())
        self.management_system.squads.remove(selected_squad)
        self.refresh_squads()

    def list_squads(self):
        self.refresh_squads()

    def refresh_squads(self):
        self.squads_listbox.delete(0, tk.END)
        for squad in self.management_system.squads:
            self.squads_listbox.insert(tk.END, f"{squad.name}")

    def run_please(self):
        data_file = "data.pickle.gz"
        data = decompress_data(data_file)

        if len(data) == 4:
            self.management_system.comrades, self.management_system.commanders, self.management_system.missions, self.management_system.squads = data
        else:
            self.management_system.comrades = []
            self.management_system.commanders = []
            self.management_system.missions = []
            self.management_system.squads = []

if __name__ == "__main__":
    root = tk.Tk()
    app = Comrade_Information_Management_System_GUI(root)
    root.mainloop()


    def run_please(self):
        data_file = "data.pickle.gz"
        data = decompress_data(data_file)
    
        if len(data) == 4:
            self.comrades, self.commanders, self.missions, self.squads = data
        else:
            self.comrades = []
            self.commanders = []
            self.missions = []
            self.squads = []

    
