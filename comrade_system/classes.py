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
