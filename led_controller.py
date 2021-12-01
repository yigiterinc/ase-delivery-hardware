import RPi.GPIO as GPIO

from time import sleep
from typing import List


def init(self, gpios : List[int]) -> None:
    # Check if GPIO mode is set
    if GPIO.getmode() is None:
        raise RuntimeError("LEDs were not initialized since GPIO mode is not set!")
    
    # Setup GPIOs as output with initial state LOW
    GPIO.setup(gpios, GPIO.OUT, GPIO.LOW)
    self.leds = gpios

    
def turnOn(self, led : int) -> None:
    # Check if LED is initialized
    if led not in self.leds:
        raise RuntimeError("LED is not initialized, please call init beforehand!")
    
    # Turn LED on
    GPIO.output(led, GPIO.HIGH)

    
def turnOff(self, led: int) -> None:
    # Check if LED is initialized
    if led not in self.leds:
        raise RuntimeError("LED is not initialized, please call init beforehand!")

    # Turn LED off
    GPIO.output(led, GPIO.LOW)


def toggle(self, led : int, secs : int):
    # Toggle LED for secs seconds
    self.turnOn(led)
    sleep(secs)
    self.turnOff(led)
