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
_sf = _ffi.dlopen('libcsfml-graphics.so')

from . import system as _system
from . import window as _window

from . import base
from .util import arg_error as _arg_error
from .util import Pixels, Rect, Rect as Rectangle


class BlendMode(base.SFMLEnum):
    ALPHA = BLEND_ALPHA = _sf.sfBlendAlpha
    ADD = BLEND_ADD = _sf.sfBlendAdd
    MULTIPLY = BLEND_MULTIPLY = _sf.sfBlendMultiply
    NONE = BLEND_NONE = _sf.sfBlendNone

class PrimitiveType(base.SFMLEnum):
    POINTS = _sf.sfPoints
    LINES = _sf.sfLines
    LINES_STRIP = _sf.sfLinesStrip
    TRIANGLES = _sf.sfTriangles
    TRIANGLES_STRIP = _sf.sfTrianglesStrip
    TRIANGLES_FAN = _sf.sfTrianglesFan
    QUADS = _sf.sfQuads


class Color(base.SFMLStruct):
    def __init__(self, r=0, g=0, b=0, a=255):
        self._sfColor = _ffi.new('sfColor*')
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    
    @property
    def r(self):
        return self._sfColor.r
    @r.setter
    def r(self, value):
        self._sfColor.r = value
    
    @property
    def g(self):
        return self._sfColor.g
    @g.setter
    def g(self, value):
        self._sfColor.g = value
    
    @property
    def b(self):
        return self._sfColor.b
    @b.setter
    def b(self, value):
        self._sfColor.b = value
    
    @property
    def a(self):
        return self._sfColor.a
    @a.setter
    def a(self, value):
        self._sfColor.a = value
    
    def __repr__(self):
        return self._repr('r= g= b= a=')

    def add(self, other):
        try: other = other._sfColor[0]
        except AttributeError: _arg_error('other', 'Color')
        result = _sf.sfColor_add(self._sfColor[0], other)
        return self._wrap_data(result)
    __add__ = add
    
    def modulate(self, other):
        try: other = other._sfColor[0]
        except AttributeError: _arg_error('other', 'Color')
        result = _sf.sfColor_modulate(self._sfColor[0], other)
        return self._wrap_data(result)
    __mul__ = modulate

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b
        yield self.a
    def __hash__(self):
        return hash(tuple(self))

    def __eq__(self, other):
        return all(a==b for a, b in zip(self, other))
    def __ne__(self, other):
        return any(a!=b for a, b in zip(self, other))

Color.BLACK = Color(0, 0, 0)
Color.WHITE = Color(255, 255, 255)
Color.RED = Color(255, 0, 0)
Color.GREEN = Color(0, 255, 0)
Color.BLUE = Color(0, 0, 255)
Color.YELLOW = Color(255, 255, 0)
Color.MAGENTA = Color(255, 0, 255)
Color.CYAN = Color(0, 255, 255)
Color.TRANSPARENT = Color(0, 0, 0, a=0)





class Transform(base.SFMLStruct):
    def __init__(self, values=(1, 0, 0, 0, 1, 0, 0, 0, 1)):
        self._sfTransform = _ffi.new('sfTransform*', (values,))

    def copy(self):
        return Transform(self.values)

    @property
    def values(self):
        return tuple(self._sfTransform.matrix)
    @values.setter
    def values(self, value):
        self._sfTransform.matrix = tuple(value)

    def __repr__(self):
        return self._repr('values')

    @classmethod
    def from_values(cls, a00, a01, a02, a10, a11, a12, a20, a21, a22):
        result = _sf.sfTransform_fromMatrix(a00, a01, a02, a10, a11, a12, a20, a21, a22)
        return cls._wrap_data(result)

    def get_matrix(self):
        m = _ffi.new('float[16]')
        _sf.sfTransform_getMatrix(self._sfTransform, m)
        return tuple(m)
    matrix = property(get_matrix)

    def get_inverse(self):
        result = _sf.sfTransform_getInverse(self._sfTransform)
        return self._wrap_data(result)
    inverse = property(get_inverse)

    def transform_point(self, point):
        point = _system.Vector2(point)
        try: point = point._sfVector2f[0]
        except AttributeError: _arg_error('point', 'Vector2f')
        result = _sf.sfTransform_transformPoint(self._sfTransform, point)
        return _system.Vector2(result.x, result.y)

    def transform_rect(self, rectangle):
        try: rectangle = rectangle._sfFloatRect[0]
        except AttributeError: _arg_error('rectangle', 'Rect')
        result = _sf.sfTransform_transformRect(self._sfTransform, rectangle)
        return Rect((result.left, result.top), (result.width, result.height))
    transform_rectangle = transform_rect

    def combine(self, other):
        try: other = other._sfTransform
        except AttributeError: raise base._arg_error('other', 'Transform')
        _sf.sfTransform_combine(self._sfTransform, other)
        return self
    __imul__ = combine
    def __mul__(self, other):
        return Transform(self.values).combine(other)

    def translate(self, offset):
        x, y = offset
        _sf.sfTransform_translate(self._sfTransform, x, y)
        return self

    def rotate(self, angle, center=None):
        if center is None:
            _sf.sfTransform_rotate(self._sfTransform, angle)
        else:
            x, y = center
            _sf.sfTransform_rotateWithCenter(self._sfTransform, angle, x, y)
        return self

    def scale(self, factor, center=None):
        fx, fy = factor
        if center is None:
            _sf.sfTransform_scale(self._sfTransform, fx, fy)
        else:
            cx, cy = center
            _sf.sfTransform_scaleWithCenter(self._sfTransform, fx, fy, cx, cy)
        return self

