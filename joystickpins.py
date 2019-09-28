import pygame as pg
import platform
from pygame import joystick

#Pins-Mapping: (A, B, X, Y, SELECT, START, SHOULDER_LEFT, SHOULDER_RIGHT, AXIS_X, AXIS_Y)
joystick_mappings = {
            'USB Gamepad' :       {
                'A'         : 1,
                'B'         : 2,
                'X'         : 0,
                'Y'         : 3,
                'SELECT'    : 8,
                'START'     : 9,
                'SH_LEFT'   : 4,
                'SH_RIGHT'  : 5,
                'AXIS_X'    : 3,
                'AXIS_Y'    : 4
            },
            'GPIO Controller 1' : {
                'A'         : 0,
                'B'         : 1,
                'X'         : 3,
                'Y'         : 4,
                'SELECT'    : 10,
                'START'     : 11,
                'SH_LEFT'   : 7,
                'SH_RIGHT'  : 6,
                'AXIS_X'    : 0,  # -1 = links, +1 = rechts
                'AXIS_Y'    : 1   # -1 = oben,  +1 = unten
            },
            'PLAYSTATION(R)3 Controller' : {
                'A'         : 13,   # circle
                'B'         : 14,   # cross
                'X'         : 12,   # triangle
                'Y'         : 15,   # square
                'SELECT'    : 0,
                'START'     : 3,
                'SH_LEFT'   : 10,   # L1
                'SH_RIGHT'  : 11,   # R1
                'AXIS_X'    : 0,  # -1 = links, +1 = rechts
                'AXIS_Y'    : 1   # -1 = oben,  +1 = unten
            },
            'Keyboard Stick' : {
                'A'         : 0,   # circle
                'B'         : 1,   # cross
                'X'         : 2,   # triangle
                'Y'         : 3,   # square
                'SELECT'    : 4,
                'START'     : 5,
                'SH_LEFT'   : 6,   # L1
                'SH_RIGHT'  : 7,   # R1
                'AXIS_X'    : 0,  # -1 = links, +1 = rechts
                'AXIS_Y'    : 1   # -1 = oben,  +1 = unten
            },
            'Mouse Stick': {
                'A': 0,  # circle
                'B': 1,  # cross
                'X': 2,  # triangle
                'Y': 3,  # square
                'SELECT': 4,
                'START': 5,
                'SH_LEFT': 6,  # L1
                'SH_RIGHT': 7,  # R1
                'AXIS_X': 0,  # -1 = links, +1 = rechts
                'AXIS_Y': 1  # -1 = oben,  +1 = unten
            },
        }

usb_gamepad_linux_mapping = {'A'        : 1,
                            'B'         : 2,
                            'X'         : 0,
                            'Y'         : 3,
                            'SELECT'    : 8,
                            'START'     : 9,
                            'SH_LEFT'   : 4,
                            'SH_RIGHT'  : 5,
                            'AXIS_X'    : 0,
                            'AXIS_Y'    : 1}

keyboard_mappings = {
            'Default' : {               # Matches best to the layout of Waveshare Game HAT
                'Buttons' : [
                    pg.K_RIGHT,         # A
                    pg.K_DOWN,          # B
                    pg.K_UP,            # X
                    pg.K_LEFT,          # Y
                    pg.K_RETURN,        # SELECT
                    pg.K_SPACE,         # START
                    pg.K_q,             # SH_LEFT
                    pg.K_e,             # SH_RIGHT
                ],
                'Axis' : [
                    (pg.K_a, pg.K_d),   # X-Axis
                    (pg.K_w, pg.K_s)    # Y-Axis
                ]
            },
            'Alt1' : {                  # Matches logically fine for using cursor keys for directions
                'Buttons': [
                    pg.K_d,             # A
                    pg.K_s,             # B
                    pg.K_w,             # X
                    pg.K_a,             # Y
                    pg.K_RETURN,        # SELECT
                    pg.K_SPACE,         # START
                    pg.K_q,             # SH_LEFT
                    pg.K_e,             # SH_RIGHT
                ],
                'Axis': [
                    (pg.K_LEFT, pg.K_RIGHT),  # X-Axis
                    (pg.K_UP, pg.K_DOWN)  # Y-Axis
                ]
            }
}

mouse_keyboard_mappings = {
            'Default' : {               #
                'Buttons' : [
                    pg.K_d,             # A
                    pg.K_s,             # B
                    pg.K_w,             # X
                    pg.K_a,             # Y
                    pg.K_RETURN,        # SELECT
                    pg.K_SPACE,         # START
                    pg.K_q,             # SH_LEFT
                    pg.K_e,             # SH_RIGHT
                ],
                'Axis' : [
                    None,  # X-Axis
                    None   # Y-Axis
                ]
            }
}


# Joystick without any operation
# Use this if you do not find a Joystick.
class NoStick():
    def get_name(self):
        return 'No Stick'
    def get_button(self, btn):
        return False
    def get_axis(self, axis):
        return 0

# get keyboard mappings
def getKeyboardMappingNames():
    return keyboard_mappings.keys()

# get keyboard mappings
def getMouseKeyboardMappingNames():
    return mouse_keyboard_mappings.keys()

