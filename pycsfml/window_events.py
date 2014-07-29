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

from warnings import warn as _warn


class Event(object):
    CLOSED = _sf.sfEvtClosed
    RESIZED = _sf.sfEvtResized
    LOST_FOCUS = _sf.sfEvtLostFocus
    GAINED_FOCUS = _sf.sfEvtGainedFocus
    TEXT_ENTERED = _sf.sfEvtTextEntered
    KEY_PRESSED = _sf.sfEvtKeyPressed
    KEY_RELEASED = _sf.sfEvtKeyReleased
    MOUSE_WHEEL_MOVED = _sf.sfEvtMouseWheelMoved
    MOUSE_BUTTON_PRESSED = _sf.sfEvtMouseButtonPressed
    MOUSE_BUTTON_RELEASED = _sf.sfEvtMouseButtonReleased
    MOUSE_MOVED = _sf.sfEvtMouseMoved
    MOUSE_ENTERED = _sf.sfEvtMouseEntered
    MOUSE_LEFT = _sf.sfEvtMouseLeft
    JOYSTICK_BUTTON_PRESSED = _sf.sfEvtJoystickButtonPressed
    JOYSTICK_BUTTON_RELEASED = _sf.sfEvtJoystickButtonReleased
    JOYSTICK_MOVED = _sf.sfEvtJoystickMoved
    JOYSTICK_CONNECTED = _sf.sfEvtJoystickConnected
    JOYSTICK_DISCONNECTED = _sf.sfEvtJoystickDisconnected

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return type(self).__name__+'()'

    def __eq__(self, other):
        try:
            r = isinstance(self, other)
            _warn("Do not use == to check for event type. That is hacky. Use isinstance instead.")
            return r
        except TypeError:
            return False

    @staticmethod
    def _wrap(sf_ptr):
        event_cls = _type_to_class[sf_ptr.type]
        try:
            struct_cls = event_cls._struct_cls
        except AttributeError:
            return event_cls()
        event = object.__new__(event_cls)
        event._sf_event = sf_ptr
        sf_ptr = getattr(sf_ptr, event_cls._struct_member)
        setattr(event, '_sf'+struct_cls.__name__, sf_ptr)
        return event

class CloseEvent(Event):
    def __init__(self):
        Event.__init__(self, Event.CLOSED)


class SizeEvent(base.SFMLStruct, Event):
    def __init__(self, width, height):
        self._sfSizeEvent = _ffi.new('sfSizeEvent*')
        Event.__init__(self, Event.RESIZED)
        self.width = width
        self.height = height

    @property
    def type(self):
        return self._sfSizeEvent.type
    @type.setter
    def type(self, value):
        self._sfSizeEvent.type = value

    @property
    def width(self):
        return self._sfSizeEvent.width
    @width.setter
    def width(self, value):
        self._sfSizeEvent.width = value

    @property
    def height(self):
        return self._sfSizeEvent.height
    @height.setter
    def height(self, value):
        self._sfSizeEvent.height = value

    def __repr__(self):
        return self._repr('width= height=')
ResizeEvent = SizeEvent


class FocusEvent(Event):
    pass

class FocusGainEvent(FocusEvent):
    gained = True
    lost = False
    def __init__(self):
        FocusEvent.__init__(self, Event.GAINED_FOCUS)

class FocusLossEvent(FocusEvent):
    gained = False
    lost = True
    def __init__(self):
        FocusEvent.__init__(self, Event.LOST_FOCUS)

try:
    _unichr = unichr
except NameError:
    _unichr = chr

class TextEvent(base.SFMLStruct, Event):
    def __init__(self, unicode):
        self._sfTextEvent = _ffi.new('sfTextEvent*')
        Event.__init__(self, Event.TEXT_ENTERED)
        self.unicode = unicode

    @property
    def type(self):
        return self._sfTextEvent.type
    @type.setter
    def type(self, value):
        self._sfTextEvent.type = value

    @property
    def unicode(self):
        return self._sfTextEvent.unicode
    @unicode.setter
    def unicode(self, value):
        self._sfTextEvent.unicode = value

    @property
    def character(self):
        return _unichr(self.unicode)

    def __repr__(self):
        return '{}(ord({!r}))'.format(type(self).__name__, self.character)


class KeyEvent(base.SFMLStruct, Event):
    def __init__(self, type, code, alt, control, shift, system):
        self._sfKeyEvent = _ffi.new('sfKeyEvent*')
        Event.__init__(self, type)
        self.code = code
        self.alt = alt
        self.control = control
        self.shift = shift
        self.system = system

    @property
    def type(self):
        return self._sfKeyEvent.type
    @type.setter
    def type(self, value):
        self._sfKeyEvent.type = value

    @property
    def code(self):
        return self._sfKeyEvent.code
    @code.setter
    def code(self, value):
        self._sfKeyEvent.code = value

    @property
    def alt(self):
        return self._sfKeyEvent.alt
    @alt.setter
    def alt(self, value):
        self._sfKeyEvent.alt = value

    @property
    def control(self):
        return self._sfKeyEvent.control
    @control.setter
    def control(self, value):
        self._sfKeyEvent.control = value

    @property
    def shift(self):
        return self._sfKeyEvent.shift
    @shift.setter
    def shift(self, value):
        self._sfKeyEvent.shift = value

    @property
    def system(self):
        return self._sfKeyEvent.system
    @system.setter
    def system(self, value):
        self._sfKeyEvent.system = value

    def __repr__(self):
        return self._repr('code= alt= control= shift= system=')