class Transformable(base.SFMLClass):
    _sf_type = 'sfTransformable'
    def __init__(self, **kwargs):
        self._sfTransformable = _sf.sfTransformable_create()
        if kwargs: self._set(**kwargs)

    def copy(self):
        result = getattr(_sf, self._sf_type+'_copy')(self._sfTransformable)
        return self._wrap_ptr(result)

    def __del__(self):
        if self._sf_owned: getattr(_sf, self._sf_type+'_destroy')(self._sfTransformable)


    def get_position(self):
        result = getattr(_sf, self._sf_type+'_getPosition')(self._sfTransformable)
        return _system.Vector2(result.x, result.y)
    def set_position(self, position):
        position = _system.Vector2(position)._sfVector2f[0]
        return getattr(_sf, self._sf_type+'_setPosition')(self._sfTransformable, position)
    position = property(get_position, set_position)

    def get_rotation(self):
        return getattr(_sf, self._sf_type+'_getRotation')(self._sfTransformable)
    def set_rotation(self, angle):
        return getattr(_sf, self._sf_type+'_setRotation')(self._sfTransformable, angle)
    rotation = property(get_rotation, set_rotation)

    def get_scale(self):
        result = getattr(_sf, self._sf_type+'_getScale')(self._sfTransformable)
        return _system.Vector2(result.x, result.y)
    def set_scale(self, scale):
        scale = _system.Vector2(scale)._sfVector2f[0]
        return getattr(_sf, self._sf_type+'_setScale')(self._sfTransformable, scale)
    ratio = property(get_scale, set_scale)

    def get_origin(self):
        result = getattr(_sf, self._sf_type+'_getOrigin')(self._sfTransformable)
        return _system.Vector2(result.x, result.y)
    def set_origin(self, origin):
        origin = _system.Vector2(origin)._sfVector2f[0]
        return getattr(_sf, self._sf_type+'_setOrigin')(self._sfTransformable, origin)
    origin = property(get_origin, set_origin)


    def move(self, offset):
        offset = _system.Vector2(offset)._sfVector2f[0]
        return getattr(_sf, self._sf_type+'_move')(self._sfTransformable, offset)

    def rotate(self, angle):
        return getattr(_sf, self._sf_type+'_rotate')(self._sfTransformable, angle)

    def scale(self, factors):
        factors = _system.Vector2(factors)._sfVector2f[0]
        return getattr(_sf, self._sf_type+'_scale')(self._sfTransformable, factors)

    def get_transform(self):
        result = getattr(_sf, self._sf_type+'_getTransform')(self._sfTransformable)
        return Transform._wrap_data(result)
    transform = property(get_transform)

    def get_inverse_transform(self):
        getattr(_sf, self._sf_type+'_getInverseTransform')(self._sfTransformable)
        return Transform._wrap_data(result)
    inverse_transform = property(get_inverse_transform)


class Drawable(object):
    def draw(self, target, states):
        raise NotImplementedError("Reimplement `draw` in your subclass")


class TransformableDrawable(Transformable, Drawable):
    pass

class Sprite(Drawable, Transformable):
    _sf_type = 'sfSprite'
    def __init__(self, texture=None, rectangle=None, **kwargs):
        self._sfSprite = _sf.sfSprite_create()
        self._sfTransformable = self._sfSprite
        if texture is not None: self.texture = texture
        if rectangle is not None: self.texture_rectangle = rectangle
        if kwargs: self._set(**kwargs)

    def get_texture(self):
        result = _sf.sfSprite_getTexture(self._sfSprite)
        return Texture._wrap_ptr(result)
    def set_texture(self, texture, reset_rect=True):
        try: texture = texture._sfTexture
        except AttributeError: _arg_error('texture', 'Texture')
        return _sf.sfSprite_setTexture(self._sfSprite, texture, reset_rect)
    texture = property(get_texture, set_texture)

    def get_texture_rect(self):
        result = _sf.sfSprite_getTextureRect(self._sfSprite)
        return Rect((result.left, result.top), (result.width, result.height))
    def set_texture_rect(self, rectangle):
        try: rectangle = rectangle._sfIntRect[0]
        except AttributeError: _arg_error('rectangle', 'Rect')
        return _sf.sfSprite_setTextureRect(self._sfSprite, rectangle)
    texture_rect = texture_rectangle = property(get_texture_rect, set_texture_rect)

    def get_color(self):
        result = _sf.sfSprite_getColor(self._sfSprite)
        return Color._wrap_data(result)
    def set_color(self, color):
        try: color = color._sfColor[0]
        except AttributeError: _arg_error('color', 'Color')
        return _sf.sfSprite_setColor(self._sfSprite, color)
    color = property(get_color, set_color)

    def get_local_bounds(self):
        result = _sf.sfSprite_getLocalBounds(self._sfSprite)
        return Rect((result.left, result.top), (result.width, result.height))
    local_bounds = property(get_local_bounds)

    def get_global_bounds(self):
        result = _sf.sfSprite_getGlobalBounds(self._sfSprite)
        return Rect((result.left, result.top), (result.width, result.height))
    global_bounds = property(get_global_bounds)


    def draw(self, target, states):
        try: starget = getattr(target, '_'+target._sf_type)
        except AttributeError: _arg_error('target', 'RenderTarget')
        try: states = states._sfRenderStates
        except AttributeError: _arg_error('states', 'RenderStates')
        return getattr(_sf, target._sf_type+'_drawSprite')(starget, self._sfSprite, states)


class Font(base.SFMLClass):
    @classmethod
    def from_file(cls, filename):
        try: filename = filename.encode()
        except AttributeError: pass
        result = _sf.sfFont_createFromFile(filename)
        if not result: raise IOError("Could not create Font from file {!r}".format(filename))
        return cls._wrap_ptr(result)
    
    @classmethod
    def from_memory(cls, data):
        result = _sf.sfFont_createFromMemory(data, len(data))
        if not result: raise IOError("Could not create Font from memory")
        return cls._wrap_ptr(result)
    
    #@classmethod
    #def from_stream(cls, stream):
        #try: stream = stream._sfInputStream
        #except AttributeError: _arg_error('stream', 'InputStream')
        #result = _sf.sfFont_createFromStream(stream)
        #return cls._wrap_ptr(result)
    
    def copy(self):
        result = _sf.sfFont_copy(self._sfFont)
        return self._wrap_ptr(result)
    
    def __del__(self):
        if self._sf_owned: _sf.sfFont_destroy(self._sfFont)
    
    def get_glyph(self, code_point, character_size, bold):
        try: code_point = ord(code_point)
        except TypeError: pass
        result = _sf.sfFont_getGlyph(self._sfFont, code_point, character_size, bold)
        return Glyph._wrap_data(result)
    
    def get_kerning(self, first, second, character_size):
        try: first, second = ord(first), ord(second)
        except TypeError: pass
        return _sf.sfFont_getKerning(self._sfFont, first, second, character_size)
    
    def get_line_spacing(self, character_size):
        return _sf.sfFont_getLineSpacing(self._sfFont, character_size)
    
    def get_texture(self, character_size):
        result = _sf.sfFont_getTexture(self._sfFont, character_size)
        return Texture._wrap_ptr(result)
    

