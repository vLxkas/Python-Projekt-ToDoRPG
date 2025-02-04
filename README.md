Dokumentation Python Projekt ToDo-RPG 

Mitglieder: Lukas Reinhart, („Luca Wolfarth“)
Ursprüngliche Aufteilung: 
Lukas: Speicherung der Daten, Leveling-System, Erstellung der User
Luca: Erstellen, bearbeiten, löschen von Quests, Grafische Oberfläche
Letztendliche Aufteilung aufgrund des Ausbildungsabbruches:
Da auf das alte GIT-Repository nicht mehr zugegriffen werden kann, wurde alles von Grund an neu programmiert.
Grundlegende Funktion des Programms:
-Beim Start des Programms über app.py wird die Datenbank über die Funktion create_tables in database.py sowie die nötigen Tabellen erstellt und in app.py bei jedem Start aufgerufen.
-Anschließend kann über den Button Benutzer erstellen ein neuer Benutzer angelegt werden. Dabei kann man seinen Namen eingeben, sowie eine Klasse und Rasse auswählen. Die Funktion create_user fängt dabei an die Eingabewerte user_name_input, user_race_input sowie user_class_input aufzurufen. Durch die Funktion load_users werden danach alle bereits erstellten Benutzer aus der Datenbank geladen und überprüft, ob der Benutzername bereits in der Datenbank vorhanden ist. Ist dies der Fall wird eine Benachrichtigung erscheinen, die einen dazu auffordert, einen anderen Namen zu verwenden. Falls der Name frei ist, wird die Funktion insert_user aufgerufen und der Benutzer wird erstellt. Danach werden die Eingabefelder geleert und man wird zur Anmeldeseite (show_login_fields) weitergeleitet.
-Sollte man sich umentscheiden und einen anderen Namen wollen kann man über den Button Zurück ganz einfach wieder auf die Startseite gelangen und einen neuen Benutzer erstellen.
-Nach der Erstellung eines Benutzers kann man sich mit diesem direkt, nachdem man den Namen eingegeben hat, anmelden über den Button Anmelden. Will man sich mit einem Benutzer anmelden, der noch nicht in der Datenbank hinzugefügt ist, wird ein Fehler ausgegeben der einen auffordert einen Benutzer zu erstellen. Gibt man einen Benutzernamen ein, der in der Datenbank vorhanden ist, wird man auf die Profilseite über die Funktion main_ui weitergeleitet.
-Auf der Profilseite werden unter Benutzerprofil alle Informationen über den Charakter angegeben (Name, Rasse, Klasse, Benutzerlevel, Fehlende XP zum nächsten Level sowie der Titel) (show_profile in user.py). Diese Informationen werden bei jeder Änderung überprüft und über die Datenbank database.db aufgerufen und wenn nötig aktualisiert (update_user_xp_and_level in user.py). Zusätzlich gibt es den Button Abmelden, der einen auf die Startseite weiterleitet (logout-user in app.py).
-In der Mitte der Profilseite unter Neue Quest erstellen können Quests erstellt werden. Hier kann ein Name eingegeben werden sowie eine Schwierigkeit und ein Fälligkeitsdatum. Hierbei wird bei der Eingabe das aktuelle Datum überprüft und ein Fehler ausgegeben sollte das eingegebene Datum in der Vergangenheit liegen. (Variablen deadline und today).
-Sobald eine Quest erstellt wird, wird diese in der Datenbank gespeichert mit der insert_quest Funktion in database.py.
-Die Quests können abgeschlossen, bearbeitet und gelöscht werden. (complete_quest, edit_quest, delete_quest_handler). Die Quests werden anschließend mithilfe von ID’s in der Datenbank angepasst oder gelöscht.
-Sobald eine Quest abgeschlossen wird, wird je nach dem Schwierigkeitsgrad XP dem jeweiligen Benutzer hinzugefügt. (complete_quest). Die XP werden mit calculate_xp ermittelt und hinzugefügt.
-Der Titel wird je nach vorhandener Stufe mit angepasst und soll somit dazu motivieren mehr Quests abzuschließen, um einen höheren Titel zu erhalten. Dabei überprüft die Funktion add_xp die XP-Anzeige und falls die XP zur nächsten Stufe ausreichen wird mit level_up das Level erhöht sowie Titel angepasst.

Fehlende Aspekte des Programms:
-Aufgrund falscher Zeiteinschätzung konnten keine Profilbilder oder ähnliches hinzugefügt werden 






				
