# PyCSFML - Python bindings for SFML
# Copyright (c) 2014, Oleh Prypin <blaxpirit@gmail.com>
#
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.


from __future__ import division, absolute_import, print_function

from .ffi import ffi as _ffi
from .window import _sf

from . import base



class Keyboard(base.SFMLClass):
    UNKNOWN = _sf.sfKeyUnknown
    A = _sf.sfKeyA; B = _sf.sfKeyB; C = _sf.sfKeyC; D = _sf.sfKeyD; E = _sf.sfKeyE; F = _sf.sfKeyF; G = _sf.sfKeyG
    H = _sf.sfKeyH; I = _sf.sfKeyI; J = _sf.sfKeyJ; K = _sf.sfKeyK; L = _sf.sfKeyL; M = _sf.sfKeyM; N = _sf.sfKeyN
    O = _sf.sfKeyO; P = _sf.sfKeyP; Q = _sf.sfKeyQ; R = _sf.sfKeyR; S = _sf.sfKeyS; T = _sf.sfKeyT; U = _sf.sfKeyU
    V = _sf.sfKeyV; W = _sf.sfKeyW; X = _sf.sfKeyX; Y = _sf.sfKeyY; Z = _sf.sfKeyZ
    NUM0 = _sf.sfKeyNum0; NUM1 = _sf.sfKeyNum1; NUM2 = _sf.sfKeyNum2; NUM3 = _sf.sfKeyNum3; NUM4 = _sf.sfKeyNum4
    NUM5 = _sf.sfKeyNum5; NUM6 = _sf.sfKeyNum6; NUM7 = _sf.sfKeyNum7; NUM8 = _sf.sfKeyNum8; NUM9 = _sf.sfKeyNum9
    ESCAPE = _sf.sfKeyEscape
    L_CONTROL = _sf.sfKeyLControl; L_SHIFT = _sf.sfKeyLShift; L_ALT = _sf.sfKeyLAlt; L_SYSTEM = _sf.sfKeyLSystem
    R_CONTROL = _sf.sfKeyRControl; R_SHIFT = _sf.sfKeyRShift; R_ALT = _sf.sfKeyRAlt; R_SYSTEM = _sf.sfKeyRSystem
    MENU = _sf.sfKeyMenu
    L_BRACKET = _sf.sfKeyLBracket; R_BRACKET = _sf.sfKeyRBracket
    SEMI_COLON = _sf.sfKeySemiColon
    COMMA = _sf.sfKeyComma
    PERIOD = _sf.sfKeyPeriod
    QUOTE = _sf.sfKeyQuote
    SLASH = _sf.sfKeySlash
    BACK_SLASH = _sf.sfKeyBackSlash
    TILDE = _sf.sfKeyTilde
    EQUAL = _sf.sfKeyEqual
    DASH = _sf.sfKeyDash
    SPACE = _sf.sfKeySpace
    RETURN = _sf.sfKeyReturn
    BACK = _sf.sfKeyBack
    TAB = _sf.sfKeyTab
    PAGE_UP = _sf.sfKeyPageUp; PAGE_DOWN = _sf.sfKeyPageDown
    END = _sf.sfKeyEnd; HOME = _sf.sfKeyHome
    INSERT = _sf.sfKeyInsert; DELETE = _sf.sfKeyDelete
    ADD = _sf.sfKeyAdd; SUBTRACT = _sf.sfKeySubtract; MULTIPLY = _sf.sfKeyMultiply; DIVIDE = _sf.sfKeyDivide
    LEFT = _sf.sfKeyLeft; RIGHT = _sf.sfKeyRight; UP = _sf.sfKeyUp; DOWN = _sf.sfKeyDown
    NUMPAD0 = _sf.sfKeyNumpad0; NUMPAD1 = _sf.sfKeyNumpad1; NUMPAD2 = _sf.sfKeyNumpad2; NUMPAD3 = _sf.sfKeyNumpad3
    NUMPAD4 = _sf.sfKeyNumpad4; NUMPAD5 = _sf.sfKeyNumpad5; NUMPAD6 = _sf.sfKeyNumpad6; NUMPAD7 = _sf.sfKeyNumpad7
    NUMPAD8 = _sf.sfKeyNumpad8; NUMPAD9 = _sf.sfKeyNumpad9
    F1 = _sf.sfKeyF1; F2 = _sf.sfKeyF2; F3 = _sf.sfKeyF3; F4 = _sf.sfKeyF4; F5 = _sf.sfKeyF5
    F6 = _sf.sfKeyF6; F7 = _sf.sfKeyF7; F8 = _sf.sfKeyF8; F9 = _sf.sfKeyF9; F10 = _sf.sfKeyF10
    F11 = _sf.sfKeyF11; F12 = _sf.sfKeyF12; F13 = _sf.sfKeyF13; F14 = _sf.sfKeyF14; F15 = _sf.sfKeyF15
    PAUSE = _sf.sfKeyPause
    KEY_COUNT = _sf.sfKeyCount

    @staticmethod
    def is_key_pressed(key):
        return _sf.sfKeyboard_isKeyPressed(key)


