""" Contains all the functions for subprocess calls """
import subprocess
import os


def exec_potrace(line='', filetype=None, filename=None, filepath=None):
    """ Executes a subprocess call that executes imagemagick's convert

    :returns True if passed, False if failed
    """
    if filename is None:
        print(filename, line, filetype)
        return False

    file_in = filename
    temp = filename.split('/')
    file_out = os.path.dirname(filepath)
    file_out = os.path.join(file_out, 'file1{}'.format(filetype))
    command = 'convert {} {} {}'.format(file_in, file_out, line)
    print(command)

    return True
