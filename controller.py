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
import bus

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


def producer(control_bus, delay_s):
    control = Controller()
    motor = motor_commands.MotorCommands()
    while 1:
        get_val = control_bus.read()
        angle = control.main_control(get_val, motor)
        time.sleep(delay_s)


def consumer_producer(control_bus, delay_s):
    control = Controller()
    motor = motor_commands.MotorCommands()
    while(1):
        get_val = control_bus.read()
        angle = control.main_control(get_val, motor)
        control_bus.write(angle)
        time.sleep(delay_s)
