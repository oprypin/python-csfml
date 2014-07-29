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

import os.path
import re

from cffi import FFI


inc_path = '/usr/include'


src = ['''
typedef unsigned long sfWindowHandle;
typedef int size_t;
typedef int wchar_t;
''']

visited = set()
def visit_header(file_path):
    if file_path in visited:
        return
    visited.add(file_path)
    with open(os.path.join(inc_path, file_path)) as src_file:
        #src.append('\n\n;;;;enum {};;;;\n\n'.format(file_path[:-2].replace('/', '_')))
        for line in src_file:
            if '//' in line:
                line = line.split('//')[0]
            line = line.strip()
            if not line:
                continue
            if line.startswith('#include'):
                m = re.match(r'#include <(SFML/.+\.h)>', line)
                if m and not m.group(1).endswith('Export.h'):
                    visit_header(m.group(1))
            if line.startswith('#') or line.startswith('//'):
                continue
            if '__int64' in line or 'HWND__' in line:
                continue
            if line.startswith('typedef') and line.rstrip(';').endswith('sfWindowHandle'):
                continue
            if '_API' in line:
                line = re.sub(r'CSFML_[A-Z]+_API ?', '', line)
            line = line.replace('(void)', '()')
            if '<<' in line:
                line = re.sub(r'1 *<< *([0-9]+)', lambda m: str(1<<int(m.group(1))), line)
            line = line.replace('sfTitlebar | sfResize | sfClose', '7')
            src.append(line)
    src.append('\n')

module_names = ['system', 'window', 'graphics', 'audio', 'network']

__all__ = ['ffi']

for m in module_names:
    visit_header('SFML/{}.h'.format(m.capitalize()))

del visited

src = '\n'.join(src)


ffi = FFI()

ffi.cdef(src)

#c = ffi.verify('\n'.join(headers), libraries=['csfml-{}'.format(m) for m in module_names])

del src