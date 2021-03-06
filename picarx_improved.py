import time
import logging
from logdecorator  import  log_on_start , log_on_end , log_on_error
logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format , level=logging.INFO ,datefmt ="%H:%M:%S")
logging.getLogger().setLevel(logging.DEBUG)
import numpy as np

try:
    from  ezblock  import *
    from ezblock import __reset_mcu__
    __reset_mcu__()
    time.sleep (0.01)
except  ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  callswith  substitute  functions ")
    from  sim_ezblock  import *

import  atexit

PERIOD = 4095
PRESCALER = 10
TIMEOUT = 0.02

dir_servo_pin = Servo(PWM('P2'))
camera_servo_pin1 = Servo(PWM('P0'))
camera_servo_pin2 = Servo(PWM('P1'))
left_rear_pwm_pin = PWM("P13")
right_rear_pwm_pin = PWM("P12")
left_rear_dir_pin = Pin("D4")
right_rear_dir_pin = Pin("D5")
length = 0.093 #mts
breadth = 0.11 #mts

S0 = ADC('A0')
S1 = ADC('A1')
S2 = ADC('A2')

Servo_dir_flag = 1
#Servo Direction calibration
dir_cal_value = -17
cam_cal_value_1 = 0
cam_cal_value_2 = 0
motor_direction_pins = [left_rear_dir_pin, right_rear_dir_pin]
motor_speed_pins = [left_rear_pwm_pin, right_rear_pwm_pin]
cali_dir_value = [1, -1]
cali_speed_value = [0, 0]
curr_servo_angle = 0

for pin in motor_speed_pins:
    pin.period(PERIOD)
    pin.prescaler(PRESCALER)


#@log_on_start(logging.DEBUG , "{asctime:s}: Message  when  function  starts ")
#@log_on_error(logging.DEBUG , "{asctime:s}: Message  when  function  encountersan error  before  completing ")
#@log_on_end(logging.DEBUG , "{asctime:s}: Message  when  function  endssuccessfully ")
def set_motor_speed(motor, speed):
    global cali_speed_value,cali_dir_value
    motor -= 1
    if speed >= 0:
        direction = 1 * cali_dir_value[motor]
    elif speed < 0:
        direction = -1 * cali_dir_value[motor]
    speed = abs(speed)
    #if speed != 0:
        #speed = int(speed /2 ) + 50
    speed = speed - cali_speed_value[motor]
    if direction < 0:
        motor_direction_pins[motor].high()
        motor_speed_pins[motor].pulse_width_percent(speed)
    else:
        motor_direction_pins[motor].low()
        motor_speed_pins[motor].pulse_width_percent(speed)

def motor_speed_calibration(value):
    global cali_speed_value,cali_dir_value
    cali_speed_value = value
    if value < 0:
        cali_speed_value[0] = 0
        cali_speed_value[1] = abs(cali_speed_value)
    else:
        cali_speed_value[0] = abs(cali_speed_value)
        cali_speed_value[1] = 0

def motor_direction_calibration(motor, value):
    # 0: positive direction
    # 1:negative direction
    global cali_dir_value
    motor -= 1
    if value == 1:
        cali_dir_value[motor] = -1*cali_dir_value[motor]


def dir_servo_angle_calibration(value):
    global dir_cal_value
    dir_cal_value = value
    set_dir_servo_angle(dir_cal_value)
    # dir_servo_pin.angle(dir_cal_value)

def set_dir_servo_angle(value):
    global dir_cal_value, curr_servo_angle
    dir_servo_pin.angle(value+dir_cal_value)
    curr_servo_angle = value

def camera_servo1_angle_calibration(value):
    global cam_cal_value_1
    cam_cal_value_1 = value
    set_camera_servo1_angle(cam_cal_value_1)
    # camera_servo_pin1.angle(cam_cal_value)

def camera_servo2_angle_calibration(value):
    global cam_cal_value_2
    cam_cal_value_2 = value
    set_camera_servo2_angle(cam_cal_value_2)
    # camera_servo_pin2.angle(cam_cal_value)

def set_camera_servo1_angle(value):
    global cam_cal_value_1
    camera_servo_pin1.angle(-1 *(value+cam_cal_value_1))

def set_camera_servo2_angle(value):
    global cam_cal_value_2
    camera_servo_pin2.angle(-1 * (value+cam_cal_value_2))

def get_adc_value():
    adc_value_list = []
    adc_value_list.append(S0.read())
    adc_value_list.append(S1.read())
    adc_value_list.append(S2.read())
    return adc_value_list

