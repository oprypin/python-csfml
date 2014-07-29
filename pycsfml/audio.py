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
_sf = _ffi.dlopen('libcsfml-audio.so')

from . import system as _system

from . import base
from .util import arg_error as _arg_error



class Listener(base.SFMLClass):
    @classmethod
    def set_global_volume(cls, volume):
        return _sf.sfListener_setGlobalVolume(volume)
    
    @classmethod
    def get_global_volume(cls):
        return _sf.sfListener_getGlobalVolume()
    
    @classmethod
    def set_position(cls, position):
        try: position = position._sfVector3f[0]
        except AttributeError: raise _arg_error('position', 'Vector3')
        return _sf.sfListener_setPosition(position)
    
    @classmethod
    def get_position(cls):
        result = _sf.sfListener_getPosition()
        return _system.Vector3(result.x, result.y, result.z)
    
    @classmethod
    def set_direction(cls, orientation):
        try: orientation = orientation._sfVector3f[0]
        except AttributeError: raise _arg_error('orientation', 'Vector3')
        return _sf.sfListener_setDirection(orientation)
    
    @classmethod
    def get_direction(cls):
        result = _sf.sfListener_getDirection()
        return _system.Vector3(result.x, result.y, result.z)
    

class SoundSource(object):
    STOPPED = _sf.sfStopped
    PAUSED = _sf.sfPaused
    PLAYING = _sf.sfPlaying

class SoundStream(base.SFMLClass, SoundSource):
    pass


class Music(SoundStream, base.SFMLClass):
    @classmethod
    def from_file(cls, filename):
        try: filename = filename.encode()
        except AttributeError: pass
        result = _sf.sfMusic_createFromFile(filename)
        if not result: raise IOError("Could not create Music from file {!r}".format(filename))
        return cls._wrap_ptr(result)
    
    @classmethod
    def from_memory(cls, data, size_in_bytes):
        result = _sf.sfMusic_createFromMemory(data, size_in_bytes)
        if not result: raise IOError("Could not create Music from memory")
        return cls._wrap_ptr(result)
    
    #@classmethod
    #def from_stream(cls, stream):
        #try: stream = stream._sfInputStream
        #except AttributeError: raise _arg_error('stream', 'InputStream')
        #result = _sf.sfMusic_createFromStream(stream)
        #if not result: raise IOError("Could not create Music from stream")
        #return cls._wrap_ptr(result)
    
    def __del__(self):
        if self._sf_owned: _sf.sfMusic_destroy(self._sfMusic)
    
    def get_loop(self):
        return _sf.sfMusic_getLoop(self._sfMusic)
    def set_loop(self, loop):
        return _sf.sfMusic_setLoop(self._sfMusic, loop)
    loop = property(get_loop, set_loop)

    def get_duration(self):
        result = _sf.sfMusic_getDuration(self._sfMusic)
        return Time._wrap_data(result)
    duration = property(get_duration)
    
    def play(self):
        return _sf.sfMusic_play(self._sfMusic)
    
    def pause(self):
        return _sf.sfMusic_pause(self._sfMusic)
    
    def stop(self):
        return _sf.sfMusic_stop(self._sfMusic)
    
    def get_channel_count(self):
        return _sf.sfMusic_getChannelCount(self._sfMusic)
    channel_count = property(get_channel_count)

    def get_sample_rate(self):
        return _sf.sfMusic_getSampleRate(self._sfMusic)
    sample_rate = property(get_sample_rate)
    
    def get_status(self):
        return _sf.sfMusic_getStatus(self._sfMusic)
    status = property(get_status)

    def get_pitch(self):
        return _sf.sfMusic_getPitch(self._sfMusic)
    def set_pitch(self, pitch):
        return _sf.sfMusic_setPitch(self._sfMusic, pitch)
    pitch = property(get_pitch, set_pitch)

    def get_volume(self):
        return _sf.sfMusic_getVolume(self._sfMusic)
    def set_volume(self, volume):
        return _sf.sfMusic_setVolume(self._sfMusic, volume)
    volume = property(get_volume, set_volume)

    def get_position(self):
        result = _sf.sfMusic_getPosition(self._sfMusic)
        return _system.Vector3(result.x, result.y, result.z)
    def set_position(self, position):
        try: position = position._sfVector3f[0]
        except AttributeError: raise _arg_error('position', 'Vector3')
        return _sf.sfMusic_setPosition(self._sfMusic, position)
    position = property(get_position, set_position)

    def is_relative_to_listener(self):
        return _sf.sfMusic_isRelativeToListener(self._sfMusic)
    def set_relative_to_listener(self, relative):
        return _sf.sfMusic_setRelativeToListener(self._sfMusic, relative)
    relative_to_listener = property(is_relative_to_listener, set_relative_to_listener)

    def get_min_distance(self):
        return _sf.sfMusic_getMinDistance(self._sfMusic)
    def set_min_distance(self, distance):
        return _sf.sfMusic_setMinDistance(self._sfMusic, distance)
    min_distance = property(get_min_distance, set_min_distance)

    def get_attenuation(self):
        return _sf.sfMusic_getAttenuation(self._sfMusic)
    def set_attenuation(self, attenuation):
        return _sf.sfMusic_setAttenuation(self._sfMusic, attenuation)
    attenuation = property(get_attenuation, set_attenuation)

    def get_playing_offset(self):
        result = _sf.sfMusic_getPlayingOffset(self._sfMusic)
        return Time._wrap_data(result)
    def set_playing_offset(self, time_offset):
        try: time_offset = time_offset._sfTime[0]
        except AttributeError: raise _arg_error('time_offset', 'Time')
        return _sf.sfMusic_setPlayingOffset(self._sfMusic, time_offset)
    playing_offset = property(get_playing_offset, set_playing_offset)



