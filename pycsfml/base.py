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

try:
    from enum import IntEnum as SFMLEnum
except ImportError:
    class SFMLEnum(object):
        pass


class SFMLClass(object):
    _sf_owned = True

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("This class is not meant to be instantiated")

    @classmethod
    def _wrap_ptr(cls, sf_ptr, owned=False): #TODO owned
        self = object.__new__(cls)
        setattr(self, '_sf'+cls.__name__, sf_ptr)
        self._sf_owned = owned
        return self

    @classmethod
    def _wrap_data(cls, sf_data, owned=False):
        self = object.__new__(cls)
        self._sf_data = sf_data
        sf_ptr = _ffi.addressof(sf_data)
        setattr(self, '_sf'+cls.__name__, sf_ptr)
        self._sf_owned = owned
        return self

    def _set(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class SFMLStruct(SFMLClass):
    def _repr(self, attrs):
        try:
            cls_name = type(self).__qualname__
        except AttributeError:
            cls_name = type(self).__name__
        return '{}({})'.format(cls_name, ', '.join(
            ('{1}={0!r}' if '=' in a else '{0!r}').format(getattr(self, a.strip('=')), a.strip('=')) for a in attrs.split()
        ))