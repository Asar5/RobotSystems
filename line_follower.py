#!/usr/bin/env python3

import motor_commands
import interpretor
import sensor_commands
import controller

motor = motor_commands.MotorCommands()
inter = interpretor.Interpretor()
contr = controller.Controller()
sens = sensor_commands.SensorCommands()

while 1:
    get_sensor_values= sens.get_adc_value()
    interpreted_sensor_values = inter.process_adc(get_sensor_values)
    controlled_values = contr.main_control(interpreted_sensor_values, motor)
    motor.forward(30)