class Sound(base.SFMLClass, SoundSource):
    def __init__(self, buffer=None, **kwargs):
        self._sfSound = _sf.sfSound_create()
        if buffer: self.buffer = buffer
        if kwargs: self._set(**kwargs)
    
    def copy(self):
        result = _sf.sfSound_copy(self._sfSound)
        return self._wrap_ptr(result)
    
    def __del__(self):
        if self._sf_owned: _sf.sfSound_destroy(self._sfSound)
    
    def play(self):
        return _sf.sfSound_play(self._sfSound)
    
    def pause(self):
        return _sf.sfSound_pause(self._sfSound)
    
    def stop(self):
        return _sf.sfSound_stop(self._sfSound)
    
    def get_buffer(self):
        result = _sf.sfSound_getBuffer(self._sfSound)
        return SoundBuffer._wrap_ptr(result)
    def set_buffer(self, buffer):
        try: buffer = buffer._sfSoundBuffer
        except AttributeError: raise _arg_error('buffer', 'SoundBuffer')
        return _sf.sfSound_setBuffer(self._sfSound, buffer)
    buffer = property(get_buffer, set_buffer)
    
    def get_loop(self):
        return _sf.sfSound_getLoop(self._sfSound)
    def set_loop(self, loop):
        return _sf.sfSound_setLoop(self._sfSound, loop)
    loop = property(get_loop, set_loop)
    
    def get_status(self):
        return _sf.sfSound_getStatus(self._sfSound)
    status = property(get_status)
    
    def get_pitch(self):
        return _sf.sfSound_getPitch(self._sfSound)
    def set_pitch(self, pitch):
        return _sf.sfSound_setPitch(self._sfSound, pitch)
    pitch = property(get_pitch, set_pitch)
    
    def get_volume(self):
        return _sf.sfSound_getVolume(self._sfSound)
    def set_volume(self, volume):
        return _sf.sfSound_setVolume(self._sfSound, volume)
    volume = property(get_volume, set_volume)
    
    def get_position(self):
        result = _sf.sfSound_getPosition(self._sfSound)
        return _system.Vector3(result.x, result.y, result.z)
    def set_position(self, position):
        try: position = position._sfVector3f[0]
        except AttributeError: raise _arg_error('position', 'Vector3')
        return _sf.sfSound_setPosition(self._sfSound, position)
    position = property(get_position, set_position)
    
    def is_relative_to_listener(self):
        return _sf.sfSound_isRelativeToListener(self._sfSound)
    def set_relative_to_listener(self, relative):
        return _sf.sfSound_setRelativeToListener(self._sfSound, relative)
    relative_to_listener = property(is_relative_to_listener, set_relative_to_listener)
    
    def get_min_distance(self):
        return _sf.sfSound_getMinDistance(self._sfSound)
    def set_min_distance(self, distance):
        return _sf.sfSound_setMinDistance(self._sfSound, distance)
    min_distance = property(get_min_distance, set_min_distance)
    
    def get_attenuation(self):
        return _sf.sfSound_getAttenuation(self._sfSound)
    def set_attenuation(self, attenuation):
        return _sf.sfSound_setAttenuation(self._sfSound, attenuation)
    attenuation = property(get_attenuation, set_attenuation)

    def get_playing_offset(self):
        result = _sf.sfSound_getPlayingOffset(self._sfSound)
        return Time._wrap_data(result)
    def set_playing_offset(self, time_offset):
        try: time_offset = time_offset._sfTime[0]
        except AttributeError: raise _arg_error('time_offset', 'Time')
        return _sf.sfSound_setPlayingOffset(self._sfSound, time_offset)
    playing_offset = property(get_playing_offset, set_playing_offset)
    
    
    

