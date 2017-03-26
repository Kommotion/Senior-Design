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


def exec_imagemagick(filepath, line='', filetype=None, filename=None):
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

    command = '"{}" "{}" -monochrome -negate "{}" {}'.format(convert_path, filename, file_out, line)
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
    result = subprocess.run(command, universal_newlines=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)

    return file_out, os.path.isfile(file_out)
