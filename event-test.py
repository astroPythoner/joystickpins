import pygame
import platform
import time
from joystickpins import JoystickPins, KeyboardStick

print(platform.system())

if __name__ == "__main__":
    all_joysticks = [JoystickPins(KeyboardStick())]

    pygame.init()
    for joy in range(pygame.joystick.get_count()):
        pygame_joystick = pygame.joystick.Joystick(joy)
        pygame_joystick.init()
        my_joystick = JoystickPins(pygame_joystick)
        all_joysticks.append(my_joystick)
        print("found_joystick: " + my_joystick.get_name())

    while True:
        for joystick in all_joysticks:
            pressed = [joystick.get_A(), joystick.get_B(), joystick.get_X(), joystick.get_Y(), joystick.get_axis_up(), joystick.get_axis_down(), joystick.get_axis_left(), joystick.get_axis_right(), joystick.get_shoulder_left(), joystick.get_shoulder_right()]
            print(joystick.get_name(), pressed)
            if True in pressed or 1 in pressed:
                print("Button pressed on "+joystick.get_name())
        time.sleep(0.5)