class SoundBuffer(base.SFMLClass):
    @classmethod
    def from_file(cls, filename):
        try: filename = filename.encode()
        except AttributeError: pass
        result = _sf.sfSoundBuffer_createFromFile(filename)
        if not result: raise IOError("Could not create SoundBuffer from file {!r}".format(filename))
        return cls._wrap_ptr(result)
    
    @classmethod
    def from_memory(cls, data):
        if not result: raise IOError("Could not create SoundBuffer from memory")
        result = _sf.sfSoundBuffer_createFromMemory(data, len(data))
        return cls._wrap_ptr(result)
    
    @classmethod
    def from_stream(cls, stream):
        try: stream = stream._sfInputStream
        except AttributeError: raise _arg_error('stream', 'InputStream')
        result = _sf.sfSoundBuffer_createFromStream(stream)
        if not result: raise IOError("Could not create SoundBuffer from stream")
        return cls._wrap_ptr(result)
    
    @classmethod
    def from_samples(cls, samples, channel_count, sample_rate):
        result = _sf.sfSoundBuffer_createFromSamples(samples, sample_count, channel_count, sample_rate)
        if not result: raise IOError("Could not create SoundBuffer from samples")
        return cls._wrap_ptr(result)
    
    def copy(self):
        result = _sf.sfSoundBuffer_copy(self._sfSoundBuffer)
        return self._wrap_ptr(result)
    
    def __del__(self):
        if self._sf_owned: _sf.sfSoundBuffer_destroy(self._sfSoundBuffer)
    
    def save_to_file(self, filename):
        return _sf.sfSoundBuffer_saveToFile(self._sfSoundBuffer, filename)
    to_file = save_to_file
    
    def get_samples(self):
        return _sf.sfSoundBuffer_getSamples(self._sfSoundBuffer)
    
    def get_sample_count(self):
        return _sf.sfSoundBuffer_getSampleCount(self._sfSoundBuffer)
    
    def get_sample_rate(self):
        return _sf.sfSoundBuffer_getSampleRate(self._sfSoundBuffer)
    sample_rate = property(get_sample_rate)
    
    def get_channel_count(self):
        return _sf.sfSoundBuffer_getChannelCount(self._sfSoundBuffer)
    channel_count = channels_count = property(get_channel_count)
    
    def get_duration(self):
        result = _sf.sfSoundBuffer_getDuration(self._sfSoundBuffer)
        return Time._wrap_data(result)
    duration = property(get_duration)
    
class SoundRecorder(base.SFMLClass):
    def __init__(self, on_start, on_process, on_stop, user_data, **kwargs):
        self._sfSoundRecorder = _sf.sfSoundRecorder_create(on_start, on_process, on_stop, user_data)
        if kwargs: self._set(**kwargs)

    def __del__(self):
        if self._sf_owned: _sf.sfSoundRecorder_destroy(self._sfSoundRecorder)

    def start(self, sample_rate):
        return _sf.sfSoundRecorder_start(self._sfSoundRecorder, sample_rate)

    def stop(self):
        return _sf.sfSoundRecorder_stop(self._sfSoundRecorder)

    def get_sample_rate(self):
        return _sf.sfSoundRecorder_getSampleRate(self._sfSoundRecorder)

    @classmethod
    def is_available(cls):
        return _sf.sfSoundRecorder_isAvailable()


class SoundBufferRecorder(SoundRecorder):
    def __init__(self, **kwargs):
        self._sfSoundBufferRecorder = _sf.sfSoundBufferRecorder_create()
        if kwargs: self._set(**kwargs)
    
    def __del__(self):
        if self._sf_owned: _sf.sfSoundBufferRecorder_destroy(self._sfSoundBufferRecorder)
    
    def start(self, sample_rate):
        return _sf.sfSoundBufferRecorder_start(self._sfSoundBufferRecorder, sample_rate)
    
    def stop(self):
        return _sf.sfSoundBufferRecorder_stop(self._sfSoundBufferRecorder)
    
    def get_sample_rate(self):
        return _sf.sfSoundBufferRecorder_getSampleRate(self._sfSoundBufferRecorder)
    sample_rate = property(get_sample_rate)
    
    def get_buffer(self):
        result = _sf.sfSoundBufferRecorder_getBuffer(self._sfSoundBufferRecorder)
        return SoundBuffer._wrap_ptr(result)
    buffer = property(get_buffer)
    

    



del base