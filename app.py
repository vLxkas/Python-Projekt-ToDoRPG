# app.py
from nicegui import ui
import datetime
from database import create_tables, insert_user, insert_quest, load_users, load_quests, update_quest_status, delete_quest as db_delete_quest
from user import User

create_tables()

user = None
quests_display = None
user_input_area = None  
edit_mode = False
edit_quest_id = None
profile_display = None  

def main_ui():
    global profile_display  
    with ui.row().classes("justify-around gap-6 w-full"):
        with ui.column():  
            ui.label("Benutzerprofil").classes("text-xl font-bold")
            global profile_display
            if profile_display is None:  
                profile_display = ui.column()  
            profile_display.clear()  
            if user:
                user.show_profile(profile_display)  
                ui.label(f'Titel: {user.get_title()}').classes("text-lg")

        with ui.column():  
            ui.label("Neue Quest erstellen").classes("text-xl font-bold")
            global quest_name_input, quest_difficulty_input, quest_deadline_input
            quest_name_input = ui.input(label="Questname")  
            quest_difficulty_input = ui.select(["leicht", "mittel", "schwer"], label="Schwierigkeit")  
            quest_deadline_input = ui.input(label="Fälligkeitsdatum (YYYY-MM-DD)")  
            ui.button("Quest erstellen", on_click=create_quest, color='green')  

        with ui.column():  
            ui.label("Quests").classes("text-xl font-bold")
            global quests_display
            quests_display = ui.column()  
            show_quests()  

    if user:
        ui.button("Abmelden", on_click=logout_user, color='red')  

def show_quests():
    if user is None:
        ui.notify("Bitte melden Sie sich an oder erstellen Sie zuerst einen Benutzer!", color='red')
        return

    global quests_display
    if quests_display:
        quests_display.clear()  

    for quest in load_quests(user.id):
        with quests_display:
            with ui.row():  
                ui.label(f"{quest[2]} ({quest[3]}) - Fällig bis: {quest[4]} - Status: {quest[5]}")
                if quest[5] == 'open':
                    ui.button("Abschließen", on_click=lambda q_id=quest[0]: complete_quest(q_id), color='blue')
                ui.button("Bearbeiten", on_click=lambda q_id=quest[0]: edit_quest(q_id), color='orange')
                ui.button("Löschen", on_click=lambda q_id=quest[0]: delete_quest_handler(q_id), color='red')

def complete_quest(quest_id):
    quest = next(q for q in load_quests(user.id) if q[0] == quest_id)
    xp_earned = calculate_xp(quest[3])  
    user.add_xp(xp_earned)  
    ui.notify(f"Quest abgeschlossen! {xp_earned} XP gewonnen!", color='green')

    update_quest_status(quest_id, "completed")
    
    show_quests()  
    update_user_profile()  

def calculate_xp(difficulty):
    difficulty_map = {'leicht': 10, 'mittel': 25, 'schwer': 50}
    return difficulty_map.get(difficulty, 0)  

def create_user():
    name = user_name_input.value
    race = user_race_input.value
    character_class = user_class_input.value
    users = load_users()

    if any(user_record[1] == name for user_record in users):
        ui.notify("Benutzername bereits vergeben. Bitte wählen Sie einen anderen Namen.", color='red')
        return

    insert_user(name, race, character_class)
    ui.notify(f"Benutzer {name} wurde erfolgreich erstellt!", color='green')

    user_name_input.value = ""
    user_race_input.value = None
    user_class_input.value = None

    user_input_area.clear()  
    show_login_fields()  

def login_user():
    global user
    name = login_name_input.value
    users = load_users()
    
    for user_record in users:
        if user_record[1] == name:
            user = User(
                id=user_record[0],
                name=user_record[1],
                race=user_record[2],
                klass=user_record[3]
            )
            user.level = user_record[4] if len(user_record) > 4 else 1
            user.xp = user_record[5] if len(user_record) > 5 else 0
            user.xp_to_next_level = user_record[6] if len(user_record) > 6 else 100
            ui.notify(f"Willkommen zurück, {name}!", color='green')
            user_input_area.clear()
            main_ui()  
            return

    ui.notify("Benutzer nicht gefunden. Bitte erstellen Sie einen Benutzer.", color='red')