class KeyPressEvent(KeyEvent):
    pressed = True
    released = False
    def __init__(self, code, alt, control, shift, system):
        KeyEvent.__init__(self, Event.KEY_PRESSED, code, alt, control, shift, system)

class KeyReleaseEvent(KeyEvent):
    pressed = False
    released = True
    def __init__(self, code, alt, control, shift, system):
        KeyEvent.__init__(self, Event.KEY_RELEASED, code, alt, control, shift, system)


class MouseWheelEvent(base.SFMLStruct, Event):
    def __init__(self, delta, x, y):
        self._sfMouseWheelEvent = _ffi.new('sfMouseWheelEvent*')
        Event.__init__(self, Event.MOUSE_WHEEL_MOVED)
        self.delta = delta
        self.x = x
        self.y = y

    @property
    def type(self):
        return self._sfMouseWheelEvent.type
    @type.setter
    def type(self, value):
        self._sfMouseWheelEvent.type = value

    @property
    def delta(self):
        return self._sfMouseWheelEvent.delta
    @delta.setter
    def delta(self, value):
        self._sfMouseWheelEvent.delta = value

    @property
    def x(self):
        return self._sfMouseWheelEvent.x
    @x.setter
    def x(self, value):
        self._sfMouseWheelEvent.x = value

    @property
    def y(self):
        return self._sfMouseWheelEvent.y
    @y.setter
    def y(self, value):
        self._sfMouseWheelEvent.y = value

    def __repr__(self):
        return self._repr('delta= x= y=')


class MouseButtonEvent(base.SFMLStruct, Event):
    def __init__(self, type, button, x, y):
        self._sfMouseButtonEvent = _ffi.new('sfMouseButtonEvent*')
        Event.__init__(self, type)
        self.button = button
        self.x = x
        self.y = y

    @property
    def type(self):
        return self._sfMouseButtonEvent.type
    @type.setter
    def type(self, value):
        self._sfMouseButtonEvent.type = value

    @property
    def button(self):
        return self._sfMouseButtonEvent.button
    @button.setter
    def button(self, value):
        self._sfMouseButtonEvent.button = value

    @property
    def x(self):
        return self._sfMouseButtonEvent.x
    @x.setter
    def x(self, value):
        self._sfMouseButtonEvent.x = value

    @property
    def y(self):
        return self._sfMouseButtonEvent.y
    @y.setter
    def y(self, value):
        self._sfMouseButtonEvent.y = value

    def __repr__(self):
        return self._repr('button= x= y=')

class MouseButtonPressEvent(MouseButtonEvent):
    pressed = True
    released = False
    def __init__(self, button, x, y):
        KeyEvent.__init__(self, Event.KEY_PRESSED, button, x, y)


class MouseButtonReleaseEvent(MouseButtonEvent):
    pressed = False
    released = True
    def __init__(self, button, x, y):
        KeyEvent.__init__(self, Event.KEY_RELEASED, button, x, y)


class MouseMoveEvent(base.SFMLStruct, Event):
    def __init__(self, x, y):
        self._sfMouseMoveEvent = _ffi.new('sfMouseMoveEvent*')
        Event.__init__(self, Event.MOUSE_MOVED)
        self.x = x
        self.y = y

    @property
    def type(self):
        return self._sfMouseMoveEvent.type
    @type.setter
    def type(self, value):
        self._sfMouseMoveEvent.type = value

    @property
    def x(self):
        return self._sfMouseMoveEvent.x
    @x.setter
    def x(self, value):
        self._sfMouseMoveEvent.x = value

    @property
    def y(self):
        return self._sfMouseMoveEvent.y
    @y.setter
    def y(self, value):
        self._sfMouseMoveEvent.y = value

    def __repr__(self):
        return self._repr('x= y=')


class MouseEvent(Event):
    pass

class MouseEnterEvent(MouseEvent):
    entered = True
    left = False
    def __init__(self):
        MouseEvent.__init__(self, Event.MOUSE_ENTERED)


class MouseLeaveEvent(MouseEvent):
    entered = False
    left = True
    def __init__(self):
        MouseEvent.__init__(self, Event.MOUSE_LEFT)


class JoystickButtonEvent(base.SFMLStruct, Event):
    def __init__(self, type, joystick_id, button):
        self._sfJoystickButtonEvent = _ffi.new('sfJoystickButtonEvent*')
        Event.__init__(self, type)
        self.joystick_id = joystick_id
        self.button = button

    @property
    def type(self):
        return self._sfJoystickButtonEvent.type
    @type.setter
    def type(self, value):
        self._sfJoystickButtonEvent.type = value

    @property
    def joystick_id(self):
        return self._sfJoystickButtonEvent.joystickId
    @joystick_id.setter
    def joystick_id(self, value):
        self._sfJoystickButtonEvent.joystickId = value

    @property
    def button(self):
        return self._sfJoystickButtonEvent.button
    @button.setter
    def button(self, value):
        self._sfJoystickButtonEvent.button = value

    def __repr__(self):
        return self._repr('joystick_id= button=')

