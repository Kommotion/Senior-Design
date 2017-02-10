""" Contains all the functions for subprocess calls """
import subprocess
import os
from utils import parsers


def exec_potrace(filepath, line='', filetype=None, filename=None):
    """ Executes a subprocess call that executes imagemagick's convert

    :returns True if passed, False if failed
    """
    if filename is None:
        return False

    line = line if line is True else ''
    name = filename.split('\\')
    name = name[len(name)-1].split('.')[0]
    file_out = os.path.join(filepath, '{}{}'.format(name, filetype))
    convert_path = parsers.get_from_config('convert_path', os.path.dirname(os.path.realpath(__file__)))

    if os.path.isfile(convert_path):
        os.remove(convert_path)

    command = '{} {} {} {}'.format(convert_path, filename, file_out, line)
    result = subprocess.run(command, universal_newlines=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

    return os.path.isfile(file_out)
