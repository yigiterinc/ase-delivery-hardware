import RPi.GPIO as GPIO
from typing import List

class PhotoResistorController:

    def __init__(self, gpio : int) -> None:
        # Check if GPIO mode is set
        if GPIO.getmode() is None:
            raise RuntimeError("PhotoResistorController.turnOn(): LEDs were not initialized since GPIO mode is not set!")
    
        # Setup GPIOs as input
        GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.photores = gpio


    def read_brightness(self) -> int:
        return GPIO.input(self.photores)