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
    def __init__(self, sensitivity=750, polarity=True):
        """
        Initialize how we interpret greyscale sensors for line following
        :param sensitivity: How different  dark/light readings should be?
        :param polarity: Whether the line being followed is darker than the  surroundings (True) or inverse (False)
        """
        self.sensitivity = sensitivity
        self.polarity = polarity

    def convert_to_discrete(self, adc_value_list):
        """
        Determine whether the system is centred or to the right/left scaled as a  range of [-1, 1] by processing the
        sensor values
        :param adc_value_list:
        :return: robot_pos: a number between [-1, 1] indicating whether the distance the system is to the right(-), left
        (+) or centred (0) to the line.
        """
        left_sensor = adc_value_list[0]
        centre_sensor = adc_value_list[1]
        right_sensor = adc_value_list[2]

        detect_left_edge = left_sensor - centre_sensor
        detect_right_edge = right_sensor - centre_sensor

        if abs(detect_left_edge) > self.sensitivity:
            if detect_left_edge < 0:
                discrete_left = False
            else:
                discrete_left = True
            discrete_centre = not discrete_left

            if abs(detect_right_edge) > self.sensitivity:
                discrete_right = not discrete_centre
            else:
                discrete_right = discrete_centre
        else:
            if abs(detect_right_edge) > self.sensitivity:
                if detect_right_edge < 0:
                    discrete_right = False
                else:
                    discrete_right = True
                discrete_centre = not discrete_right
                discrete_left = discrete_centre
            else:
                if left_sensor > self.sensitivity:
                    discrete_left = True
                else:
                    discrete_left = False
                discrete_right = discrete_left
                discrete_centre = discrete_left

        return [discrete_left,  discrete_centre, discrete_right]

    def process_adc(self, adc_list):
        discrete_list = self.convert_to_discrete(adc_list)
        robot_pos = np.inf
        if discrete_list == [False, False, False]:
            if self.polarity:
                print("Move straight; Polarity: {}; Values: {}".format(self.polarity, discrete_list))
                robot_pos = 0
            else:
                print("Move in circle; Polarity: {}; Values: {}".format(self.polarity, discrete_list))
                robot_pos = np.inf
        elif discrete_list == [False, False, True]:
            if self.polarity:
                print("Move slightly left; Polarity: {}; Values: {}".format(self.polarity, discrete_list))
                robot_pos = -0.5
            else:
                print("Move extreme right; Polarity: {}; Values: {}".format(self.polarity, discrete_list))
                robot_pos = 1.0
        elif discrete_list == [False, True, False] or discrete_list == [True, False, True]:
            print("Move straight; Polarity: {}; Values: {}".format(self.polarity, discrete_list))
            robot_pos = 0
        elif discrete_list == [False, True, True]:
            if self.polarity:
                print("Move extreme left; Polarity: {}; Values: {}".format(self.polarity, discrete_list))
                robot_pos = -1.0
            else:
                print("Move slight right; Polarity: {}; Values: {}".format(self.polarity, discrete_list))
                robot_pos = 0.5

        elif discrete_list == [True, False, False]:
            if self.polarity:
                print("Move slight right; Polarity: {}; Values: {}".format(self.polarity, discrete_list))
                robot_pos = 0.5
            else:
                print("Move extreme left; Polarity: {}; Values: {}".format(self.polarity, discrete_list))
                robot_pos = -1.0
        elif discrete_list == [True, True, False]:
            if self.polarity:
                print("Move extreme right; Polarity: {}; Values: {}".format(self.polarity, discrete_list))
                robot_pos = 1.0
            else:
                print("Move slight left; Polarity: {}; Values: {}".format(self.polarity, discrete_list))
                robot_pos = -0.5
        elif discrete_list == [True, True, True]:
            if self.polarity:
                print("Move in  circle; Polarity: {}; Values: {}".format(self.polarity, discrete_list))
                robot_pos = np.inf
            else:
                print("Move straight; Polarity: {}; Values: {}".format(self.polarity, discrete_list))
                robot_pos = 0
        return robot_pos

if __name__ == '__main__':
    # import sensor_commands

    # s_r = sensor_commands.SensorCommands()
    # int_sense = Interpretor(sensitivity=750, polarity=False)
    int_sense = Interpretor(sensitivity=750, polarity=True)

    # while(1):
        # val = s_r.get_adc_value()
    retval = int_sense.process_adc([10, 8, 1500])
    print(retval)
    # time.sleep(3)

