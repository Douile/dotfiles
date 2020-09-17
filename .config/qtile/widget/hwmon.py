# -*- coding:utf-8 -*-

# Copyright (c) 2020 Douile
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import os.path

from libqtile.widget import base

from libqtile.log_utils import logger
from libqtile.utils import (
    UnixCommandNotFound,
    catch_exception_and_warn,
)

class ThermalHwmon(base.InLoopPollText):
    """Widget to display thermal information

    To get a list of tag_sensors use `ls /sys/class/hwmon/hwmon**/temp*_input` in your terminal
    The sensor tag name is the part before _input e.g. temp1
    """
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('update_interval', 1, 'Update interval in seconds'),
        ('tag_sensor', None, 'Tag of temperature sensor'),
        ('threshold', 70 , 'If temp is above change to foreground_alert'),
        ('foreground_alert', 'ff0000', 'Foreground colour alert'),
        ('hwmon_dir', '/sys/class/hwmon', 'Path for hwmon devices'),
        ('format', '{temp:02.2f}C', 'Formatting string'),
    ]

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(ThermalHwmon.defaults)

        sensors = self.get_temp_sensors()
        self.sensor = None
        if self.tag_sensor is not None and sensors[self.tag_sensor] is not None:
            self.sensor = sensors[self.tag_sensor]
        else:
            for key in sensors:
                self.sensor = sensors[key]
                break

        self.foreground_normal = self.foreground

    @catch_exception_and_warn(warning=UnixCommandNotFound, excepts=FileNotFoundError)
    def get_temp_sensors(self):
        """Enumerates the names of all hwmon temp sensors"""
        sensors = {}

        hwmons = os.listdir(self.hwmon_dir)
        for hwmon in hwmons:
            for dev in os.listdir(os.path.join(self.hwmon_dir,hwmon)):
                if dev.endswith('_input'):
                    sensors[dev[:-6]] = os.path.join(self.hwmon_dir,hwmon,dev)

        logger.info(sensors)
        return sensors

    @catch_exception_and_warn(warning=UnixCommandNotFound, excepts=FileNotFoundError)
    def get_temp(self, sensor):
        """Gets the temperature from given temp input (in degrees)"""
        temp = None
        with open(sensor, 'r') as sensor_input:
            temp = sensor_input.read()
        if temp is not None:
            return int(temp)/1000

    def poll(self):
        if self.sensor is None:
            return False
        temp = self.get_temp(self.sensor)
        text = "N/A"
        if temp is not None:
            text = self.format.format_map({ 'temp': temp })

            if temp > self.threshold:
                self.layout.colour = self.foreground_alert
            else:
                self.layout.colour = self.foreground_normal

        return text
