#!/usr/bin/env python3

import motor_commands
import interpretor
import sensor_commands
import controller
import bus
from sensor_commands import producer as sensor_function
from interpretor import consumer_producer as interpreter_function
from controller import consumer_producer as controller_function


import concurrent.futures
from readerwriterlock import rwlock

motor = motor_commands.MotorCommands()
inter = interpretor.Interpretor()
contr = controller.Controller()
sens = sensor_commands.SensorCommands()
sensor_values_bus = bus.Bus()
interpreter_bus = bus.Bus()
controller_bus = bus.Bus()

sensor_delay = 1
interpreter_delay = 1
controller_delay = 1

with concurrent.futures.ThreadPoolExecutor(max_workers =2) as executor:
    eSensor = executor.submit(sensor_function ,sensor_values_bus , sensor_delay)
    eInterpreter = executor.submit(interpreter_function ,sensor_values_bus , interpreter_bus ,interpreter_delay)

eSensor.result()
eInterpreter.result()

# while 1:
#     get_sensor_values= sens.get_adc_value()
#     interpreted_sensor_values = inter.process_adc(get_sensor_values)
#     controlled_values = contr.main_control(interpreted_sensor_values, motor)
#     motor.forward(30)
