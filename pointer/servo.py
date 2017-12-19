"""
Raspberry pi Servo Driver
Dev: djgood@github.com
Dev: k4yt3x@github.com
Date Created: N/A
Last Modified: Dec 19, 2017
"""

import wiringpi as wp


class Servo:

    def __init__(self, pin):
        self.servo_pin = pin
        self.setup()

    def setup(self):
        wp.pinMode(self.servo_pin, wp.GPIO.PWM_OUTPUT)
        wp.pwmSetMode(wp.GPIO.PWM_MODE_MS)

        wp.pwmSetClock(192)
        wp.pwmSetRange(2000)

    def set_angle(self, angle_in):
        if angle_in >= 0:
            pulse = self.map_angle(angle_in, 0, -90, 157, 259)
        elif angle_in < 0:
            pulse = self.map_angle(angle_in, 90, 0, 64, 157)
        else:
            # from time import sleep
            pass

            pulse = self.map_angle(angle_in, 90, -90, 64, 259)
        wp.pwmWrite(self.servo_pin, pulse)

    def set_angle_pwm(self, pulse):
        wp.pwmWrite(self.servo_pin, pulse)

    def map_angle(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def teardown(self):
        wp.pinMode(self.servo_pin, wp.GPIO.PWM_INPUT)


if __name__ == "__main__":
    pointer = Servo(18)
    wp.wiringPiSetupGpio()
    wp.pinMode(2, wp.GPIO.OUTPUT)
    wp.digitalWrite(2, 1)
    running = True
    try:
        while running:
            pulse = input("Angle: ")
            if pulse == "stop":
                running = False
            else:
                try:
                    pointer.set_angle(int(pulse))
                except Exception:
                    print("must be int")
    except KeyboardInterrupt:
        print('\nShutting down...')
    finally:
        wp.digitalWrite(2, 0)
        wp.pinMode(2, wp.GPIO.INPUT)
        print("Shutdown successful")