class Image(base.SFMLClass):
    def __init__(self, width, height, **kwargs):
        self._sfImage = _sf.sfImage_create(width, height)
        if kwargs: self._set(**kwargs)
    
    @classmethod
    def from_color(cls, width, height, color):
        try: color = color._sfColor[0]
        except AttributeError: _arg_error('color', 'Color')
        result = _sf.sfImage_createFromColor(width, height, color)
        return cls._wrap_ptr(result)
    create = from_color
    
    @classmethod
    def from_pixels(cls, pixels):
        result = _sf.sfImage_createFromPixels(pixels.width, pixels.height, pixels.data)
        if not result: raise IOError("Could not create Image from pixels")
        return cls._wrap_ptr(result)
    
    @classmethod
    def from_file(cls, filename):
        try: filename = filename.encode()
        except AttributeError: pass
        result = _sf.sfImage_createFromFile(filename)
        if not result: raise IOError("Could not create Image from file {!r}".format(filename))
        return cls._wrap_ptr(result)
    
    @classmethod
    def from_memory(cls, data):
        result = _sf.sfImage_createFromMemory(data, len(data))
        if not result: raise IOError("Could not create Image from memory")
        return cls._wrap_ptr(result)
    
    #@classmethod
    #def from_stream(cls, stream):
        #try: stream = stream._sfInputStream
        #except AttributeError: _arg_error('stream', 'InputStream')
        #result = _sf.sfImage_createFromStream(stream)
        #return cls._wrap_ptr(result)
    
    def copy(self):
        result = _sf.sfImage_copy(self._sfImage)
        return self._wrap_ptr(result)
    
    def __del__(self):
        if self._sf_owned: _sf.sfImage_destroy(self._sfImage)
    
    def save_to_file(self, filename):
        try: filename = filename.encode()
        except AttributeError: pass
        return _sf.sfImage_saveToFile(self._sfImage, filename)
    to_file = save_to_file
    
    def get_size(self):
        result = _sf.sfImage_getSize(self._sfImage)
        return _system.Vector2(result.x, result.y)
    size = property(get_size)

    @property
    def width(self):
        return self.size.x
    @property
    def height(self):
        return self.size.y
    
    def mask_from_color(self, color, alpha=0):
        image = self._sfImage
        try: color = color._sfColor[0]
        except AttributeError: _arg_error('color', 'Color')
        return _sf.sfImage_createMaskFromColor(image, color, alpha)
    create_mask_from_color = mask_from_color
    
    def copy_image(self, source, dest, source_rect=Rect((0, 0), (0, 0)), apply_alpha=False):
        try: source = source._sfImage
        except AttributeError: _arg_error('source', 'Image')
        try: source_rect = source_rect._sfIntRect[0]
        except AttributeError: _arg_error('source_rect', 'Rect')
        return _sf.sfImage_copyImage(self._sfImage, source, dest_x, dest_y, source_rect, apply_alpha)
    blit = copy_image
    
    def get_pixel(self, xy):
        result = _sf.sfImage_getPixel(self._sfImage, *xy)
        return Color._wrap_data(result)
    __getitem__ = get_pixel
    def set_pixel(self, xy, color):
        x, y = xy
        try: color = color._sfColor[0]
        except AttributeError: _arg_error('color', 'Color')
        return _sf.sfImage_setPixel(self._sfImage, x, y, color)
    __setitem__ = set_pixel
    
    def get_pixels_ptr(self):
        return Pixels(self.size, _sf.sfImage_getPixelsPtr(self._sfImage))
    pixels = property(get_pixels_ptr)
    
    def flip_horizontally(self):
        return _sf.sfImage_flipHorizontally(self._sfImage)
    def flip_vertically(self):
        return _sf.sfImage_flipVertically(self._sfImage)


class Texture(base.SFMLClass, _window.GlResource):
    def __init__(self, width, height, **kwargs):
        self._sfTexture = _sf.sfTexture_create(width, height)
        if not self._sfTexture: raise RuntimeError("Could not create a texture of size {!r}, {!r}".format(width, height))
        if kwargs: self._set(**kwargs)

    @classmethod
    def create(cls, width, height):
        return cls(width, height)

    @classmethod
    def from_file(cls, filename, area=Rect((0, 0), (0, 0))):
        try: filename = filename.encode()
        except AttributeError: pass
        try: area = area._sfIntRect
        except AttributeError: _arg_error('area', 'Rect')
        result = _sf.sfTexture_createFromFile(filename, area)
        if not result: raise IOError("Could not create Texture from file {!r}".format(filename))
        return cls._wrap_ptr(result)

    @classmethod
    def from_memory(cls, data, area=Rect((0, 0), (0, 0))):
        try: area = area._sfIntRect
        except AttributeError: _arg_error('area', 'Rect')
        result = _sf.sfTexture_createFromMemory(data, len(data), area)
        if not result: raise IOError("Could not create Texture from memory")
        return cls._wrap_ptr(result)

    #@classmethod
    #def from_stream(cls, stream, area):
        #try: stream = stream._sfInputStream
        #except AttributeError: _arg_error('stream', 'InputStream')
        #try: area = area._sfIntRect
        #except AttributeError: _arg_error('area', 'Rect')
        #result = _sf.sfTexture_createFromStream(stream, area)
        #return cls._wrap_ptr(result)

    @classmethod
    def from_image(cls, image, area=Rect((0, 0), (0, 0))):
        try: image = image._sfImage
        except AttributeError: _arg_error('image', 'Image')
        try: area = area._sfIntRect
        except AttributeError: _arg_error('area', 'Rect')
        result = _sf.sfTexture_createFromImage(image, area)
        if not result: raise IOError("Could not create Texture from Image")
        return cls._wrap_ptr(result)

    def copy(self):
        result = _sf.sfTexture_copy(self._sfTexture)
        return self._wrap_ptr(result)

    def __del__(self):
        if self._sf_owned: _sf.sfTexture_destroy(self._sfTexture)

    def get_size(self):
        result = _sf.sfTexture_getSize(self._sfTexture)
        return _system.Vector2(result.x, result.y)
    size = property(get_size)

    def copy_to_image(self):
        result = _sf.sfTexture_copyToImage(self._sfTexture)
        return Image._wrap_ptr(result)
    to_image = copy_to_image

    def update_from_pixels(self, pixels, position=Rect((0, 0), (0, 0))):
        return _sf.sfTexture_updateFromPixels(self._sfTexture, pixels, position.width, position.height, position.x, position.y)

    def update_from_image(self, image, position):
        position = _system.Vector2(position)
        try: image = image._sfImage
        except AttributeError: _arg_error('image', 'Image')
        return _sf.sfTexture_updateFromImage(self._sfTexture, image, *position)

    def update_from_window(self, window, position):
        position = _system.Vector2(position)
        try:
            window = window._sfRenderWindow
            return _sf.sfTexture_updateFromWindow(self._sfTexture, window, *position)
        except AttributeError:
            try:
                window = window._sfWindow
                return _sf.sfTexture_updateFromRenderWindow(self._sfTexture, window, *position)
            except AttributeError:
                _arg_error('window', 'Window')

    def is_smooth(self):
        return _sf.sfTexture_isSmooth(self._sfTexture)
    def set_smooth(self, smooth):
        return _sf.sfTexture_setSmooth(self._sfTexture, smooth)
    smooth = property(is_smooth, set_smooth)

    def is_repeated(self):
        return _sf.sfTexture_isRepeated(self._sfTexture)
    def set_repeated(self, repeated):
        return _sf.sfTexture_setRepeated(self._sfTexture, repeated)
    repeated = property(is_repeated, set_repeated)

    def bind(self):
        return _sf.sfTexture_bind(self._sfTexture)

    @classmethod
    def get_maximum_size(cls):
        return _sf.sfTexture_getMaximumSize()




