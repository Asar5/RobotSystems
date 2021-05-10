#!/usr/bin/env python3

import motor_commands
import interpretor
import sensor_commands
import controller
from rossros import *
# import bus
# from sensor_commands import producer as sensor_function
# from interpretor import consumer_producer as interpreter_function
# from controller import consumer_producer as controller_function

import concurrent.futures
from readerwriterlock import rwlock


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

# while 1:
#     get_sensor_values= sens.get_adc_value()
#     interpreted_sensor_values = inter.process_adc(get_sensor_values)
#     controlled_values = contr.main_control(interpreted_sensor_values, motor)
#     motor.forward(30)
