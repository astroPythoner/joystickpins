# joystickpins
pygame add on to easier use controllers for games

# Notwendige Bibliotheken
- pygame
- platform

# Verwendung
Kopiere die read_me.py Datei als \_\_init\_\_.py in dein Projekt. Du kannst dann im Code deines Spiels mit diesen Zeilen joystickpins importieren. 
```
import __init__
import joystickpins
```

### So erstellt du einen neuen Kontroller:
In der Schleife gehst du alle gefundenen Joysticks durch und initialisierst sie mit pygame. Danach gibts du den erstellten Joystick einem neuen Joystickpins objekt und kannst diesen dann verwenden.
Willst du mehrere Joysticks unterstützen kannst du sie in ein Array legen.
```
import pygame
from joystickpins import JoystickPins

for joy in range(pygame.joystick.get_count()):
    pygame_joystick = pygame.joystick.Joystick(joy)
    pygame_joystick.init()
    my_joystick = JoystickPins(pygame_joystick)
```

### So verwendest du den erstellten JoystickPin:
Mit den Methoden kannst du herausfinden welche Köpfe, Joysticks oder Schultern gedrückt werden. Wird None zurückgegeben ist der Kontroller nicht gemapped.
```
my_joystick.get_A()             # returns True when button is pressed
my_joystick.get_B()
my_joystick.get_X()
my_joystick.get_Y()
my_joystick.get_select()        # returns True when Select button is pressed
my_joystick.get_start()         # returns True when start button is pressed
my_joystick.get_shoulder_left() # returns True when Shoulders are pressed button is pressed
my_joystick.get_shoulder_right()
my_joystick.get_axis_left()     # returns True when Joystick is moved into direction
my_joystick.get_axis_right()
my_joystick.get_axis_up()
my_joystick.get_axis_down()

my_joystick.get_name()           # returns the name of the joystick
```

## So mappst du einen neuen Kontroller:
Wenn du einen anderen Kontroller verwenden möchtest musst du dem Programm erst sagen, welche Knöpfe und Achsen was bedeuten.

Um herauszufinden welcher Knopf auf deinem Joystick wie nummeriert ist starte die python Datei event-text.py.
Es öffnet sich dann einen pygame Fenster. In der Zeile ganz unten siehst du die Namen der angeschlossenen Kontroller.
Merke dir den Namen des Kontrollers, den du hinzufügen möchtest und drücke dann einmal alle Knöpfe und bewege die Joysticks.
Beim drücken eines Knopfes/bewegen einer Achse wird nun die dazugehörige Nummer angezeigt.

Ganz oben in der joystickpins.py Datei findest du das Dictionary mit den mappings. Füge dort deinen Kontroller hinzu:

Ersetze den Namen und die Nummer, gegen die, die du gerade herausgefunden hast.
```
joystick_mappings = {
            '<name>' :       {
                'A'         : <A/Kreis>,
                'B'         : <B/Kreuz>,
                'X'         : <X/Dreieck>,
                'Y'         : <Y/Viereck>,
                'SELECT'    : <Select>,
                'START'     : <Start>,
                'SH_LEFT'   : <Schulter links>,
                'SH_RIGHT'  : <Schulter rechts>,
                'AXIS_X'    : <Joystick x-Richtung>,
                'AXIS_Y'    : <Joystick y-Richtung>
            },
```