class Shader(base.SFMLClass, _window.GlResource):
    @classmethod
    def from_file(cls, vertex_filename, fragment_filename):
        try: vertex_filename = vertex_filename.encode()
        except AttributeError: pass
        try: fragment_filename = fragment_filename.encode()
        except AttributeError: pass
        result = _sf.sfShader_createFromFile(vertex_filename, fragment_filename)
        if not result: raise IOError("Could not create Shader from files {!r}, {!r}".format(vertex_filename, fragment_filename))
        return cls._wrap_ptr(result)
    
    @classmethod
    def from_memory(cls, vertex_shader, fragment_shader):
        result = _sf.sfShader_createFromMemory(vertex_shader, fragment_shader)
        if not result: raise IOError("Could not create Shader from memory")
        return cls._wrap_ptr(result)
    
    #@classmethod
    #def from_stream(cls, vertex_shader_stream, fragment_shader_stream):
        #try: vertex_shader_stream = vertex_shader_stream._sfInputStream
        #except AttributeError: _arg_error('vertex_shader_stream', 'InputStream')
        #try: fragment_shader_stream = fragment_shader_stream._sfInputStream
        #except AttributeError: _arg_error('fragment_shader_stream', 'InputStream')
        #result = _sf.sfShader_createFromStream(vertex_shader_stream, fragment_shader_stream)
        #return cls._wrap_ptr(result)
    
    def __del__(self):
        if self._sf_owned: _sf.sfShader_destroy(self._sfShader)
    
    def set_float_parameter(self, name, x):
        return _sf.sfShader_setFloatParameter(self._sfShader, name, x)
    set_1float_parameter = set_float_parameter
    def set_float2_parameter(self, name, x, y):
        return _sf.sfShader_setFloat2Parameter(self._sfShader, name, x, y)
    set_2float_parameter = set_float2_parameter
    def set_float3_parameter(self, name, x, y, z):
        return _sf.sfShader_setFloat3Parameter(self._sfShader, name, x, y, z)
    set_3float_parameter = set_float3_parameter
    def set_float4_parameter(self, name, x, y, z, w):
        return _sf.sfShader_setFloat4Parameter(self._sfShader, name, x, y, z, w)
    set_4float_parameter = set_float4_parameter
    def set_vector2_parameter(self, name, vector):
        vector = _system.Vector2(vector)._sfVector2f[0]
        return _sf.sfShader_setVector2Parameter(self._sfShader, name, vector)
    def set_vector3_parameter(self, name, vector):
        try: vector = vector._sfVector3f[0]
        except AttributeError: _arg_error('vector', 'Vector3\1')
        return _sf.sfShader_setVector3Parameter(self._sfShader, name, vector)
    def set_color_parameter(self, name, color):
        try: color = color._sfColor[0]
        except AttributeError: _arg_error('color', 'Color')
        return _sf.sfShader_setColorParameter(self._sfShader, name, color)
    def set_transform_parameter(self, name, transform):
        try: transform = transform._sfTransform[0]
        except AttributeError: _arg_error('transform', 'Transform')
        return _sf.sfShader_setTransformParameter(self._sfShader, name, transform)
    def set_texture_parameter(self, name, texture):
        try: texture = texture._sfTexture
        except AttributeError: _arg_error('texture', 'Texture')
        return _sf.sfShader_setTextureParameter(self._sfShader, name, texture)
    def set_current_texture_parameter(self, name):
        return _sf.sfShader_setCurrentTextureParameter(self._sfShader, name)
    set_currenttexturetype_parameter = set_current_texture_parameter
    
    def set_parameter(self, name, *args):
        if len(args)==1:
            (arg,) = args
            if isinstance(arg, (float, int)):
                self.set_float_parameter(name, arg)
            elif isinstance(arg, _system.Vector2):
                self.set_vector2_parameter(name, arg)
            elif isinstance(arg, _system.Vector3):
                self.set_vector3_parameter(name, arg)
            elif isinstance(arg, Color):
                self.set_color_parameter(name, arg)
            elif isinstance(arg, Transform):
                self.set_transform_parameter(name, arg)
            elif isinstance(arg, Texture):
                self.set_texture_parameter(name, arg)
            else:
                self.set_float_parameter(name, arg)
        elif len(args)==0:
            self.set_current_texture_parameter(name)
        elif len(args)==2:
            self.set_float2_parameter(name, *args)
        elif len(args)==3:
            self.set_float3_parameter(name, *args)
        elif len(args)==4:
            self.set_float4_parameter(name, *args)

    def bind(self):
        return _sf.sfShader_bind(self._sfShader)
    
    @classmethod
    def is_available(cls):
        return _sf.sfShader_isAvailable()
    




