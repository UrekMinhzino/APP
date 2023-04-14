from datetime import datetime


class Rank:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"


class Comrade:
    def __init__(self, name, rank, date_of_birth, date_of_join, status, squads):
        self.name = name
        self.rank = rank
        self.date_of_birth = date_of_birth
        self.date_of_join = date_of_join
        self.status = status
        self.squads = squads

    def get_age(self):
        delta = datetime.now() - self.date_of_birth
        return delta.days // 365

    def get_service_length(self):
        delta = datetime.now() - self.date_of_join
        return delta.days // 365
    
    def has_mission(self):
        for squad in self.squads:
            if self in squad.members:
                return True
        return False

    def __str__(self):
        return f"{self.name}, {self.rank}, {self.status}"

class Commander(Comrade):
    def __init__(self, name, rank, date_of_birth, date_of_join, status, squads):
        super().__init__(name, rank, date_of_birth, date_of_join, status, squads)
        self.mission = []

    def has_mission(self):
        return bool(self.mission)
    
    def add_mission(self, mission):
        self.mission.append(mission)

class Mission:
    def __init__(self, name, status, squad):
        self.name = name
        self.status = status
        self.squad = squad
        squad.add_mission(self)
    
class Squad:
    def __init__(self, name, commander, members):
        self.name = name
        self.members = members
        self.commander = commander
        self.mission = []

    def add_member(self, comrade):
        self.members.append(comrade)

    def remove_member(self, comrade):
        self.members.remove(comrade)

    def get_members(self):
        return [str(member) for member in self.members]
    
    def add_mission(self, mission):
        self.mission.append(mission)

    def has_mission(self):
        return bool(self.mission)
    
    def __str__(self):
        return f"{self.name}, commanded by {self.commander.name}, with members: {', '.join([m.name for m in self.members])}"

class Comrade_Information_Management_System:
    def __init__(self):
        self.comrades = []
        self.commanders = []
        self.missions = []
        self.squads = []

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

    def input_commander(self):
        print("Commander:")
        while True:
            name = input("Enter name (or leave blank to exit): ")
            if not name:
                break
            rank_name = input("Enter rank name: ")
            rank = Rank(rank_name)
            date_of_birth = datetime.strptime(input("Enter date of birth (YYYY-MM-DD): "), "%Y-%m-%d")
            date_of_join = datetime.strptime(input("Enter date of join (YYYY-MM-DD): "), "%Y-%m-%d")
            status = input("Enter status: ")
            commander = Commander(name, rank, date_of_birth, date_of_join, status, self.squads)
            self.commanders.append(commander)

    def input_mission(self):
        print("Mission:")
        num_mission = int(input("Enter number of mission: "))
        for mission in range(num_mission):
            name = input("Enter name: ")
            status = input("Enter status: ")
            squad_name = input("Assign squad for this mission: ")
            squad = next((s for s in self.squads if s.name == squad_name), None)
            if squad:
                mission = Mission(name, status, squad)
                squad.commander.add_mission(mission)
                self.missions.append(mission)
                print("Mission added successfully!")
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
            print(f"{mission.name}, {mission.status}, assigned to {mission.squad.name}")

    def create_squad(self):
        self.input_squad()
        print("Squad created successfully!")

    def commander_without_squad(self):
        print("Commander(s) who is(are) inactive:")
        for commander in self.commanders:
            if not commander.has_mission():
                print(str(commander))

    def comrade_without_squad(self):
        print("Comrade(s) who is(are) inactive:")
        for comrade in self.comrades:
            if not comrade.has_mission():
                print(str(comrade))

    def run_please(self):
        self.input_comrade()
        self.list_comrades()
        self.input_commander()
        self.list_commanders()
        self.input_squad()
        self.input_mission()
        self.list_missions()
        self.commander_without_squad()
        self.comrade_without_squad()
program = Comrade_Information_Management_System()
program.run_please()