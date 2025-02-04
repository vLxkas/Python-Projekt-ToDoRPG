# user.py
from nicegui import ui
from database import update_user_xp_and_level  

class User:
    def __init__(self, id, name, race, klass):
        self.id = id  
        self.name = name  
        self.race = race  
        self.klass = klass  
        self.level = 1  
        self.xp = 0  
        self.quests = []  
        self.xp_to_next_level = 100  

    def add_xp(self, xp):
        self.xp += xp
        while self.xp >= self.xp_to_next_level:
            self.level_up()  
        update_user_xp_and_level(self.id, self.xp, self.level, self.xp_to_next_level)

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level  
        self.xp_to_next_level = int(self.xp_to_next_level * 1.1)  
        ui.notify(f'Glückwunsch! {self.name} ist auf Level {self.level} aufgestiegen!', color='green')

    def get_title(self):
        level_titles = {
            5: "Novize",
            10: "Abenteurer",
            15: "Kämpfer",
            20: "Veteran",
            25: "Held",
            30: "Champion",
            40: "Eroberer",
            50: "Meister",
            60: "Legende I",
            80: "Legende II",
            100:"Legende III",
            150:"Legende IV",
            200:"Legende V",
            500:"Unstoppable",
            1000:"Unkillable",
        }
        for level in sorted(level_titles.keys(), reverse=True):
            if self.level >= level:
                return level_titles[level]
        return "Neuling"  

    def show_profile(self, profile_display):
        profile_display.clear()  
        with profile_display:
            ui.label(f'Name: {self.name}')  
            ui.label(f'Rasse: {self.race}')  
            ui.label(f'Klasse: {self.klass}')  
            ui.label(f'Level: {self.level}')  
            ui.label(f'XP: {self.xp}/{self.xp_to_next_level}')  