#class RenderTexture(base.SFMLClass, RenderTarget):
    #_sf_type = 'sfRenderTexture'
    #def __init__(self, width, height, depth_buffer, **kwargs):
        #self._sfRenderTexture = _sf.sfRenderTexture_create(width, height, depth_buffer)
        #if kwargs: self._set(**kwargs)
    
    #def __del__(self):
        #_sf.sfRenderTexture_destroy(self._sfRenderTexture)
    
    #def get_size(self):
        #result = _sf.sfRenderTexture_getSize(self._sfRenderTexture)
        #return _system.Vector2(result.x, result.y)
    
    #def set_active(self, active):
        #return _sf.sfRenderTexture_setActive(self._sfRenderTexture, active)
    
    #def display(self):
        #return _sf.sfRenderTexture_display(self._sfRenderTexture)
    
    #def clear(self, color):
        #try: color = color._sfColor[0]
        #except AttributeError: _arg_error('color', 'Color')
        #return _sf.sfRenderTexture_clear(self._sfRenderTexture, color)
    
    #def set_view(self, view):
        #try: view = view._sfView
        #except AttributeError: _arg_error('view', 'View')
        #return _sf.sfRenderTexture_setView(self._sfRenderTexture, view)
    
    #def get_view(self):
        #result = _sf.sfRenderTexture_getView(self._sfRenderTexture)
        #return View._wrap_ptr(result)
    
    #def get_default_view(self):
        #result = _sf.sfRenderTexture_getDefaultView(self._sfRenderTexture)
        #return View._wrap_ptr(result)
    
    #def get_viewport(self, view):
        #try: view = view._sfView
        #except AttributeError: _arg_error('view', 'View')
        #result = _sf.sfRenderTexture_getViewport(self._sfRenderTexture, view)
        #return Rect((result.left, result.top), (result.width, result.height))

    #def map_pixel_to_coords(self, point, view):
        #point = _system.Vector2(point)._sfVector2i[0]
        #try: view = view._sfView
        #except AttributeError: _arg_error('view', 'View')
        #result = _sf.sfRenderTexture_mapPixelToCoords(self._sfRenderTexture, point, view)
        #return _system.Vector2(result.x, result.y)
    
    #def map_coords_to_pixel(self, point, view):
        #point = _system.Vector2(point)._sfVector2f[0]
        #try: view = view._sfView
        #except AttributeError: _arg_error('view', 'View')
        #result = _sf.sfRenderTexture_mapCoordsToPixel(self._sfRenderTexture, point, view)
        #return _system.Vector2(result.x, result.y)
    
    #def draw_sprite(self, object, states):
        #try: object = object._sfSprite
        #except AttributeError: _arg_error('object', 'Sprite')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderTexture_drawSprite(self._sfRenderTexture, object, states)
    
    #def draw_text(self, object, states):
        #try: object = object._sfText
        #except AttributeError: _arg_error('object', 'Text')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderTexture_drawText(self._sfRenderTexture, object, states)
    
    #def draw_shape(self, object, states):
        #try: object = object._sfShape
        #except AttributeError: _arg_error('object', 'Shape')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderTexture_drawShape(self._sfRenderTexture, object, states)
    
    #def draw_circle_shape(self, object, states):
        #try: object = object._sfCircleShape
        #except AttributeError: _arg_error('object', 'CircleShape')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderTexture_drawCircleShape(self._sfRenderTexture, object, states)
    
    #def draw_convex_shape(self, object, states):
        #try: object = object._sfConvexShape
        #except AttributeError: _arg_error('object', 'ConvexShape')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderTexture_drawConvexShape(self._sfRenderTexture, object, states)
    
    #def draw_rectangle_shape(self, object, states):
        #try: object = object._sfRectangleShape
        #except AttributeError: _arg_error('object', 'RectangleShape')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderTexture_drawRectangleShape(self._sfRenderTexture, object, states)
    
    #def draw_vertex_array(self, object, states):
        #try: object = object._sfVertexArray
        #except AttributeError: _arg_error('object', 'VertexArray')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderTexture_drawVertexArray(self._sfRenderTexture, object, states)
    
    #def draw_primitives(self, vertices, vertex_count, type, states):
        #try: vertices = vertices._sfVertex
        #except AttributeError: _arg_error('vertices', 'Vertex')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderTexture_drawPrimitives(self._sfRenderTexture, vertices, vertex_count, type, states)
    
    #def push_glstates(self):
        #return _sf.sfRenderTexture_pushGLStates(self._sfRenderTexture)
    
    #def pop_glstates(self):
        #return _sf.sfRenderTexture_popGLStates(self._sfRenderTexture)
    
    #def reset_glstates(self):
        #return _sf.sfRenderTexture_resetGLStates(self._sfRenderTexture)
    
    #def get_texture(self):
        #result = _sf.sfRenderTexture_getTexture(self._sfRenderTexture)
        #return Texture._wrap_ptr(result)
    
    #def set_smooth(self, smooth):
        #return _sf.sfRenderTexture_setSmooth(self._sfRenderTexture, smooth)
    
    #def is_smooth(self):
        #return _sf.sfRenderTexture_isSmooth(self._sfRenderTexture)
    
    #def set_repeated(self, repeated):
        #return _sf.sfRenderTexture_setRepeated(self._sfRenderTexture, repeated)
    
    #def is_repeated(self):
        #return _sf.sfRenderTexture_isRepeated(self._sfRenderTexture)
    

class RenderTarget(object):
    pass

class RenderStates(base.SFMLStruct):
    def __init__(self, blend_mode=BlendMode.ALPHA, transform=Transform(), texture=None, shader=None):
        self._sfRenderStates = _ffi.new('sfRenderStates*')
        self.blend_mode = blend_mode
        self.transform = transform
        if texture: self.texture = texture
        if shader: self.shader = shader

    def copy(self):
        return RenderStates(self.blend_mode, self.transform.copy(), self.texture, self.shader)

    @property
    def blend_mode(self):
        return self._sfRenderStates.blendMode
    @blend_mode.setter
    def blend_mode(self, value):
        self._sfRenderStates.blendMode = value

    @property
    def transform(self):
        return Transform._wrap_data(self._sfRenderStates.transform)
    @transform.setter
    def transform(self, value):
        self._sfRenderStates.transform = value._sfTransform[0]

    @property
    def texture(self):
        return Texture._wrap_ptr(self._sfRenderStates.texture)
    @texture.setter
    def texture(self, value):
        self._sfRenderStates.texture = value._sfTexture

    @property
    def shader(self):
        return Shader._wrap_ptr(self._sfRenderStates.shader)
    @shader.setter
    def shader(self, value):
        self._sfRenderStates.shader = value._sfShader

    def __repr__(self):
        return self._repr('blend_mode= transform= texture= shader=')


