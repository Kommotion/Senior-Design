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

   ----------------------------------------------------------------------
   This module is for establishing serial communications between the
   host computer and the MCU. It contains functions for getting the
   devices and calling the scripts to stream Gcode to the MCU.
"""

import serial.tools.list_ports
import os
import subprocess
import stream
from utils import parsers


def pre_test():
    """ Runs the pre-test to check if what is required for etching is ready

    This pre-test runs the homing.gcode file, which attemps to home the stage
    first, then home the stage to the origin point of the 3D glass cube
    """
    mcu_serial = parsers.get_from_config('serial_number', os.path.dirname(os.path.realpath(__file__)))
    device_path = _get_device_path(mcu_serial)
    reason = ''

    # Some spaghetti logic up in here
    if device_path is False:
        reason = 'Could not find correct serial port'
        result = False
    else:
        result = _home_stage(device_path)
        if result is False:
            reason = 'Error in streaming'

    ret_dict = dict()
    ret_dict['device'] = device_path
    ret_dict['result'] = result
    ret_dict['reason'] = reason
    return ret_dict


def _get_device_path(mcu_serial=None):
    """ Returns the device path for first match of given serial """
    if mcu_serial is None:
        return False

    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if p.serial_number == mcu_serial:
            return p.device

    return False


def _home_stage(device_path):
    """ Homes the stage to begin etching process """
    homing_gcode = os.path.dirname(os.path.realpath(__file__)) + '\\homing.gcode'
#     streaming_file = os.path.dirname(os.path.realpath(__file__)) + '\\stream.py'
    return stream.start_stream(homing_gcode, device_path)


def full_test(filename, device_path):
    """ Initiates the stream for the given gcode file

    Requires the gcode file to be passed in and the device path
    """
    result = stream.start_stream(filename, device_path)
    if result is False:
        reason = 'CRITICAL ERROR STREAMING GCODE'
    else:
        reason =''

    return result, reason
