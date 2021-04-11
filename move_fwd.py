import picarx_improved
import numpy as  np
import time

picarx_improved.set_dir_servo_angle(-10)
time.sleep(5)
picarx_improved.forward(50)
i = 0
while(i < 20000):
    print(i)
    i+=1
picarx_improved.stop()
time.sleep(2)
picarx_improved.set_dir_servo_angle(25)
time.sleep(5)
picarx_improved.backward(50)
i = 0
while(i < 20000):
    print(i)
    i+=1
picarx_improved.stop()
time.sleep(2)
picarx_improved.set_dir_servo_angle(0)
time.sleep(2)
#picarx_improved.set_dir_servo_angle(10)
#time.sleep(2)
#picarx_improved.set_dir_servo_angle(-20)
#time.sleep(2)
#picarx_improved.set_dir_servo_angle(0)