class RenderWindow(_window.Window, RenderTarget):
    _sf_type = 'sfRenderWindow'
    def __init__(self, mode, title, style=_window.Style.DEFAULT, settings=_window.ContextSettings(), **kwargs):
        try: mode = mode._sfVideoMode[0]
        except AttributeError: _arg_error('mode', 'VideoMode')
        title = [ord(c) for c in title]+[0]
        try: settings = settings._sfContextSettings
        except AttributeError: _arg_error('settings', 'ContextSettings')
        self._sfRenderWindow = _sf.sfRenderWindow_createUnicode(mode, title, style, settings)
        if kwargs: self._set(**kwargs)
    
    @classmethod
    def from_handle(cls, handle, settings=_window.ContextSettings()):
        try: settings = settings._sfContextSettings
        except AttributeError: _arg_error('settings', 'ContextSettings')
        result = _sf.sfRenderWindow_createFromHandle(handle, settings)
        return cls._wrap_ptr(result)
    
    def __del__(self):
        if self._sf_owned: _sf.sfRenderWindow_destroy(self._sfRenderWindow)
    
    def close(self):
        return _sf.sfRenderWindow_close(self._sfRenderWindow)
    
    def is_open(self):
        return _sf.sfRenderWindow_isOpen(self._sfRenderWindow)
    is_open = property(is_open)

    def get_settings(self):
        result = _sf.sfRenderWindow_getSettings(self._sfRenderWindow)
        return ContextSettings._wrap_data(result)
    settings = property(get_settings)

    def poll_event(self):
        event = _ffi.new('sfEvent*')
        if _sf.sfRenderWindow_pollEvent(self._sfRenderWindow, event):
            return _window.Event._wrap(event)
    @property
    def events(self):
        return iter(self.poll_event, None)

    def wait_event(self):
        event = _ffi.new('sfEvent*')
        if _sf.sfRenderWindow_waitEvent(self._sfRenderWindow, event):
            return _window.Event._wrap(event)

    def get_position(self):
        result = _sf.sfRenderWindow_getPosition(self._sfRenderWindow)
        return _system.Vector2(result.x, result.y)
    def set_position(self, position):
        position = _system.Vector2(position)._sfVector2i[0]
        return _sf.sfRenderWindow_setPosition(self._sfRenderWindow, position)
    position = property(get_position, set_position)

    def get_size(self):
        result = _sf.sfRenderWindow_getSize(self._sfRenderWindow)
        return _system.Vector2(result.x, result.y)
    def set_size(self, size):
        size = _system.Vector2(size)._sfVector2u[0]
        return _sf.sfRenderWindow_setSize(self._sfRenderWindow, size)
    size = property(get_size, set_size)

    @property
    def width(self):
        return self.size.x
    @width.setter
    def width(self, value):
        self.size = (value, self.size.y)
    @property
    def height(self):
        return self.size.y
    @height.setter
    def height(self, value):
        self.size = (self.size.x, value)

    def set_title(self, title):
        title = [ord(c) for c in title]+[0]
        return _sf.sfRenderWindow_setUnicodeTitle(self._sfRenderWindow, title)
    title = property(fset=set_title)

    def set_icon(self, width, height, pixels):
        return _sf.sfRenderWindow_setIcon(self._sfRenderWindow, width, height, pixels)
    icon = property(fset=set_icon)

    def set_visible(self, visible):
        return _sf.sfRenderWindow_setVisible(self._sfRenderWindow, visible)
    visible = property(fset=set_visible)
    def show(self):
        self.visible = True
    def hide(self):
        self.visible = False

    def set_mouse_cursor_visible(self, show):
        return _sf.sfRenderWindow_setMouseCursorVisible(self._sfRenderWindow, show)
    mouse_cursor_visible = property(fset=set_mouse_cursor_visible)

    def set_vertical_sync_enabled(self, enabled):
        return _sf.sfRenderWindow_setVerticalSyncEnabled(self._sfRenderWindow, enabled)
    vertical_sync_enabled = vertical_synchronization = property(fset=set_vertical_sync_enabled)

    def set_key_repeat_enabled(self, enabled):
        return _sf.sfRenderWindow_setKeyRepeatEnabled(self._sfRenderWindow, enabled)
    key_repeat_enabled = property(fset=set_key_repeat_enabled)

    def set_active(self, active):
        return _sf.sfRenderWindow_setActive(self._sfRenderWindow, active)
    active = property(fset=set_active)

    def display(self):
        return _sf.sfRenderWindow_display(self._sfRenderWindow)
    
    def set_framerate_limit(self, limit):
        return _sf.sfRenderWindow_setFramerateLimit(self._sfRenderWindow, limit)
    framerate_limit = property(fset=set_framerate_limit)

    def set_joystick_threshold(self, threshold):
        return _sf.sfRenderWindow_setJoystickThreshold(self._sfRenderWindow, threshold)
    joystick_threshold = property(fset=set_joystick_threshold)

    def get_system_handle(self):
        return _sf.sfRenderWindow_getSystemHandle(self._sfRenderWindow)
    system_handle = property(get_system_handle)

    def clear(self, color=Color.BLACK):
        try: color = color._sfColor[0]
        except AttributeError: _arg_error('color', 'Color')
        return _sf.sfRenderWindow_clear(self._sfRenderWindow, color)
    
    def get_view(self):
        result = _sf.sfRenderWindow_getView(self._sfRenderWindow)
        return View._wrap_ptr(result)
    def set_view(self, view):
        try: view = view._sfView
        except AttributeError: _arg_error('view', 'View')
        return _sf.sfRenderWindow_setView(self._sfRenderWindow, view)
    view = property(get_view, set_view)
    
    def get_default_view(self):
        result = _sf.sfRenderWindow_getDefaultView(self._sfRenderWindow)
        return View._wrap_ptr(result)
    default_view = property(get_default_view)
    
    def get_viewport(self, view):
        try: view = view._sfView
        except AttributeError: _arg_error('view', 'View')
        result = _sf.sfRenderWindow_getViewport(self._sfRenderWindow, view)
        return Rect((result.left, result.top), (result.width, result.height))

    def map_pixel_to_coords(self, point, view):
        point = _system.Vector2(point)._sfVector2i[0]
        try: view = view._sfView
        except AttributeError: _arg_error('view', 'View')
        result = _sf.sfRenderWindow_mapPixelToCoords(self._sfRenderWindow, point, view)
        return _system.Vector2(result.x, result.y)
    convert_coords = map_pixel_to_coords #TODO
    
    def map_coords_to_pixel(self, point, view):
        point = _system.Vector2(point)._sfVector2f[0]
        try: view = view._sfView
        except AttributeError: _arg_error('view', 'View')
        result = _sf.sfRenderWindow_mapCoordsToPixel(self._sfRenderWindow, point, view)
        return _system.Vector2(result.x, result.y)
    convert_coords = map_coords_to_pixel #TODO

    def draw(self, drawable, states=RenderStates()):
        drawable.draw(self, states.copy())

    #def draw_sprite(self, object, states):
        #try: object = object._sfSprite
        #except AttributeError: _arg_error('object', 'Sprite')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderWindow_drawSprite(self._sfRenderWindow, object, states)
    
    #def draw_text(self, object, states):
        #try: object = object._sfText
        #except AttributeError: _arg_error('object', 'Text')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderWindow_drawText(self._sfRenderWindow, object, states)
    
    #def draw_shape(self, object, states):
        #try: object = object._sfShape
        #except AttributeError: _arg_error('object', 'Shape')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderWindow_drawShape(self._sfRenderWindow, object, states)
    
    #def draw_circle_shape(self, object, states):
        #try: object = object._sfCircleShape
        #except AttributeError: _arg_error('object', 'CircleShape')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderWindow_drawCircleShape(self._sfRenderWindow, object, states)
    
    #def draw_convex_shape(self, object, states):
        #try: object = object._sfConvexShape
        #except AttributeError: _arg_error('object', 'ConvexShape')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderWindow_drawConvexShape(self._sfRenderWindow, object, states)
    
    #def draw_rectangle_shape(self, object, states):
        #try: object = object._sfRectangleShape
        #except AttributeError: _arg_error('object', 'RectangleShape')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderWindow_drawRectangleShape(self._sfRenderWindow, object, states)
    
    #def draw_vertex_array(self, object, states):
        #try: object = object._sfVertexArray
        #except AttributeError: _arg_error('object', 'VertexArray')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderWindow_drawVertexArray(self._sfRenderWindow, object, states)
    
    #def draw_primitives(self, vertices, vertex_count, type, states):
        #try: vertices = vertices._sfVertex
        #except AttributeError: _arg_error('vertices', 'Vertex')
        #try: states = states._sfRenderStates
        #except AttributeError: _arg_error('states', 'RenderStates')
        #return _sf.sfRenderWindow_drawPrimitives(self._sfRenderWindow, vertices, vertex_count, type, states)
    
    def push_gl_states(self):
        return _sf.sfRenderWindow_pushGLStates(self._sfRenderWindow)
    push_GL_states = push_gl_states
    
    def pop_gl_states(self):
        return _sf.sfRenderWindow_popGLStates(self._sfRenderWindow)
    pop_GL_states = pop_gl_states
    
    def reset_gl_states(self):
        return _sf.sfRenderWindow_resetGLStates(self._sfRenderWindow)
    reset_GL_states = reset_gl_states
    
    def capture(self):
        result = _sf.sfRenderWindow_capture(self._sfRenderWindow)
        return Image._wrap_ptr(result)
    


