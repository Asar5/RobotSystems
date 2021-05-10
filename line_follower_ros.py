#!/usr/bin/env python3

import motor_commands
import interpretor
import sensor_commands
import controller
from rossros import *


motor = motor_commands.MotorCommands()
inter = interpretor.Interpretor()
contr = controller.Controller()
sens = sensor_commands.SensorCommands()
sensor_values_bus = Bus(name="Sensor Bus")
interpreter_bus = Bus(name= "Inter Bus")
controller_bus = Bus("Control Bus")

sensor_function = Producer(sens.get_adc_value, sensor_values_bus, delay=0.2, name="Sensor Producer")
interpreter_function = ConsumerProducer(inter.process_adc, sensor_values_bus, interpreter_bus, delay=0.5,
                                        name="Interpreter Consumer Producer")
control_function = Consumer(contr.main_control, interpreter_bus, delay=0.3, name="Controller Consumer")

sensor_delay = 1
interpreter_delay = 1
controller_delay = 1


runConcurrently([sensor_function, interpreter_function, control_function])

