### Little pygame screen showing the events of a controller (just for testing)
# pygame needs to be installed to run this script

import pygame
import time
from joystickpins import JoystickPins, KeyboardStick, MouseAddOnStick

# Bildschrimgröße
WIDTH = 480*2
HEIGHT = 320*2
FPS = 60

# Pygame initialisieren und Fenster aufmachen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Event Test!")
clock = pygame.time.Clock()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# finde passendste Schriftart zu arial.
font_name = pygame.font.match_font('arial')

# Tasten
A = "a"
B = "b"
X = "x"
Y = "y"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
SHOULDER_LEFT = "shoulder left"
SHOULDER_RIGHT = "shoulder right"
SELECT= "select"
START = "start"
ESC = "esc"
ALL = "all"

class Game():
    def __init__(self):
        self.running = True

        self.pressed_button_texts = ["Jetzt Taste auf deinem Controller drücken"]

        self.all_joysticks = []
        self.find_josticks()

    def find_josticks(self):
        # Knöpfe und Kontroller finden und Initialisieren
        self.all_joysticks = []
        #self.all_joysticks.append(JoystickPins(KeyboardStick()))
        #self.all_joysticks.append(JoystickPins(KeyboardStick('Alt1')))
        self.all_joysticks.append(JoystickPins(MouseAddOnStick()))
        for joy in range(pygame.joystick.get_count()):
            pygame_joystick = pygame.joystick.Joystick(joy)
            pygame_joystick.init()
            my_joystick = JoystickPins(pygame_joystick)
            self.all_joysticks.append(my_joystick)
            print("found_joystick: " + my_joystick.get_name())
        print("joystick-count=", len(self.all_joysticks))

    def draw_text(self, surf, text, size, x, y, color=WHITE, rect_place="oben_mitte"):
        # Zeichnet den text in der color auf die surf.
        # x und y sind die Koordinaten des Punktes rect_place. rect_place kann "oben_mitte", "oben_links" oder "oben_rechts" sein.
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if rect_place == "oben_mitte":
            text_rect.midtop = (x, y)
        elif rect_place == "oben_links":
            text_rect.x = x
            text_rect.y = y
        elif rect_place == "oben_rechts":
            text_rect.topright = (x, y)
        surf.blit(text_surface, text_rect)

    def check_key_pressed(self, check_for=ALL, joysticks = None):
        # Überprüft ob die Taste(n) check_for gedrückt ist.
        if joysticks == None:
            joysticks = self.all_joysticks
        for joystick in joysticks:
            if check_for == LEFT:
                if joystick.get_axis_left():
                    return joystick
            if check_for == RIGHT:
                if joystick.get_axis_right():
                    return joystick
            if check_for == SHOULDER_LEFT:
                if joystick.get_shoulder_left():
                    return joystick
            if check_for == SHOULDER_RIGHT:
                if joystick.get_shoulder_right():
                    return joystick
            if check_for == UP:
                if joystick.get_axis_up():
                    return joystick
            if check_for == DOWN:
                if joystick.get_axis_down():
                    return joystick
            if check_for == A:
                if joystick.get_A():
                    return joystick
            if check_for == B:
                if joystick.get_B():
                    return joystick
            if check_for == X:
                if joystick.get_X():
                    return joystick
            if check_for == Y:
                if joystick.get_Y():
                    return joystick
            if check_for == SELECT:
                if joystick.get_select():
                    return joystick
            if check_for == START:
                if joystick.get_start():
                    return joystick
            if check_for == ESC:
                if joystick.get_select() and joystick.get_start():
                    return joystick
            if check_for == ALL:
                if joystick.get_A() or joystick.get_B() or joystick.get_X() or joystick.get_Y() or joystick.get_start() or joystick.get_shoulder_left() or joystick.get_shoulder_right() or joystick.get_axis_left() or joystick.get_axis_right() or joystick.get_axis_up() or joystick.get_axis_down():
                    return joystick
        return False

    def start_game(self):

        # Daurschleife
        while self.running:

            # Bilschirm leeren
            screen.fill(BLACK)

            print(self.all_joysticks)

            # Eingaben zum Verlassen des Spiels checken
            if self.check_key_pressed(ESC):
                self.running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Gedrückte Tasten erkennen und auf dem Display anzeigen
            self.detect_presses()
            self.draw_display()

            # Nachdem alles gezeichnet ist anzeigen
            pygame.display.flip()

    def detect_presses(self):
        # Gedrückte Tasten erkennen
        for joystick in self.all_joysticks:
            if joystick.mapping != {}:
                a = self.check_key_pressed(A)
                if a != False:
                    self.pressed_button_texts.append("A gedrückt (" + str(a.get_name()) + " , btn num:" + str(a._A) + ")")
                b = self.check_key_pressed(B)
                if b != False:
                    self.pressed_button_texts.append("B gedrückt (" + str(b.get_name()) + " , btn num:" + str(b._B) + ")")
                x = self.check_key_pressed(X)
                if x != False:
                    self.pressed_button_texts.append("X gedrückt (" + str(x.get_name()) + " , btn num:" + str(x._X) + ")")
                y = self.check_key_pressed(Y)
                if y != False:
                    self.pressed_button_texts.append("Y gedrückt (" + str(y.get_name()) + " , btn num:" + str(y._Y) + ")")
                up = self.check_key_pressed(UP)
                if up != False:
                    self.pressed_button_texts.append("Up gedrückt (" + str(up.get_name()) + " , Achse:" + str(up._axis_y) + ")")
                down = self.check_key_pressed(DOWN)
                if down != False:
                    self.pressed_button_texts.append("Down gedrückt (" + str(down.get_name()) + " , Achse:" + str(down._axis_y) + ")")
                left = self.check_key_pressed(LEFT)
                if left != False:
                    self.pressed_button_texts.append("Left gedrückt (" + str(left.get_name()) + " , Achse:" + str(left._axis_x) + ")")
                right = self.check_key_pressed(RIGHT)
                if right != False:
                    self.pressed_button_texts.append("Right gedrückt (" + str(right.get_name()) + " , Achse:" + str(right._axis_x) + ")")#
                shouler_left = self.check_key_pressed(SHOULDER_LEFT)
                if shouler_left != False:
                    self.pressed_button_texts.append("Schulter Links gedrückt (" + str(shouler_left.get_name()) + " , btn num:" + str(shouler_left._shoulder_left) + ")")
                shoulder_right = self.check_key_pressed(SHOULDER_RIGHT)
                if shoulder_right != False:
                    self.pressed_button_texts.append("Schulter Rechts gedrückt (" + str(shoulder_right.get_name()) + " , btn num:" + str(shoulder_right._shoulder_right) + ")")
                start = self.check_key_pressed(START)
                if start != False:
                    self.pressed_button_texts.append("Start gedrückt (" + str(start.get_name()) + " , btn num:" + str(start._start) + ")")
                select = self.check_key_pressed(SELECT)
                if select != False:
                    self.pressed_button_texts.append("Select gedrückt (" + str(select.get_name()) + " , btn num:" + str(select._select) + ")")
            else:
                axes = joystick.joystick.get_numaxes()
                for i in range(axes):
                    if joystick.get_axis(i):
                        self.pressed_button_texts.append("Achse gedrückt (undefined mapping; " + str(joystick.get_name()) + " , Achse:" + str(i) + ")")

                buttons = joystick.joystick.get_numbuttons()
                for i in range(buttons):
                    if joystick.get_button(i):
                        self.pressed_button_texts.append("Knopf gedrückt (undefined mapping; " + str(joystick.get_name()) + " , btn num:" + str(i) + ")")

        while len(self.pressed_button_texts) > 15:
            del self.pressed_button_texts[0]

    def draw_display(self):
        # Auf dem Display anzeigen
        for num, text in enumerate(self.pressed_button_texts):
            self.draw_text(screen,text,30,WIDTH/2,num*40)
        text = ""
        for joystick in self.all_joysticks:
            text += ", "+joystick.get_name()
        self.draw_text(screen, str(len(self.all_joysticks))+" Joysticks:"+text[1:], 30, WIDTH / 2, HEIGHT-35)

game = Game()
game.start_game()

pygame.quit()