class Text(Drawable, Transformable):
    REGULAR = _sf.sfTextRegular
    BOLD = _sf.sfTextBold
    ITALIC = _sf.sfTextItalic
    UNDERLINED = _sf.sfTextUnderlined

    _sf_type = 'sfText'
    def __init__(self, string='', font=None, character_size=30):
        self._sfText = _sf.sfText_create()
        self._sfTransformable = self._sfText
        if string: self.string = string
        if font: self.font = font
        self.character_size = character_size

    def get_string(self):
        return _sf.sfText_getUnicodeString(self._sfText) #TODO
    def set_string(self, string):
        string = [ord(c) for c in string]+[0]
        return _sf.sfText_setUnicodeString(self._sfText, string)
    string = property(get_string, set_string)

    def get_font(self):
        result = _sf.sfText_getFont(self._sfText)
        return Font._wrap_ptr(result)
    def set_font(self, font):
        try: font = font._sfFont
        except AttributeError: _arg_error('font', 'Font')
        return _sf.sfText_setFont(self._sfText, font)
    font = property(get_font, set_font)
    
    def get_character_size(self):
        return _sf.sfText_getCharacterSize(self._sfText)
    def set_character_size(self, size):
        return _sf.sfText_setCharacterSize(self._sfText, size)
    character_size = property(get_character_size, set_character_size)
    
    def get_style(self):
        return _sf.sfText_getStyle(self._sfText)
    def set_style(self, style):
        return _sf.sfText_setStyle(self._sfText, style)
    style = property(get_style, set_style)
    
    def get_color(self):
        result = _sf.sfText_getColor(self._sfText)
        return Color._wrap_data(result)
    def set_color(self, color):
        try: color = color._sfColor[0]
        except AttributeError: _arg_error('color', 'Color')
        return _sf.sfText_setColor(self._sfText, color)
    color = property(get_color, set_color)

    def find_character_pos(self, index):
        result = _sf.sfText_findCharacterPos(self._sfText, index)
        return _system.Vector2(result.x, result.y)
    
    def get_local_bounds(self):
        result = _sf.sfText_getLocalBounds(self._sfText)
        return Rect((result.left, result.top), (result.width, result.height))
    local_bounds = property(get_local_bounds)

    def get_global_bounds(self):
        result = _sf.sfTExt_getGlobalBounds(self._sfText)
        return Rect((result.left, result.top), (result.width, result.height))
    global_bounds = property(get_global_bounds)

    def draw(self, target, states):
        try: starget = getattr(target, '_'+target._sf_type)
        except AttributeError: _arg_error('target', 'RenderTarget')
        try: states = states._sfRenderStates
        except AttributeError: _arg_error('states', 'RenderStates')
        return getattr(_sf, target._sf_type+'_drawText')(starget, self._sfText, states)



    

