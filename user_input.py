#!/usr/bin/env python3
import picarx_improved as pic


def get_back_forth():
    print("Enter 'f' for forward")
    print("Enter 'b' for backward ")
    print("Enter 'x' for exit")
    dir = input("What direction do  you want to move in?")

    if dir == 'f':
        direction = pic.forward
    elif dir == 'b':
        direction = pic.backward
    elif dir == 'x':
        exit()
    else:
        print("Wrong input, Try again")
        exit()

    print("Enter - integer for left")
    print("Enter + integer for right")
    print("Enter 'x' for exit")
    angle = input("What angle do you want to move at?")
    try:
        angle = int(angle)
    except TypeError:
        if angle == 'x':
            exit()
        print("Wrong input, Try again")
        exit()
    pic.move_back_forth(angle=angle, direction=direction)


def get_pp(man_type):
    print("Enter 'l' for left")
    print("Enter 'r' for right")
    print("Enter 'x' for exit")
    side_input = input("What side do you want to maneuver in")
    if side_input == 'l':
        side = 'left'
    elif side_input == 'r':
        side = 'right'
    elif side_input == 'x':
        exit()
    else:
        print("Wrong input, Try again")
        exit()
    man_type(side=side)


if __name__ == '__main__':
    while(1):
        print("Enter '1' for forward/backward")
        print("Enter '2' for parallel parking")
        print("Enter '3' for k-turn")
        print("Enter 'x' for exit")
        man_num = input("What maneuver do you want to perform?")
        if man_num == 'x':
            break
        elif man_num == '1':
            get_back_forth()
        elif man_num == '2':
            get_pp(pic.parallel_park)
        elif man_num == '3':
            get_pp(pic.k_turn)
