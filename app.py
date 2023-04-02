from datetime import datetime


class Rank:
    def __init__(self, name, description, pay_grade):
        self.name = name
        self.description = description
        self.pay_grade = pay_grade

    def __str__(self):
        return f"{self.name} ({self.pay_grade})"


class Comrade:
    def __init__(self, name, rank, date_of_birth, date_of_join, status):
        self.name = name
        self.rank = rank
        self.date_of_birth = date_of_birth
        self.date_of_join = date_of_join
        self.status = status

    def get_age(self):
        delta = datetime.now() - self.date_of_birth
        return delta.days // 365

    def get_service_length(self):
        delta = datetime.now() - self.date_of_join
        return delta.days // 365

    def __str__(self):
        return f"{self.name}, {self.rank}, {self.status}"


class Clearance:
    def __init__(self, level):
        self.level = level

    def __str__(self):
        return f"{self.level}"


class Commander(Comrade):
    def __init__(self, name, rank, date_of_birth, date_of_join, status, clearance_level):
        super().__init__(name, rank, date_of_birth, date_of_join, status)
        self.clearance = Clearance(clearance_level)


class Mission:
    def __init__(self, name, status, unit):
        self.name = name
        self.status = status
        self.unit = unit


class Squad:
    def __init__(self, name, members):
        self.name = name
        self.members = members

    def add_member(self, comrade):
        self.members.append(comrade)

    def remove_member(self, comrade):
        self.members.remove(comrade)

    def get_members(self):
        return [str(member) for member in self.members]

class Comrade_Information_Management_System:
    def __init__(self):
        self.comrades = []
        self.commanders = []
        self.missions = []
        self.squads = []

    def input_comrade(self):
        name = input("Enter name: ")
        rank_name = input("Enter rank name: ")
        rank_description = input("Enter rank description: ")
        rank_pay_grade = input("Enter rank pay grade: ")
        rank = Rank(rank_name, rank_description, rank_pay_grade)
        date_of_birth = datetime.strptime(input("Enter date of birth (YYYY-MM-DD): "), "%Y-%m-%d")
        date_of_join = datetime.strptime(input("Enter date of join (YYYY-MM-DD): "), "%Y-%m-%d")
        status = input("Enter status: ")
        comrade = Comrade(name, rank, date_of_birth, date_of_join, status)
        self.comrades.append(comrade)

    def input_commander(self):
        name = input("Enter name: ")
        rank_name = input("Enter rank name: ")
        rank_description = input("Enter rank description: ")
        rank_pay_grade = input("Enter rank pay grade: ")
        rank = Rank(rank_name, rank_description, rank_pay_grade)
        date_of_birth = datetime.strptime(input("Enter date of birth (YYYY-MM-DD): "), "%Y-%m-%d")
        date_of_join = datetime.strptime(input("Enter date of join (YYYY-MM-DD): "), "%Y-%m-%d")
        status = input("Enter status: ")
        clearance_level = input("Enter clearance level: ")
        commander = Commander(name, rank, date_of_birth, date_of_join, status, clearance_level)
        self.commanders.append(commander)

    def input_mission(self):
        name = input("Enter name: ")
        status = input("Enter status: ")
        unit = input("Enter unit: ")
        mission = Mission(name, status, unit)
        self.missions.append(mission)

    def input_squad(self):
        name = input("Enter name: ")
        members = []
        while True:
            member_name = input("Enter member name (or leave blank to exit): ")
            if member_name == "":
                break
            comrade = next((c for c in self.comrades if c.name == member_name), None)
            if comrade:
                members.append(comrade)
            else:
                print("Comrade not found.")
        squad = Squad(name, members)
        self.squads.append(squad)

    def list_comrades(self):
        print("Comrades:")
        for comrade in self.comrades:
            print(str(comrade))

    def list_commanders(self):
        print("Commanders:")
        for commander in self.commanders:
            print(str(commander))

    def list_missions(self):
        print("Missions:")
        for mission in self.missions:
            print(f"{mission.name}, {mission.status}, {mission.unit}")

    def list_squads(self):
        print("Squads:")
        for squad in self.squads:
            print(squad.name)
            members = squad.get_members()
        if members:
            print("  Members:")
            for member in members:
                print(f"    - {member}")
            else:
                print("  No members.")

    def create_squad(self):
        self.input_squad()
        print("Squad created successfully!")

    def run_please(self):
        self.input_comrade()
        self.input_commander()
        self.input_mission()
        self.list_comrades()
        self.list_commanders()
        self.list_missions()
        self.create_squad()
        self.list_squads()

program = Comrade_Information_Management_System()
program.run_please()