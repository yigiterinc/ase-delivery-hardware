import RPi.GPIO as GPIO
from typing import List


def init(self, gpio : int) -> None:
    # Check if GPIO mode is set
    if GPIO.getmode() is None:
        raise RuntimeError("LEDs were not initialized since GPIO mode is not set!")
    
    # Setup GPIOs as input
    GPIO.setup(gpio, GPIO.IN)
    self.photores = gpio


def read_brightness() -> int:
    pass