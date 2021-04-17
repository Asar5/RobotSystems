#!/usr/bin/env python3
import time
import logging
from logdecorator  import  log_on_start , log_on_end , log_on_error
logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format , level=logging.INFO ,datefmt ="%H:%M:%S")
logging.getLogger().setLevel(logging.DEBUG)
import numpy as np
import atexit
import motor_commands
import interpretor
import sensor_commands


try:
    from ezblock import *
    from ezblock import __reset_mcu__
    __reset_mcu__()
    time.sleep (0.01)
except ImportError:
    print("This computer does not appear to be a PiCar-X system(/opt/ezblock is not present). Shadowing hardware calls "
          "with substitute functions")
    from sim_ezblock import *


class Controller:
    def __init__(self, scaling=1.0):
        self.scaling = scaling

    def main_control(self, value, motor):
        angle = self.scaling*value
        motor.set_dir_servo_angle(angle)
        return angle