class JoystickButtonPressEvent(JoystickButtonEvent):
    pressed = True
    released = False
    def __init__(self, joystick_id, button):
        JoystickButtonEvent.__init__(self, Event.JOYSTICK_BUTTON_PRESSED, joystick_id, button)

class JoystickButtonReleaseEvent(JoystickButtonEvent):
    pressed = False
    released = True
    def __init__(self, joystick_id, button):
        JoystickButtonEvent.__init__(self, Event.JOYSTICK_BUTTON_RELEASED, joystick_id, button)


class JoystickMoveEvent(base.SFMLStruct, Event):
    def __init__(self, joystick_id, axis, position):
        self._sfJoystickMoveEvent = _ffi.new('sfJoystickMoveEvent*')
        Event.__init__(self, Event.JOYSTICK_MOVED)
        self.joystick_id = joystick_id
        self.axis = axis
        self.position = position

    @property
    def type(self):
        return self._sfJoystickMoveEvent.type
    @type.setter
    def type(self, value):
        self._sfJoystickMoveEvent.type = value

    @property
    def joystick_id(self):
        return self._sfJoystickMoveEvent.joystickId
    @joystick_id.setter
    def joystick_id(self, value):
        self._sfJoystickMoveEvent.joystickId = value

    @property
    def axis(self):
        return self._sfJoystickMoveEvent.axis
    @axis.setter
    def axis(self, value):
        self._sfJoystickMoveEvent.axis = value

    @property
    def position(self):
        return self._sfJoystickMoveEvent.position
    @position.setter
    def position(self, value):
        self._sfJoystickMoveEvent.position = value

    def __repr__(self):
        return self._repr('joystick_id= axis= position=')


class JoystickConnectEvent(base.SFMLStruct, Event):
    def __init__(self, type, joystick_id):
        self._sfJoystickConnectEvent = _ffi.new('sfJoystickConnectEvent*')
        Event.__init__(self, type)
        self.joystick_id = joystick_id

    @property
    def type(self):
        return self._sfJoystickConnectEvent.type
    @type.setter
    def type(self, value):
        self._sfJoystickConnectEvent.type = value

    @property
    def joystick_id(self):
        return self._sfJoystickConnectEvent.joystickId
    @joystick_id.setter
    def joystick_id(self, value):
        self._sfJoystickConnectEvent.joystickId = value

    def __repr__(self):
        return self._repr('joystick_id=')

class JoystickConnectConnectEvent(JoystickConnectEvent):
    connected = True
    disconnected = False
    def __init__(self, joystick_id):
        JoystickConnectEvent.__init__(self, Event.JOYSTICK_CONNECTED, joystick_id)

class JoystickConnectDisconnectEvent(JoystickConnectEvent):
    connected = False
    disconnected = True
    def __init__(self, joystick_id):
        JoystickConnectEvent.__init__(self, Event.JOYSTICK_DISCONNECTED, joystick_id)





_type_to_class = {
    Event.CLOSED: CloseEvent,
    Event.RESIZED: ResizeEvent,
    Event.LOST_FOCUS: FocusLossEvent,
    Event.GAINED_FOCUS: FocusGainEvent,
    Event.TEXT_ENTERED: TextEvent,
    Event.KEY_PRESSED: KeyPressEvent,
    Event.KEY_RELEASED: KeyReleaseEvent,
    Event.MOUSE_WHEEL_MOVED: MouseWheelEvent,
    Event.MOUSE_BUTTON_PRESSED: MouseButtonPressEvent,
    Event.MOUSE_BUTTON_RELEASED: MouseButtonReleaseEvent,
    Event.MOUSE_MOVED: MouseMoveEvent,
    Event.MOUSE_ENTERED: MouseEnterEvent,
    Event.MOUSE_LEFT: MouseLeaveEvent,
    Event.JOYSTICK_BUTTON_PRESSED: JoystickButtonPressEvent,
    Event.JOYSTICK_BUTTON_RELEASED: JoystickButtonReleaseEvent,
    Event.JOYSTICK_MOVED: JoystickMoveEvent,
    Event.JOYSTICK_CONNECTED: JoystickConnectConnectEvent,
    Event.JOYSTICK_DISCONNECTED: JoystickConnectDisconnectEvent,
}

for event_cls in _type_to_class.values():
    if issubclass(event_cls, base.SFMLStruct):
        struct_cls = event_cls
        while not base.SFMLStruct in struct_cls.__bases__:
            (struct_cls,) = struct_cls.__bases__
        event_cls._struct_cls = struct_cls
        event_cls._struct_member = struct_cls.__name__[0].lower()+struct_cls.__name__[1:-5]



del base