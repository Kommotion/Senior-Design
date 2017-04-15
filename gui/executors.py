"""
   Copyright 2017 Nicolas Ramirez

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
""" Contains all the functions for subprocess calls """
import subprocess
import os
from utils import parsers
from tkinter import messagebox


def exec_imagemagick(filepath, negate, line='', filetype=None, filename=None):
    """ Executes a subprocess call that executes imagemagick's convert

    :returns True if passed, False if failed
    """
    if filename is None:
        return '', False

    line = line if line is True else ''
    name = filename.split('\\')
    name = name[len(name)-1].split('.')[0]
    file_out = os.path.join(filepath, '{}{}'.format(name, filetype))
    convert_path = parsers.get_from_config('convert_path', os.path.dirname(os.path.realpath(__file__)))

    if not convert_path:
        return '', False

    if os.path.isfile(file_out):
        os.remove(file_out)

    if negate:
        command = '"{}" "{}" -monochrome -negate "{}" {}'.format(convert_path, filename, file_out, line)
    else:
        command = '"{}" "{}" -monochrome "{}" {}'.format(convert_path, filename, file_out, line)
    print(command)
    result = subprocess.run(command, universal_newlines=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

    return file_out, os.path.isfile(file_out)


def exec_potrace(filepath, line='', filename=None):
    """ Executes a subprocess call that executes imagemagick's convert

    :returns True if passed, False if failed
    """
    if filename is None:
        return '', False

    line = line if line is True else ''
    name = filename.split('\\')
    name = name[len(name)-1].split('.')[0]
    file_out = os.path.join(filepath, '{}{}'.format(name, '.svg'))
    potrace_path = parsers.get_from_config('potrace_path', os.path.dirname(os.path.realpath(__file__)))

    if not potrace_path:
        return '', False

    if os.path.isfile(file_out):
        os.remove(file_out)

    command = '"{}" -s "{}" -o "{}" --flat {}'.format(potrace_path, filename, file_out, line)
    result = subprocess.run(command, universal_newlines=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

    return file_out, os.path.isfile(file_out)

def stl_conversion(root, filename, filepath, extrusion):
    """ Converts the SVG file to a STL file by using the FreeCad script

    :return:  True or False, depending on pass
    """
    name = filename.split('\\')
    name = name[len(name)-1].split('.')[0]
    file_out = os.path.join(filepath, '{}.stl'.format(name))

    if os.path.isfile(file_out):
        os.remove(file_out)

    path = os.path.dirname(os.path.realpath(__file__))
    script = '{}\\stl.py'.format(path)

    command = 'python2 "{}" -i "{}" -o "{}" -e {}'.format(script, filename, file_out, extrusion)
    messagebox.showinfo('Caution', 'This process may take a few minutes to run.\nPress OK to continue')

    # Terrible exception handling but there is a bug that occasionally occurs
    # This bug has nothing to do with STL creation process and only with the
    # STDOUT/STDERR handling so it can be safely ignored
    try:
        result = subprocess.run(command, universal_newlines=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    except Exception as e:
        print(e)
        pass

    return file_out, os.path.isfile(file_out)


def execute_slic3r(filename, filepath, x ,y):
    """ Slices the STL object into Gcode using Slic3r

    In order for this to work, path to slic3r-console.exe needs to be provided in the config.json file
    """
    name = filename.split('\\')
    name = name[len(name) - 1].split('.')[0]
    file_out = os.path.join(filepath, '{}.gcode'.format(name))

    x = 25.4 * x / 2
    y = 25.4 * y / 2

    if os.path.isfile(file_out):
        os.remove(file_out)

    slicer = parsers.get_from_config('slic3r_path', os.path.dirname(os.path.realpath(__file__)))
    config = os.path.dirname(os.path.realpath(__file__)) + '\\config.ini'

    command = '"{}" --load "{}" "{}" --print-center {},{}'.format(slicer, config, filename, x, y)
    print(command)
    result = subprocess.run(command, universal_newlines=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE,
                            shell=True)

    return file_out, os.path.isfile(file_out)


def execute_scale_stl(filename, filepath, x, y, z):
    """ Executes the scaling of an STL file via Freecad """
    path = os.path.dirname(os.path.realpath(__file__))
    script = '{}\\stl.py'.format(path)

    x = x * 25.4
    y = y * 25.4
    z = z * 25.4
    print(x, y, z)

    command = 'python2 "{}" -i "{}" -o "None" -s 1 -x {} -y {} -z {}'.format(script, filename, x, y, z)
    print(command)

    # Terrible exception handling but there is a bug that occasionally occurs
    # This bug has nothing to do with STL creation process and only with the
    # STDOUT/STDERR handling so it can be safely ignored
    try:
        result = subprocess.run(command, universal_newlines=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE,
                                shell=True)
    except Exception as e:
        print(e)
        pass

    return True
