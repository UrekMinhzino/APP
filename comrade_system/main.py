from tkinter import *
from gui import MilitaryApp
from management_system import Comrade_Information_Management_System

def main():
    program = Comrade_Information_Management_System()
    app = MilitaryApp(program)
    app.mainloop()

if __name__ == "__main__":
    main()
