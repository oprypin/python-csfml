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
from .graphics import _sf

from . import system as _system

from . import base
from .util import arg_error as _arg_error
from .graphics import Drawable, Transformable



class Shape(Drawable, Transformable):
    _sf_type = 'sfShape'
    def __init__(self, **kwargs):
        get_point_count = lambda _: self.get_point_count()
        self._get_point_count_callback = _ffi.callback('unsigned int(void*)', get_point_count)

        get_point = lambda i, _: _system.Vector2(self.get_point(i))._sfVector2f[0]
        self._get_point_callback = _ffi.callback('sfVector2f(unsigned int, void*)', get_point)

        self._sfShape = _sf.sfShape_create(self._get_point_count_callback, self._get_point_callback, _ffi.NULL)
        self._sfTransformable = self._sfShape
        if kwargs: self._set(**kwargs)

    def get_texture(self):
        result = getattr(_sf, self._sf_type+'_getTexture')(self._sfShape)
        return Texture._wrap_ptr(result)
    def set_texture(self, texture, reset_rect):
        try: texture = texture._sfTexture
        except AttributeError: _arg_error('texture', 'Texture')
        return getattr(_sf, self._sf_type+'_setTexture')(self._sfShape, texture, reset_rect)
    texture = property(get_texture, set_texture)

    def get_texture_rect(self):
        result = getattr(_sf, self._sf_type+'_getTextureRect')(self._sfShape)
        return Rect((result.left, result.top), (result.width, result.height))
    def set_texture_rect(self, rect):
        try: rect = rect._sfIntRect[0]
        except AttributeError: _arg_error('rect', 'Rect')
        return getattr(_sf, self._sf_type+'_setTextureRect')(self._sfShape, rect)
    texture_rect = texture_rectangle = property(get_texture_rect, set_texture_rect)

    def get_fill_color(self):
        result = getattr(_sf, self._sf_type+'_getFillColor')(self._sfShape)
        return Color._wrap_data(result)
    def set_fill_color(self, color):
        try: color = color._sfColor[0]
        except AttributeError: _arg_error('color', 'Color')
        return getattr(_sf, self._sf_type+'_setFillColor')(self._sfShape, color)
    fill_color = property(get_fill_color, set_fill_color)

    def get_outline_color(self):
        result = getattr(_sf, self._sf_type+'_getOutlineColor')(self._sfShape)
        return Color._wrap_data(result)
    def set_outline_color(self, color):
        try: color = color._sfColor[0]
        except AttributeError: _arg_error('color', 'Color')
        return getattr(_sf, self._sf_type+'_setOutlineColor')(self._sfShape, color)
    outline_color = property(get_outline_color, set_outline_color)

    def get_outline_thickness(self):
        return getattr(_sf, self._sf_type+'_getOutlineThickness')(self._sfShape)
    def set_outline_thickness(self, thickness):
        return getattr(_sf, self._sf_type+'_setOutlineThickness')(self._sfShape, thickness)
    outline_thickness = property(get_outline_thickness, set_outline_thickness)



    def get_point_count(self):
        return getattr(_sf, self._sf_type+'_getPointCount')(self._sfShape)
    @property
    def point_count(self):
        return self.get_point_count()

    def get_point(self, index):
        result = getattr(_sf, self._sf_type+'_getPoint')(self._sfShape, index)
        return _system.Vector2(result.x, result.y)

    def get_local_bounds(self):
        result = getattr(_sf, self._sf_type+'_getLocalBounds')(self._sfShape)
        return Rect((result.left, result.top), (result.width, result.height))
    local_bounds = property(get_local_bounds)

    def get_global_bounds(self):
        result = getattr(_sf, self._sf_type+'_getGlobalBounds')(self._sfShape)
        return Rect((result.left, result.top), (result.width, result.height))
    global_bounds = property(get_global_bounds)

    def update(self):
        return _sf.sfShape_update(self._sfShape)


    def draw(self, target, states):
        try: starget = getattr(target, '_'+target._sf_type)
        except AttributeError: _arg_error('target', 'RenderTarget')
        try: states = states._sfRenderStates
        except AttributeError: _arg_error('states', 'RenderStates')
        return getattr(_sf, target._sf_type+'_draw'+self._sf_type[2:])(starget, self._sfShape, states)




class CircleShape(Shape):
    _sf_type = 'sfCircleShape'
    def __init__(self, radius=0, point_count=30, **kwargs):
        self._sfCircleShape = _sf.sfCircleShape_create()
        self._sfTransformable = self._sfShape = self._sfCircleShape
        self.radius = radius
        self.point_count = point_count
        if kwargs: self._set(**kwargs)

    def get_radius(self):
        return _sf.sfCircleShape_getRadius(self._sfCircleShape)
    def set_radius(self, radius):
        return _sf.sfCircleShape_setRadius(self._sfCircleShape, radius)
    radius = property(get_radius, set_radius)

    def set_point_count(self, count):
        return _sf.sfCircleShape_setPointCount(self._sfCircleShape, count)
    point_count = property(Shape.get_point_count, set_point_count)


class RectangleShape(Shape):
    _sf_type = 'sfRectangleShape'
    def __init__(self, size=(0, 0), **kwargs):
        self._sfRectangleShape = _sf.sfRectangleShape_create()
        self._sfTransformable = self._sfShape = self._sfRectangleShape
        self.size = size
        if kwargs: self._set(**kwargs)

    def get_size(self):
        result = _sf.sfRectangleShape_getSize(self._sfRectangleShape)
        return _system.Vector2(result.x, result.y)
    def set_size(self, size):
        size = _system.Vector2(size)._sfVector2f[0]
        return _sf.sfRectangleShape_setSize(self._sfRectangleShape, size)
    size = property(get_size, set_size)


class ConvexShape(Shape):
    _sf_type = 'sfConvexShape'
    def __init__(self, **kwargs):
        self._sfConvexShape = _sf.sfConvexShape_create()
        self._sfTransformable = self._sfShape = self._sfConvexShape
        if kwargs: self._set(**kwargs)

    def get_point_count(self):
        return _sf.sfConvexShape_getPointCount(self._sfConvexShape)
    def set_point_count(self, count):
        return _sf.sfConvexShape_setPointCount(self._sfConvexShape, count)
    point_count = property(get_point_count, set_point_count)

    def get_point(self, index):
        result = _sf.sfConvexShape_getPoint(self._sfConvexShape, index)
        return _system.Vector2(result.x, result.y)
    def set_point(self, index, point):
        point = _system.Vector2(point)._sfVector2f[0]
        return _sf.sfConvexShape_setPoint(self._sfConvexShape, index, point)

