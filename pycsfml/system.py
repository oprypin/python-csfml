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
_sf = _ffi.dlopen('libcsfml-system.so')

from . import base
from .util import arg_error as _arg_error

from functools import total_ordering as _total_ordering
from threading import local as _threadlocal


@_total_ordering
class Time(base.SFMLStruct):
    def __init__(self):
        self._sfTime = _ffi.new('sfTime*', (0,))

    def __repr__(self):
        return 'microseconds({})'.format(self.microseconds)

    def as_seconds(self):
        return _sf.sfTime_asSeconds(self._sfTime[0])
    seconds = property(as_seconds)

    def as_milliseconds(self):
        return _sf.sfTime_asMilliseconds(self._sfTime[0])
    milliseconds = property(as_milliseconds)

    def as_microseconds(self):
        return _sf.sfTime_asMicroseconds(self._sfTime[0])
    microseconds = property(as_microseconds)

    def __int__(self):
        return self.microseconds

    def __eq__(self, other):
        return self.microseconds==other.microseconds
    def __lt__(self, other):
        return self.microseconds<other.microseconds
    def __neg__(self):
        return Time(-int(self))
    def __add__(self, other):
        return Time(int(self)+int(other))
    def __sub__(self, other):
        return Time(int(self)-int(other))
    def __mul__(self, other):
        return Time(int(self)*int(other))
    def __truediv__(self, other):
        return Time(int(self)/int(other))
    __div__ = __truediv__


def seconds(amount):
    result = _sf.sfSeconds(amount)
    return Time._wrap_data(result)

def milliseconds(amount):
    result = _sf.sfMilliseconds(amount)
    return Time._wrap_data(result)

def microseconds(amount):
    result = _sf.sfMicroseconds(amount)
    return Time._wrap_data(result)


class Clock(base.SFMLClass):
    def __init__(self):
        self._sfClock = _sf.sfClock_create()
    
    def copy(self):
        result = _sf.sfClock_copy(self._sfClock)
        return self._wrap_ptr(result)
    
    def __del__(self):
        if self._sf_owned: _sf.sfClock_destroy(self._sfClock)
    
    def get_elapsed_time(self):
        result = _sf.sfClock_getElapsedTime(self._sfClock)
        return Time._wrap_data(result)
    elapsed_time = property(get_elapsed_time)
    
    def restart(self):
        result = _sf.sfClock_restart(self._sfClock)
        return Time._wrap_data(result)
    

class Mutex(base.SFMLClass):
    def __init__(self):
        self._sfMutex = _sf.sfMutex_create()
    
    def __del__(self):
        if self._sf_owned: _sf.sfMutex_destroy(self._sfMutex)
    
    def lock(self):
        _sf.sfMutex_lock(self._sfMutex)
    
    def unlock(self):
        _sf.sfMutex_unlock(self._sfMutex)

    def __enter__(self):
        self.lock()
    def __exit__(self, typ, value, tb):
        self.unlock()


class Lock(object):
    def __init__(self, mutex):
        self.mutex = mutex
        self.mutex.lock()

    def __del__(self):
        self.mutex.unlock()



class Thread(base.SFMLClass):
    def __init__(self, function, *args, **kwargs):
        callback = lambda _: function(*args, **kwargs)
        self._callback = callback = _ffi.callback('void(void*)', callback)
        self._sfThread = _sf.sfThread_create(callback, _ffi.NULL)

    def __del__(self):
        if self._sf_owned: _sf.sfThread_destroy(self._sfThread)
    
    def launch(self):
        _sf.sfThread_launch(self._sfThread)
    
    def wait(self):
        _sf.sfThread_wait(self._sfThread)
    
    def terminate(self):
        _sf.sfThread_terminate(self._sfThread)


class ThreadLocal(_threadlocal):
    def __init__(self, value=None):
        _threadlocal.__init__(self)
        self.value = value

#def input_stream_read_func(data, size, user_data):
    #return _sf.sfInputStreamReadFunc(data, size, user_data)
    

#def input_stream_seek_func(position, user_data):
    #return _sf.sfInputStreamSeekFunc(position, user_data)
    

#def input_stream_tell_func(user_data):
    #return _sf.sfInputStreamTellFunc(user_data)
    

#def input_stream_get_size_func(user_data):
    #return _sf.sfInputStreamGetSizeFunc(user_data)
    

#class InputStream(base.SFMLStruct):
    #def __init__(self, read, seek, tell, get_size, user_data):
        #self._sfInputStream = _ffi.new('sfInputStream*')
        #self.read = read
        #self.seek = seek
        #self.tell = tell
        #self.get_size = get_size
        #self.user_data = user_data
    
    #@property
    #def read(self):
        #return self._sfInputStream.read
    #@read.setter
    #def read(self, value):
        #self._sfInputStream.read = value
    
    #@property
    #def seek(self):
        #return self._sfInputStream.seek
    #@seek.setter
    #def seek(self, value):
        #self._sfInputStream.seek = value
    
    #@property
    #def tell(self):
        #return self._sfInputStream.tell
    #@tell.setter
    #def tell(self, value):
        #self._sfInputStream.tell = value
    
    #@property
    #def get_size(self):
        #return self._sfInputStream.getSize
    #@get_size.setter
    #def get_size(self, value):
        #self._sfInputStream.getSize = value
    
    #@property
    #def user_data(self):
        #return self._sfInputStream.userData
    #@user_data.setter
    #def user_data(self, value):
        #self._sfInputStream.userData = value
    
    #def __repr__(self):
        #return self._repr('read= seek= tell= get_size= user_data=')


def sleep(duration):
    try: duration = duration._sfTime[0]
    except AttributeError: _arg_error('duration', 'Time')
    return _sf.sfSleep(duration)


from .util import Vector2, Vector3


del base