# Keyboard-Joystick replacement
# Use this to simulate Joystick on KeyboardInterrupt.
# keep in mind: there are no Joystick-events for this "Joystick"
#
# Mousemode is intended to add regular buttons besides the mouse control
class _DummyStick:
    def __init__(self, mapping = 'Default', name = 'Dummy'):
        self._name = name
        self.set_mapping(mapping)

    def set_mapping(self, mapping):
        self._mapping = mapping
        self._apply_mapping()

    def _apply_mapping(self):
        pass                    # do in subclass

    def get_mapping(self):
        return self._mapping

    def get_name(self):
        return self._name

    def get_button(self, btn):
        if btn is None:
            return False

        keys = pg.key.get_pressed()
        return keys[self._buttons[btn]]

    def get_axis(self, axis):
        if axis is None:
            return 0
        if self._axis[axis] is None:
            return 0

        #print('get_axis {0}'.format(axis))
        if axis is None:
            return 0
        keys = pg.key.get_pressed()
        #print('get_axis - keys: {0}'.format(keys))
        val = 0
        pos1 = keys[self._axis[axis][0]]
        pos2 = keys[self._axis[axis][1]]
        if pos1 and not pos2:
            val = -1
        elif pos2 and not pos1:
            val = 1
        return val

class KeyboardStick(_DummyStick):

    def __init__(self, mapping = 'Default'):
        _DummyStick.__init__(self, mapping, 'Keyboard Stick')

    def _apply_mapping(self):
        self._buttons = keyboard_mappings[self._mapping]['Buttons']
        self._axis = keyboard_mappings[self._mapping]['Axis']


class MouseAddOnStick(_DummyStick):

    def __init__(self, mapping = 'Default'):
        _DummyStick.__init__(self, mapping, 'Mouse Stick')

    def _apply_mapping(self):
        self._buttons = mouse_keyboard_mappings[self._mapping]['Buttons']
        self._axis = mouse_keyboard_mappings[self._mapping]['Axis']


# Joystick-Pin-mapping
# Encapsulates different Joystick-Button-Numberings.
# Pass the pygame-Joystick to __init__ => the Pin-Mapping should be matched.
# Pass None as Joystick to get a dummy without function.
# Pass a KeyboardStick-object to get a simulation via keyboard
# Pass a MouseAddOnStick-object to get a simulation via keyboard for non-mouse-buttons
class JoystickPins():
    def __init__(self, joystick, mapping = None):
        self.no_stick = joystick is None
        if self.no_stick:
            self.joystick = NoStick()
        else:
            self.joystick = joystick

        self.name = joystick.get_name().strip()
        if mapping is not None:
            self.mapping = mapping
        elif self.name == 'USB Gamepad' and 'Linux' in platform.system():
            print("Linux mapping")
            self.mapping = usb_gamepad_linux_mapping
        elif self.name in joystick_mappings.keys():
            self.mapping = joystick_mappings[self.name]
        else:
            self.mapping = {}
        #print(self.mapping)

        self._A = self.mapping.get('A')
        self._B = self.mapping.get('B')
        self._X = self.mapping.get('X')
        self._Y = self.mapping.get('Y')
        self._select = self.mapping.get('SELECT')
        self._start  = self.mapping.get('START')
        self._shoulder_left  = self.mapping.get('SH_LEFT')
        self._shoulder_right = self.mapping.get('SH_RIGHT')
        self._axis_x = self.mapping.get('AXIS_X')
        self._axis_y = self.mapping.get('AXIS_Y')

    def get_name(self):
        return self.name

    def A(self):
        return self._A
    def B(self):
        return self._B
    def X(self):
        return self._X
    def Y(self):
        return self._Y
    def select(self):
        return self._select
    def start(self):
        return self._start
    def shoulder_left(self):
        return self._shoulder_left
    def shoulder_right(self):
        return self._shoulder_right
    def axis_x(self):
        return self._axis_x
    def axis_y(self):
        return self._axis_y

    def get_button(self, idx):
        return self.joystick.get_button(idx)

    def get_A(self):
        return self.joystick.get_button(self._A)
    def get_B(self):
        return self.joystick.get_button(self._B)
    def get_X(self):
        return self.joystick.get_button(self._X)
    def get_Y(self):
        return self.joystick.get_button(self._Y)
    def get_select(self):
        return self.joystick.get_button(self._select)
    def get_start(self):
        return self.joystick.get_button(self._start)
    def get_shoulder_left(self):
        return self.joystick.get_button(self._shoulder_left)
    def get_shoulder_right(self):
        return self.joystick.get_button(self._shoulder_right)

    def get_axis(self, axis):
        val = self.joystick.get_axis(axis)
        result = 0
        if val < -0.9:
            result = -1
        elif val > 0.9:
            result = 1
        return result

    def get_axis_left(self):
        return self.joystick.get_axis(self._axis_x) < -0.9
    def get_axis_right(self):
        return self.joystick.get_axis(self._axis_x) >  0.9
    def get_axis_up(self):
        return self.joystick.get_axis(self._axis_y) < -0.9
    def get_axis_down(self):
        return self.joystick.get_axis(self._axis_y) >  0.9

    def get_axis_x(self):
        val = self.get_axis(self._axis_x)
    def get_axis_y(self):
        val = self.get_axis(self._axis_y)