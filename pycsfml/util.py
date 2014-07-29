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


class BaseVector(object):
    def __eq__(self, other):
        return all(a==b for a, b in zip(self, other))
    def __ne__(self, other):
        return any(a!=b for a, b in zip(self, other))

    def __add__(self, other):
        return type(self)(a+b for a, b in zip(self, other))
    def __sub__(self, other):
        return type(self)(a-b for a, b in zip(self, other))
    def __mul__(self, x):
        return type(self)(i*x for i in self)
    def __truediv__(self, x):
        return type(self)(i/x for i in self)
    __div__ = __truediv__
    def __floordiv__(self, x):
        return type(self)(i//x for i in self)

    def __neg__(self):
        return type(self)(-i for i in self)

    def __abs__(self):
        return sum(i**2 for i in self)**0.5

    def __repr__(self):
        return type(self).__name__+repr(tuple(self))


class Vector2(BaseVector):
    def __init__(self, x=(0, 0), y=None):
        if y is None:
            try:
                x, y = x
            except TypeError:
                raise TypeError("Pass 1 iterable or 2 numbers to Vector2")
            except ValueError:
                raise ValueError("The iterable you passed to Vector2 didn't have exactly 2 elements")
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y
    def __hash__(self):
        return hash(tuple(self))

    @property
    def _sfVector2i(self):
        self._sf_ptr = _ffi.new('sfVector2i*', tuple(self))
        return self._sf_ptr
    @property
    def _sfVector2u(self):
        self._sf_ptr = _ffi.new('sfVector2u*', tuple(self))
        return self._sf_ptr
    @property
    def _sfVector2f(self):
        self._sf_ptr = _ffi.new('sfVector2f*', tuple(self))
        return self._sf_ptr

class Vector3(BaseVector):
    def __init__(self, x, y=None, z=None):
        if y is None and z is None:
            try:
                x, y, z = x
            except TypeError:
                raise TypeError("Pass 1 iterable or 3 numbers to Vector3")
            except ValueError:
                raise ValueError("The iterable you passed to Vector3 didn't have exactly 3 elements")
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
    def __hash__(self):
        return hash(tuple(self))

    @property
    def _sfVector3f(self):
        self._sf_ptr = _ffi.new('sfVector3f*', tuple(self))
        return self._sf_ptr



class Rect(object):
    def __init__(self, position=(0, 0), size=(0, 0), **kwargs):
        try:
            if len(position)==4 and size==(0, 0):
                position, size = position[:2], position[2:]
        except TypeError:
            pass
        self.position = position
        self.size = size
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)

    @property
    def position(self):
        return Vector2(self.left, self.top)
    @position.setter
    def position(self, value):
        self.left, self.top = Vector2(value)

    @property
    def size(self):
        return Vector2(self.width, self.height)
    @size.setter
    def size(self, value):
        self.width, self.height = Vector2(value)

    @property
    def center(self):
        return self.position+self.size/2

    @property
    def right(self):
        return self.left+self.width
    @property
    def bottom(self):
        return self.top+self.height

    def __repr__(self):
        return '{}(({}, {}), width={}, height={})'.format(type(self).__name__, self.left, self.top, self.width, self.height)

    def __eq__(self, other):
        return self.left==other.left and self.top==other.top and\
          self.width==other.width and self.height==other.height
    def __ne__(self, other):
        return not (self==other)

    def contains(self, point):
        x, y = Vector2(point)
        l = min(self.left, self.right)
        r = max(self.left, self.right)
        t = min(self.top, self.bottom)
        b = max(self.top, self.bottom)
        return x>=l and x<r and y>=t and y<b
    __contains__ = contains

    def intersects(self, other):
        a, b = self, other
        l = max(min(a.left, a.right), min(b.left, b.right))
        t = max(min(a.top, a.bottom), min(b.top, b.bottom))
        r = min(max(a.left, a.right), max(b.left, b.right))
        b = min(max(a.top, a.bottom), max(b.top, b.bottom))
        if l<r and t<b:
            return type(self)((l, t), (r-l, b-t))
    __and__ = intersects

    @property
    def _sfIntRect(self):
        self._sf_ptr = _ffi.new('sfIntRect*', (self.left, self.top, self.width, self.height))
        return self._sf_ptr
    @property
    def _sfFloatRect(self):
        self._sf_ptr = _ffi.new('sfFloatRect*', (self.left, self.top, self.width, self.height))
        return self._sf_ptr



class Pixels(object):
    def __init__(self, size, data):
        self.size = _system.Vector2(size)
        self.data = data

    @property
    def width(self):
        return self.size.x
    @width.setter
    def width(self, value):
        self.size.x = value

    @property
    def height(self):
        return self.size.y
    @height.setter
    def height(self, value):
        self.size.y = value


class FakeCallableInt(int):
    def __call__(self):
        return int(self)


def arg_error(arg, cls):
    raise TypeError("`{}` must be a `{}` object".format(arg, cls))