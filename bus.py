#!/usr/bin/env python3

from readerwriterlock import rwlock


class Bus:
    def __init__(self):
        self.message = None
        self.lock = rwlock.RWLockWriteD()

    def read(self):
        with self.lock.gen_rlock():
            msg = self.message
        return msg

    def write(self, msg):
        with self.lock.gen_wlock():
            self.message = msg


if __name__ == '__main__':
    # !/usr/bin/env python3

    import motor_commands
    import interpretor
    import sensor_commands
    import controller
    from sensor_commands import producer as sensor_function
    from interpretor import consumer_producer as interpreter_function
    from controller import consumer_producer as controller_function

    import concurrent.futures

    motor = motor_commands.MotorCommands()
    inter = interpretor.Interpretor()
    contr = controller.Controller()
    sens = sensor_commands.SensorCommands()
    sensor_values_bus = Bus()
    interpreter_bus = Bus()
    controller_bus = Bus()

    sensor_delay = 1
    interpreter_delay = 1
    controller_delay = 1

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        eSensor = executor.submit(sensor_function, sensor_values_bus, sensor_delay)
        eInterpreter = executor.submit(interpreter_function, sensor_values_bus, interpreter_bus, interpreter_delay)

    eSensor.result()
    eInterpreter.result()


