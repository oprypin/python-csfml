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
_sf = _ffi.dlopen('libcsfml-window.so')

from . import system as _system

from . import base
from .util import arg_error as _arg_error, FakeCallableInt as _FakeCallableInt

from itertools import islice as _islice
from warnings import warn as _warn


class Style(base.SFMLEnum):
    NONE = _sf.sfNone
    TITLEBAR = _sf.sfTitlebar
    RESIZE = _sf.sfResize
    CLOSE = _sf.sfClose
    FULLSCREEN = _sf.sfFullscreen
    DEFAULT = _sf.sfDefaultStyle


class ContextSettings(base.SFMLStruct):
    def __init__(self, depth=0, stencil=0, antialiasing=0, major=2, minor=0, **kwargs):
        self._sfContextSettings = _ffi.new('sfContextSettings*')
        if antialiasing and not depth:
            _warn("Antialiasing may not work if depth is not set")
        self.depth_bits = depth
        self.stencil_bits = stencil
        self.antialiasing_level = antialiasing
        self.major_version = major
        self.minor_version = minor
        if kwargs: self._set(**kwargs)

    @property
    def depth_bits(self):
        return self._sfContextSettings.depthBits
    @depth_bits.setter
    def depth_bits(self, value):
        self._sfContextSettings.depthBits = value

    @property
    def stencil_bits(self):
        return self._sfContextSettings.stencilBits
    @stencil_bits.setter
    def stencil_bits(self, value):
        self._sfContextSettings.stencilBits = value

    @property
    def antialiasing_level(self):
        return self._sfContextSettings.antialiasingLevel
    @antialiasing_level.setter
    def antialiasing_level(self, value):
        self._sfContextSettings.antialiasingLevel = value

    @property
    def major_version(self):
        return self._sfContextSettings.majorVersion
    @major_version.setter
    def major_version(self, value):
        self._sfContextSettings.majorVersion = value

    @property
    def minor_version(self):
        return self._sfContextSettings.minorVersion
    @minor_version.setter
    def minor_version(self, value):
        self._sfContextSettings.minorVersion = value

    def __repr__(self):
        return self._repr('depth_bits= stencil_bits= antialiasing_level= major_version= minor_version=')

class GlResource(object):
    pass


class Window(base.SFMLClass, GlResource):
    def __init__(self, mode, title, style=Style.DEFAULT, settings=ContextSettings(), **kwargs):
        try: mode = mode._sfVideoMode[0]
        except AttributeError: _arg_error('mode', 'VideoMode')
        title = [ord(c) for c in title]+[0]
        try: settings = settings._sfContextSettings
        except AttributeError: _arg_error('settings', 'ContextSettings')
        self._sfWindow = _sf.sfWindow_createUnicode(mode, title, style, settings)
        if kwargs: self._set(**kwargs)
        self.on_create()
    
    @classmethod
    def from_handle(cls, handle, settings=ContextSettings()):
        try: settings = settings._sfContextSettings
        except AttributeError: _arg_error('settings', 'ContextSettings')
        result = _sf.sfWindow_createFromHandle(handle, settings)
        result = cls._wrap_ptr(result)
        result.on_create()
        return result
    
    def create(self, *args, **kwargs):
        self.__del__()
        self.__init__(*args, **kwargs)
    recreate = create
    def create_from_handle(self, *args, **kwargs):
        self.__del__()
        self._sfWindow = self.from_handle(*args, **kwargs)._sfWindow
    recreate_from_handle = create_from_handle

    def __del__(self):
        if self._sf_owned: _sf.sfWindow_destroy(self._sfWindow)
    
    def close(self):
        _sf.sfWindow_close(self._sfWindow)
    
    def is_open(self):
        return _sf.sfWindow_isOpen(self._sfWindow)
    is_open = property(is_open)
    
    def get_settings(self):
        result = _sf.sfWindow_getSettings(self._sfWindow)
        return ContextSettings._wrap_data(result)
    settings = property(get_settings)
    
    def poll_event(self):
        event = _ffi.new('sfEvent*')
        if _sf.sfWindow_pollEvent(self._sfWindow, event):
            if event.type==Event.RESIZED:
                self.on_resize()
            return Event._wrap(event)
    @property
    def events(self):
        return iter(self.poll_event, None)

    def wait_event(self):
        event = _ffi.new('sfEvent*')
        if _sf.sfWindow_waitEvent(self._sfWindow, event):
            if event.type==Event.RESIZED:
                self.on_resize()
            return Event._wrap(event)

    def get_position(self):
        result = _sf.sfWindow_getPosition(self._sfWindow)
        return _system.Vector2(result.x, result.y)
    def set_position(self, position):
        position = _system.Vector2(position)._sfVector2i[0]
        _sf.sfWindow_setPosition(self._sfWindow, position)
    position = property(get_position, set_position)
    
    def get_size(self):
        result = _sf.sfWindow_getSize(self._sfWindow)
        return _system.Vector2(result.x, result.y)
    def set_size(self, size):
        size = _system.Vector2(size)._sfVector2u[0]
        _sf.sfWindow_setSize(self._sfWindow, size)
    size = property(get_size, set_size)

    def set_title(self, title):
        title = [ord(c) for c in title]+[0]
        _sf.sfWindow_setUnicodeTitle(self._sfWindow, title)
    title = property(fset=set_title)
    
    def set_icon(self, pixels):
        _sf.sfWindow_setIcon(self._sfWindow, pixels.width, pixels.height, pixels.data)
    icon = property(fset=set_icon)
    
    def set_visible(self, visible):
        _sf.sfWindow_setVisible(self._sfWindow, visible)
    visible = property(fset=set_visible)
    def show(self):
        self.visible = True
    def hide(self):
        self.visible = False
    
    def set_mouse_cursor_visible(self, visible):
        _sf.sfWindow_setMouseCursorVisible(self._sfWindow, visible)
    mouse_cursor_visible = property(fset=set_mouse_cursor_visible)
    
    def set_vertical_sync_enabled(self, enabled):
        _sf.sfWindow_setVerticalSyncEnabled(self._sfWindow, enabled)
    vertical_sync_enabled = vertical_synchronization = property(fset=set_vertical_sync_enabled)
    
    def set_key_repeat_enabled(self, enabled):
        _sf.sfWindow_setKeyRepeatEnabled(self._sfWindow, enabled)
    key_repeat_enabled = property(fset=set_key_repeat_enabled)
    
    def set_active(self, active):
        return _sf.sfWindow_setActive(self._sfWindow, active)
    active = property(fset=set_active)
    
    def display(self):
        _sf.sfWindow_display(self._sfWindow)
    
    def set_framerate_limit(self, limit):
        _sf.sfWindow_setFramerateLimit(self._sfWindow, limit)
    framerate_limit = property(fset=set_framerate_limit)
    
    def set_joystick_threshold(self, threshold):
        _sf.sfWindow_setJoystickThreshold(self._sfWindow, threshold)
    joystick_threshold = property(fset=set_joystick_threshold)
    
    def get_system_handle(self):
        _sf.sfWindow_getSystemHandle(self._sfWindow)
    system_handle = property(get_system_handle)

    def on_create(self):
        pass
    def on_resize(self):
        pass


