#!/usr/bin/env python3
import time
import logging
from logdecorator  import  log_on_start , log_on_end , log_on_error
logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format , level=logging.INFO ,datefmt ="%H:%M:%S")
logging.getLogger().setLevel(logging.DEBUG)
import numpy as np
import atexit
import bus

try:
    from  ezblock  import *
    from ezblock import __reset_mcu__
    __reset_mcu__()
    time.sleep (0.01)
except ImportError:
    print("This computer does not appear to be a PiCar-X system(/opt/ezblock is not present). Shadowing hardware calls "
          "with substitute functions")
    from sim_ezblock import *


class SensorCommands:
    def __init__(self):
        self.s0 = ADC('A0')
        self.s1 = ADC('A1')
        self.s2 = ADC('A2')

    def get_adc_value(self):
        adc_value_list = [self.s0.read(), self.s1.read(), self.s2.read()]
        return adc_value_list


def producer(sensor_bus, delay_s):
    sensor = SensorCommands()
    while(1):
        set_val = sensor.get_adc_value()
        sensor_bus.write(set_val)
        time.sleep(delay_s)
