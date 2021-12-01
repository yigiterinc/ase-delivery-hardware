import authentication_controller
import led_controller
import photo_resistor_controller

from math import isclose
from time import time_ns


# Global configuration variables
led_blinking_secs = 1
led_confirmation_secs = 3
opening_secs = 10
brightness_closed = 0


class BoxController:
    
    def init(self, led_green : int, led_red : int, photo_res : int) -> None:
        # Save LEDs, photo resistor and time configurations
        self.led_green = led_green
        self.led_red = led_red
        self.photo_res = photo_res
        self.open_secs = 0

        # Setup GPIO pins
        led_controller.init([led_green, led_red])
        photo_resistor_controller.init(photo_res)


    def __unlock(self) -> None:
        # Set absolute starting time
        self.open_secs = time_ns()


    def __lock(self) -> None:
        # As long as the brightness level does not embodies a closed box
        while not isclose(photo_resistor_controller.read_brightness(), brightness_closed):
            # Check if allowed opening time is exceeded and if yes toggle red LED
            if time_ns() - self.open_secs > opening_secs:
                led_controller.toggle(self.led_red, led_blinking_secs)   


    def handle_new_customer(self, user_id : int) -> None:
        # Check if customer is authenticated and if yes toggle green LED
        if authentication_controller.authenticate(user_id):
            led_controller.toggle(self.led_green, self.led_confirmation_secs)
            self.__unlock()
            self.__lock()
        # Otherwise toggle red LED
        else:
            led_controller.toggle(self.led_red, self.led_confirmation_secs) 
