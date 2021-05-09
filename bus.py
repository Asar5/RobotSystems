#!/usr/bin/env python3


class Bus:
    def __init__(self, msg):
        self.message = msg

    def read(self):
        return self.message

    def write(self, msg):
        self.message = msg


if __name__ == '__main__':
    pass