def logout_user():
    global user, profile_display, quests_display
    user = None  
    profile_display = None  
    quests_display = None  
    ui.notify("Sie wurden erfolgreich abgemeldet.", color='green')
    user_input_area.clear()  
    show_login_ui()  

def create_quest():
    if user is None:
        ui.notify("Bitte melden Sie sich zuerst an!", color='red')
        return

    quest_name = quest_name_input.value
    difficulty = quest_difficulty_input.value
    deadline_str = quest_deadline_input.value

    try:
        deadline = datetime.datetime.strptime(deadline_str, "%Y-%m-%d").date()
        today = datetime.date.today()

        if deadline < today:
            ui.notify("Das Fälligkeitsdatum darf nicht in der Vergangenheit liegen.", color='red')
            return

        insert_quest(user.id, quest_name, difficulty, deadline)
        ui.notify("Quest erfolgreich erstellt!", color='green')

        reset_quest_form()  
        show_quests()  

    except ValueError:
        ui.notify("Ungültiges Datum. Bitte im Format YYYY-MM-DD eingeben.", color='red')

def reset_quest_form():
    global edit_mode, edit_quest_id
    quest_name_input.value = ""
    quest_difficulty_input.value = None
    quest_deadline_input.value = ""
    edit_mode = False  
    edit_quest_id = None  

def edit_quest(quest_id):
    global edit_mode, edit_quest_id
    edit_mode = True
    edit_quest_id = quest_id
    quest = next(q for q in load_quests(user.id) if q[0] == quest_id)
    quest_name_input.value = quest[2]  
    quest_difficulty_input.value = quest[3]  
    quest_deadline_input.value = str(quest[4])  

def delete_quest_handler(quest_id):
    db_delete_quest(quest_id)
    ui.notify("Quest erfolgreich gelöscht!", color='green')
    show_quests()  

def update_user_profile():
    if profile_display is not None and user is not None:  
        profile_display.clear()  
        user.show_profile(profile_display)  

def show_login_ui():
    global user_input_area
    with ui.column() as user_input_area:
        ui.label("Benutzerregistrierung / Anmeldung").classes("text-2xl font-bold")
        ui.button("Benutzer erstellen", on_click=show_create_user_ui, color='green')  
        ui.button("Anmelden", on_click=show_login_fields, color='blue')  

def show_create_user_ui():
    global user_input_area
    user_input_area.clear()  
    with user_input_area:
        ui.label("Benutzer erstellen").classes("text-xl font-bold")
        global user_name_input, user_race_input, user_class_input
        user_name_input = ui.input(label="Benutzername")  
        user_race_input = ui.select(["Mensch", "Elf", "Zwerg", "Ork", "Tiermensch"], label="Rasse")  
        user_class_input = ui.select(["Krieger", "Magier", "Schurke", "Paladin", "Jäger"], label="Klasse")  
        
        ui.button("Benutzer erstellen", on_click=create_user, color='green')  
        ui.button("Zurück", on_click=lambda: reset_to_initial_ui(), color='red')  

def reset_to_initial_ui():
    global user_input_area
    user_input_area.clear()  
    show_login_ui()  

def show_login_fields():
    global user_input_area
    user_input_area.clear()  
    with user_input_area:
        ui.label("Anmelden").classes("text-xl font-bold")
        global login_name_input
        login_name_input = ui.input(label="Benutzername")  
        ui.button("Anmelden", on_click=login_user, color='blue')  
        ui.button("Zurück", on_click=lambda: reset_to_initial_ui(), color='red')  

show_login_ui()
ui.run(title="Quest Manager", host="127.0.0.1", port=8080, reload=True)