class VertexArray(base.SFMLClass):
    def __init__(self, **kwargs):
        self._sfVertexArray = _sf.sfVertexArray_create()
        if kwargs: self._set(**kwargs)
    
    def copy(self):
        result = _sf.sfVertexArray_copy(self._sfVertexArray)
        return self._wrap_ptr(result)
    
    def __del__(self):
        if self._sf_owned: _sf.sfVertexArray_destroy(self._sfVertexArray)
    
    def get_vertex_count(self):
        return _sf.sfVertexArray_getVertexCount(self._sfVertexArray)
    
    def get_vertex(self, index):
        result = _sf.sfVertexArray_getVertex(self._sfVertexArray, index)
        return Vertex._wrap_ptr(result)
    
    def clear(self):
        return _sf.sfVertexArray_clear(self._sfVertexArray)
    
    def resize(self, vertex_count):
        return _sf.sfVertexArray_resize(self._sfVertexArray, vertex_count)
    
    def append(self, vertex):
        try: vertex = vertex._sfVertex[0]
        except AttributeError: _arg_error('vertex', 'Vertex')
        return _sf.sfVertexArray_append(self._sfVertexArray, vertex)
    
    def set_primitive_type(self, type):
        return _sf.sfVertexArray_setPrimitiveType(self._sfVertexArray, type)
    
    def get_primitive_type(self):
        return _sf.sfVertexArray_getPrimitiveType(self._sfVertexArray)
    
    def get_bounds(self):
        result = _sf.sfVertexArray_getBounds(self._sfVertexArray)
        return Rect((result.left, result.top), (result.width, result.height))


class View(base.SFMLClass):
    def __init__(self, rectangle=None, **kwargs):
        if rectangle is None:
            self._sfView = _sf.sfView_create()
        else:
            try: rectangle = rectangle._sfFloatRect[0]
            except AttributeError: _arg_error('rectangle', 'Rect')
            self._sfView = _sf.sfView_createFromRect(rectangle)
        if kwargs: self._set(**kwargs)
    
    def copy(self):
        result = _sf.sfView_copy(self._sfView)
        return self._wrap_ptr(result)
    
    def __del__(self):
        if self._sf_owned: _sf.sfView_destroy(self._sfView)
    
    def get_center(self):
        result = _sf.sfView_getCenter(self._sfView)
        return _system.Vector2(result.x, result.y)
    def set_center(self, center):
        center = _system.Vector2(center)._sfVector2f[0]
        return _sf.sfView_setCenter(self._sfView, center)
    center = property(get_center, set_center)
    
    def get_size(self):
        result = _sf.sfView_getSize(self._sfView)
        return _system.Vector2(result.x, result.y)
    def set_size(self, size):
        try: size = size._sfVector2f[0]
        except AttributeError: _arg_error('size', 'Vector2\1')
        return _sf.sfView_setSize(self._sfView, size)
    size = property(get_size, set_size)
    
    def get_rotation(self):
        return _sf.sfView_getRotation(self._sfView)
    def set_rotation(self, angle):
        return _sf.sfView_setRotation(self._sfView, angle)
    rotation = property(get_rotation, set_rotation)

    def get_viewport(self):
        result = _sf.sfView_getViewport(self._sfView)
        return Rect((result.left, result.top), (result.width, result.height))
    def set_viewport(self, viewport):
        try: viewport = viewport._sfFloatRect[0]
        except AttributeError: _arg_error('viewport', 'Rect')
        return _sf.sfView_setViewport(self._sfView, viewport)
    viewport = property(get_viewport, set_viewport)

    def reset(self, rectangle):
        try: rectangle = rectangle._sfFloatRect[0]
        except AttributeError: _arg_error('rectangle', 'Rect')
        return _sf.sfView_reset(self._sfView, rectangle)
    
    def move(self, offset):
        try: offset = offset._sfVector2f[0]
        except AttributeError: _arg_error('offset', 'Vector2f')
        return _sf.sfView_move(self._sfView, offset)
    
    def rotate(self, angle):
        return _sf.sfView_rotate(self._sfView, angle)
    
    def zoom(self, factor):
        return _sf.sfView_zoom(self._sfView, factor)


class Glyph(base.SFMLStruct):
    def __init__(self, advance=None, bounds=None, texture_rect=None):
        self._sfGlyph = _ffi.new('sfGlyph*')
        if advance is not None: self.advance = advance
        if bounds: self.bounds = bounds
        if texture_rect: self.texture_rect = texture_rect
    
    @property
    def advance(self):
        return self._sfGlyph.advance
    @advance.setter
    def advance(self, value):
        self._sfGlyph.advance = value
    
    @property
    def bounds(self):
        result = self._sfGlyph.bounds
        return Rect((result.left, result.top), (result.width, result.height))
    @bounds.setter
    def bounds(self, value):
        self._sfGlyph.bounds = value._sfIntRect
    
    @property
    def texture_rect(self):
        result = self._sfGlyph.textureRect
        return Rect((result.left, result.top), (result.width, result.height))
    @texture_rect.setter
    def texture_rect(self, value):
        self._sfGlyph.textureRect = value._sfIntRect
    texture_rectangle = texture_rect
    
    def __repr__(self):
        return self._repr('advance= bounds= texture_rect=')





class Vertex(base.SFMLStruct):
    def __init__(self, position, color, tex_coords):
        self._sfVertex = _ffi.new('sfVertex*')
        self.position = position
        self.color = color
        self.tex_coords = tex_coords
    
    @property
    def position(self):
        result = self._sfVertex.position
        return _system.Vector2(result.x, result.y)
    @position.setter
    def position(self, value):
        value = sf.Vector2(value)._sfVector2f
        self._sfVertex.position = value
    
    @property
    def color(self):
        result = self._sfVertex.color
        return Color._wrap_data(result)
    @color.setter
    def color(self, value):
        try: value = value._sfColor
        except AttributeError: _arg_error('value', 'Color')
        self._sfVertex.color = value._sfColor
    
    @property
    def tex_coords(self):
        result = self._sfVertex.tex_coords
        return _system.Vector2(result.x, result.y)
    @tex_coords.setter
    def tex_coords(self, value):
        value = sf.Vector2(value)._sfVector2f
        self._sfVertex.texCoords = value
    
    def __repr__(self):
        return self._repr('position= color= tex_coords=')




from .graphics_shapes import *



del base