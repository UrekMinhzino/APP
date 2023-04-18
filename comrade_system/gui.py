import tkinter as tk
from tkinter import *
from management_system import Comrade_Information_Management_System

class MilitaryApp(tk.Tk):
    def __init__(self, program):
        super().__init__()

        self.title("Military Information Management System")
        self.geometry("800x600")
        self.configure(bg="dark green")

        # Left Panel
        self.comrades_frame = ComradesFrame(self, program)
        self.comrades_frame.grid(row=0, column=0, padx=20, pady=20)

        self.commanders_frame = CommandersFrame(self, program)
        self.commanders_frame.grid(row=1, column=0, padx=20, pady=20)

        self.squads_frame = SquadsFrame(self, program)
        self.squads_frame.grid(row=0, column=1, padx=20, pady=20)

        self.missions_frame = MissionsFrame(self, program)
        self.missions_frame.grid(row=1, column=1, padx=20, pady=20)

class InputFrame(tk.Frame):
    def __init__(self, parent, program, label_text, input_function):
        tk.Frame.__init__(self, parent, bg="dark green", padx=10, pady=10)

        # Title
        self.label = tk.Label(self, text=label_text, bg="dark green", fg="white", font=("Ariel", 20, 'bold'))
        self.label.pack(pady=10)

        # Name Entry
        self.name_entry = tk.Entry(self, font=("Ariel", 16))
        self.name_entry.pack(pady=5)

        # Rank Entry
        self.rank_entry = tk.Entry(self, font=("Ariel", 16))
        self.rank_entry.pack(pady=5)

        # Button
        self.add_button = tk.Button(self, text="Add", font=("Ariel", 16), bg="deep sky blue", fg="white", relief='ridge', activebackground='dark blue', activeforeground='white', command=input_function)
        self.add_button.pack(pady=10)

class ComradesFrame(InputFrame):
    def __init__(self, parent, program):
        super().__init__(parent, program, "Comrades", self.add_comrade)
        self.program = program

    def add_comrade(self):
        name = self.name_entry.get()
        rank = self.rank_entry.get()

        self.program.input_comrade(name, rank)

        self.name_entry.delete(0, 'end')
        self.rank_entry.delete(0, 'end')

class CommandersFrame(InputFrame):
    def __init__(self, parent, program):
        super().__init__(parent, program, "Commanders", self.add_commander)
        self.program = program

    def add_commander(self):
        name = self.name_entry.get()
        rank = self.rank_entry.get()

        self.program.input_commander(name, rank)

        self.name_entry.delete(0, 'end')
        self.rank_entry.delete(0, 'end')

class SquadsFrame(InputFrame):
    def __init__(self, parent, program):
        super().__init__(parent, program, "Squads", self.add_squad)
        self.program = program

    def add_squad(self):
        squad_name = self.name_entry.get()
        commander_id = self.rank_entry.get()

        self.program.input_squad(squad_name, commander_id)

        self.name_entry.delete(0, 'end')
        self.rank_entry.delete(0, 'end')

class MissionsFrame(InputFrame):
    def __init__(self, parent, program):
        super().__init__(parent, program, "Missions", self.add_mission)
        self.program = program

    def add_mission(self):
        mission_name = self.name_entry.get()
        squad_id = self.rank_entry.get()

        self.program.input_mission(mission_name, squad_id)

        self.name_entry.delete(0, 'end')
        self.rank_entry.delete(0, 'end')


if __name__ == "__main__":
    program = Comrade_Information_Management_System()
    app = MilitaryApp(program)
    app.mainloop()
