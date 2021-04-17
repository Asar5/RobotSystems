#!/usr/bin/env python3
import time
import logging
from logdecorator  import  log_on_start , log_on_end , log_on_error
logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format , level=logging.INFO ,datefmt ="%H:%M:%S")
logging.getLogger().setLevel(logging.DEBUG)
import numpy as np
import atexit

try:
    from ezblock import *
    from ezblock import __reset_mcu__
    __reset_mcu__()
    time.sleep (0.01)
except ImportError:
    print("This computer does not appear to be a PiCar-X system(/opt/ezblock is not present). Shadowing hardware calls "
          "with substitute functions")
    from sim_ezblock import *

class Interpretor:
    def __init__(self, sensitivity=0.01, polarity=True):
        """
        Initialize how we interpret greyscale sensors for line following
        :param sensitivity: How different  dark/light readings should be?
        :param polarity: Whether the line being followed is darker than the  surroundings (True) or inverse (False)
        """
        self.sensitivity = sensitivity
        self.polarity = polarity

    def process_adc(self, adc_value_list):
        """
        Determine whether the system is centred or to the right/left scaled as a  range of [-1, 1] by processing the
        sensor values
        :param adc_value_list:
        :return: robot_pos: a number between [-1, 1] indicating whether the distance the system is to the right(-), left
        (+) or centred (0) to the line.
        """
        right_sensor = adc_value_list[0]
        centre_sensor = adc_value_list[1]
        left_sensor = adc_value_list[2]
        robot_pos = np.inf

        if abs(centre_sensor - right_sensor) > self.sensitivity:
            logging.debug("Towards right")
            robot_pos = -1

        if abs(centre_sensor - left_sensor) > self.sensitivity:
            logging.debug("Towards left")
            robot_pos = 1

        if (adc_value_list <= self.sensitivity/2).all():
            if self.polarity:
                logging.debug("Centred")
                robot_pos = 0
            else:
                logging.debug("Position unknown")
                robot_pos = np.inf

        return robot_pos