def set_power(speed):
    set_motor_speed(1, speed)
    set_motor_speed(2, speed) 

def backward(speed):
    logging.debug("BACK")
    if curr_servo_angle == 0:
        set_motor_speed(1, speed)
        set_motor_speed(2, speed)
    else:
        find_turn_speed(speed)

#@log_on_start(logging.DEBUG , "{asctime:s}: Moving forward")
#@log_on_error(logging.DEBUG , "{asctime:s}: Error on executing forward")
#@log_on_end(logging.DEBUG , "{asctime:s}: Finished executing forward")
def forward(speed):
    logging.debug("FRONT")
    if curr_servo_angle == 0:
        set_motor_speed(1, -1*speed)
        set_motor_speed(2, -1*speed)
    else:
        find_turn_speed(-1*speed)


def find_turn_speed(speed):
    global length, curr_servo_angle, breadth
    rev_dir =  False
    if speed < 0:
        rev_dir = True
        speed = -speed
    turn_radius = length/abs(np.tan(curr_servo_angle))
    speed_in = speed*abs((turn_radius - breadth/2))*1  
    speed_out = speed*abs((turn_radius + breadth/2))*1  
    if  speed_in < speed_out:
        c = speed_in
        speed_in = speed_out
        speed_out = c
    if speed_in < 35:
        speed_in = 35
    if  speed_out < 40:
        speed_out = 40
    if rev_dir:
        speed_in = -speed_in
        speed_out = -speed_out

    if curr_servo_angle > 0:
        set_motor_speed(1, speed_in)
        set_motor_speed(2, speed_out)
    else:
        set_motor_speed(2, speed_in)
        set_motor_speed(1, speed_out)
    logging.debug("turn radius %s: ", turn_radius)
    logging.debug("servo angle %s: ",curr_servo_angle)
    logging.debug("speed in %s: ",speed_in)
    logging.debug("speed out %s: ",speed_out)


@atexit.register
@log_on_start(logging.DEBUG , "Exiting")
@log_on_error(logging.DEBUG , "Error on exit")
@log_on_end(logging.DEBUG , "Clean Exit")
def stop():
    logging.debug("hello")
    set_motor_speed(1, 0)
    set_motor_speed(2, 0)


def Get_distance():
    timeout=0.01
    trig = Pin('D8')
    echo = Pin('D9')

    trig.low()
    time.sleep(0.01)
    trig.high()
    time.sleep(0.000015)
    trig.low()
    pulse_end = 0
    pulse_start = 0
    timeout_start = time.time()
    while echo.value()==0:
        pulse_start = time.time()
        if pulse_start - timeout_start > timeout:
            return -1
    while echo.value()==1:
        pulse_end = time.time()
        if pulse_end - timeout_start > timeout:
            return -2
    during = pulse_end - pulse_start
    cm = round(during * 340 / 2 * 100, 2)
    #print(cm)
    return cm

def move_back_forth(angle=0, dist=1.0, direction=forward, speed=50, times=1):
    for i in range(0, times):
        set_dir_servo_angle(angle)
        direction(speed)
        time.sleep(dist)
    #    stop()
    set_dir_servo_angle(0)
    stop()

def parallel_park(side):
    angle = 45
    if side == 'left':
        angle = -angle
        spd = 30
        dst = 1.5
    else:
        angle = 20
        spd = 20
        dst = 0.5
    move_back_forth(angle=0, dist=0.5, direction=forward, speed=spd)
    move_back_forth(angle=angle, direction=backward, speed=spd)
    move_back_forth(angle=-angle, dist=dst, direction=backward, speed=spd)
    move_back_forth(speed=spd)

def k_turn(side):
    #move_back_forth(angle=50, direction=forward)
    if side == 'left':
        angle = -40
        spd = 50
    else:
        angle = 50
        spd = 20
    move_back_forth(angle=angle, dist=2.0, direction=forward, speed=spd)
    move_back_forth(angle=-angle, dist=2.5, direction=backward, speed=spd)
    move_back_forth(angle=angle, dist=2.8, direction=forward, speed=spd)


def test():
    # dir_servo_angle_calibration(-10) 
    set_dir_servo_angle(-40)
    # time.sleep(1)
    # set_dir_servo_angle(0)
    # time.sleep(1)
    # set_motor_speed(1, 1)
    # set_motor_speed(2, 1)
    # camera_servo_pin.angle(0)


# if __name__ == "__main__":
#     try:
#         # dir_servo_angle_calibration(-10) 
#         while 1:
#             test()
#     finally: 
#         stop()