class VideoMode(base.SFMLStruct):
    def __init__(self, width, height, bits_per_pixel=32):
        self._sfVideoMode = _ffi.new('sfVideoMode*')
        self.width = width
        self.height = height
        self.bits_per_pixel = bits_per_pixel
    
    @property
    def width(self):
        return self._sfVideoMode.width
    @width.setter
    def width(self, value):
        self._sfVideoMode.width = value
    
    @property
    def height(self):
        return self._sfVideoMode.height
    @height.setter
    def height(self, value):
        self._sfVideoMode.height = value

    @property
    def size(self):
        return _system.Vector2(self.width, self.height)
    @size.setter
    def size(self, value):
        self.width, self.height = value
    
    @property
    def bits_per_pixel(self):
        return self._sfVideoMode.bitsPerPixel
    @bits_per_pixel.setter
    def bits_per_pixel(self, value):
        self._sfVideoMode.bitsPerPixel = value
    bpp = bits_per_pixel
    
    def __repr__(self):
        return self._repr('width= height= bits_per_pixel=')

    @classmethod
    def get_desktop_mode(cls):
        result = _sf.sfVideoMode_getDesktopMode()
        return cls._wrap_data(result)
    
    @classmethod
    def get_fullscreen_modes(cls, count=150):
        array = _sf.sfVideoMode_getFullscreenModes(_ffi.new('int*', count))
        for i in range(count):
            el = array[i]
            if not (0<el.bitsPerPixel<=128 and 64<=el.width<=0x8000 and 64<=el.height<=0x8000):
                break
            yield cls._wrap_ptr(el)
        else:
            for el in _itertools._islice(cls.get_fullscreen_modes(count*2), count, None):
                yield el
    
    def is_valid(self):
        result = _sf.sfVideoMode_isValid(self._sfVideoMode[0])
        return _FakeCallableInt(result)
    is_valid = property(is_valid)


class Context(base.SFMLClass, GlResource):
    def __init__(self):
        self._sfContext = _sf.sfContext_create()

    def __del__(self):
        if self._sf_owned: _sf.sfContext_destroy(self._sfContext)

    def set_active(self, active):
        _sf.sfContext_setActive(self._sfContext, active)
    active = property(fset=set_active)
    def activate(self):
        self.set_active(True)
    def deactivate(self):
        self.set_active(False)


from .window_events import *
from .window_devices import *


del base