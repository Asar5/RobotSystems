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
    from  ezblock  import *
    from ezblock import __reset_mcu__
    __reset_mcu__()
    time.sleep (0.01)
except  ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  callswith  substitute  functions ")
    from  sim_ezblock  import *


class MotorCommands:
    def __init__(self):
        self.PERIOD = 4095
        self.PRESCALER = 10
        self.TIMEOUT = 0.02

        self.dir_servo_pin = Servo(PWM('P2'))
        self.camera_servo_pin1 = Servo(PWM('P0'))
        self.camera_servo_pin2 = Servo(PWM('P1'))
        self.left_rear_pwm_pin = PWM("P13")
        self.right_rear_pwm_pin = PWM("P12")
        self.left_rear_dir_pin = Pin("D4")
        self.right_rear_dir_pin = Pin("D5")
        self.length = 0.093  # mts
        self.breadth = 0.11  # mts

        self.Servo_dir_flag = 1
        self.dir_cal_value = -17
        self.cam_cal_value_1 = 0
        self.cam_cal_value_2 = 0
        self.motor_direction_pins = [self.left_rear_dir_pin, self.right_rear_dir_pin]
        self.motor_speed_pins = [self.left_rear_pwm_pin, self.right_rear_pwm_pin]
        self.cali_dir_value = [1, -1]
        self.cali_speed_value = [0, 0]
        self.curr_servo_angle = 0

        for pin in self.motor_speed_pins:
            pin.period(self.PERIOD)
            pin.prescaler(self.PRESCALER)

        atexit.register(self.cleanup)

    def set_motor_speed(self, motor, speed):
        motor -= 1
        if speed >= 0:
            direction = 1 * self.cali_dir_value[motor]
        else:
            direction = -1 * self.cali_dir_value[motor]
        speed = abs(speed)
        # if speed != 0:
        # speed = int(speed /2 ) + 50
        speed = speed - self.cali_speed_value[motor]
        if direction < 0:
            self.motor_direction_pins[motor].high()
            self.motor_speed_pins[motor].pulse_width_percent(speed)
        else:
            self.motor_direction_pins[motor].low()
            self.motor_speed_pins[motor].pulse_width_percent(speed)
        pass

    def motor_speed_calibration(self, value):
        # Not  sure about this line ->self.cali_speed_value = value
        if value < 0:
            self.cali_speed_value[0] = 0
            self.cali_speed_value[1] = abs(value)
        else:
            self.cali_speed_value[0] = abs(value)
            self.cali_speed_value[1] = 0

    def motor_direction_calibration(self, motor, value):
        # 0: positive direction
        # 1:negative direction
        motor -= 1
        if value == 1:
            self.cali_dir_value[motor] = -1 * self.cali_dir_value[motor]

    def dir_servo_angle_calibration(self, value):
        self.dir_cal_value = value
        self.set_dir_servo_angle(self.dir_cal_value)

    def set_dir_servo_angle(self, value):
        self.dir_servo_pin.angle(value + self.dir_cal_value)
        self.curr_servo_angle = value

    def camera_servo1_angle_calibration(self, value):
        self.cam_cal_value_1 = value
        self.set_camera_servo1_angle(self.cam_cal_value_1)
        # camera_servo_pin1.angle(cam_cal_value)

    def camera_servo2_angle_calibration(self, value):
        self.cam_cal_value_2 = value
        self.set_camera_servo2_angle(self.cam_cal_value_2)
        # camera_servo_pin2.angle(cam_cal_value)

    def set_camera_servo1_angle(self, value):
        self.camera_servo_pin1.angle(-1 *(value+self.cam_cal_value_1))

    def set_camera_servo2_angle(self, value):
        self.camera_servo_pin2.angle(-1 * (value+self.cam_cal_value_2))

    def set_power(self, speed):
        self.set_motor_speed(1, speed)
        self.set_motor_speed(2, speed)

    def backward(self, speed):
        logging.debug("BACK")
        if self.curr_servo_angle == 0:
            self.set_motor_speed(1, speed)
            self.set_motor_speed(2, speed)
        else:
            self.find_turn_speed(speed)

    # @log_on_start(logging.DEBUG , "{asctime:s}: Moving forward")
    # @log_on_error(logging.DEBUG , "{asctime:s}: Error on executing forward")
    # @log_on_end(logging.DEBUG , "{asctime:s}: Finished executing forward")
    def forward(self, speed):
        logging.debug("FRONT")
        if self.curr_servo_angle == 0:
            self.set_motor_speed(1, -1 * speed)
            self.set_motor_speed(2, -1 * speed)
        else:
            self.find_turn_speed(-1 * speed)

    def find_turn_speed(self, speed):
        rev_dir = False
        if speed < 0:
            rev_dir = True
            speed = -speed
        turn_radius = self.length / abs(np.tan(self.curr_servo_angle))
        speed_in = speed * abs((turn_radius - self.breadth / 2)) * 1
        speed_out = speed * abs((turn_radius + self.breadth / 2)) * 1
        if speed_in < speed_out:
            c = speed_in
            speed_in = speed_out
            speed_out = c
        if speed_in < 35:
            speed_in = 35
        if speed_out < 40:
            speed_out = 40
        if rev_dir:
            speed_in = -speed_in
            speed_out = -speed_out

        if self.curr_servo_angle > 0:
            self.set_motor_speed(1, speed_in)
            self.set_motor_speed(2, speed_out)
        else:
            self.set_motor_speed(2, speed_in)
            self.set_motor_speed(1, speed_out)
        logging.debug("turn radius %s: ", turn_radius)
        logging.debug("servo angle %s: ", self.curr_servo_angle)
        logging.debug("speed in %s: ", speed_in)
        logging.debug("speed out %s: ", speed_out)

    @log_on_start(logging.DEBUG, "Exiting")
    @log_on_error(logging.DEBUG, "Error on exit")
    @log_on_end(logging.DEBUG, "Clean Exit")
    def stop(self):
        logging.debug("Stopping Motors")
        self.set_motor_speed(1, 0)
        self.set_motor_speed(2, 0)

    def cleanup(self):
        self.stop()


if __name__ == '__main__':
    my_commands = MotorCommands()
    print(my_commands.forward(40))