class Mouse(base.SFMLClass):
    LEFT = _sf.sfMouseLeft
    RIGHT = _sf.sfMouseRight
    MIDDLE = _sf.sfMouseMiddle
    X_BUTTON1 = _sf.sfMouseXButton1
    X_BUTTON2 = _sf.sfMouseXButton2
    BUTTON_COUNT = _sf.sfMouseButtonCount

    def is_button_pressed(self, button):
        return _sf.sfMouse_isButtonPressed(button)

    @staticmethod
    def get_position(relative_to=None):
        if relative_to is None:
            relative_to = _ffi.NULL
        try:
            relative_to = relative_to._sfWindow
        except AttributeError:
            try:
                relative_to = relative_to._sfRenderWindow
            except AttributeError:
                _arg_error('relative_to', 'Window')
            else:
                result = _sf.sfMouse_getPositionRenderWindow(relative_to)
        else:
            result = _sf.sfMouse_getPosition(relative_to)
        return _system.Vector2(result.x, result.y)

    @staticmethod
    def set_position(position, relative_to=None):
        position = _system.Vector2(position)._sfVector2i[0]
        if relative_to is None:
            relative = _ffi.NULL
        try:
            relative_to = relative_to._sfWindow
        except AttributeError:
            try:
                relative_to = relative_to._sfRenderWindow
            except AttributeError:
                _arg_error('relative_to', 'Window')
            else:
                _sf.sfMouse_setPositionRenderWindow(position, relative_to)
        else:
            _sf.sfMouse_setPosition(position, relative_to)

class Joystick(base.SFMLClass):
    COUNT = _sf.sfJoystickCount
    BUTTON_COUNT = _sf.sfJoystickButtonCount
    AXIS_COUNT = _sf.sfJoystickAxisCount

    X = _sf.sfJoystickX
    Y = _sf.sfJoystickY
    Z = _sf.sfJoystickZ
    R = _sf.sfJoystickR
    U = _sf.sfJoystickU
    V = _sf.sfJoystickV
    POV_X = _sf.sfJoystickPovX
    POV_Y = _sf.sfJoystickPovY

    @staticmethod
    def is_connected(joystick):
        return _sf.sfJoystick_isConnected(joystick)

    @staticmethod
    def get_button_count(joystick):
        return _sf.sfJoystick_getButtonCount(joystick)

    @staticmethod
    def has_axis(joystick, axis):
        return _sf.sfJoystick_hasAxis(joystick, axis)

    @staticmethod
    def is_button_pressed(joystick, button):
        return _sf.sfJoystick_isButtonPressed(joystick, button)

    @staticmethod
    def get_axis_position(joystick, axis):
        return _sf.sfJoystick_getAxisPosition(joystick, axis)

    @staticmethod
    def update():
        _sf.sfJoystick_update()